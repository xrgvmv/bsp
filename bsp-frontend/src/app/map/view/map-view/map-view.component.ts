import { Component, OnInit, OnDestroy } from '@angular/core';
import { combineLatest, Subscription, interval } from 'rxjs';
import { switchMap, startWith } from 'rxjs/operators';
import * as L from 'leaflet';
import { MapService } from '../../service/map.service';
import { AboutViewComponent } from '../about-view/about-view.component';
import { UavsListViewComponent } from '../uavs-list-view/uavs-list-view.component';
import { RemoteidMovement } from '../../model/remoteid-movement.model';
import { DroneidMovement } from '../../model/droneid-movement.model';
import { Remoteid } from '../../model/remoteid.model';
import { Droneid } from '../../model/droneid.model';
import { HistoricDataViewIconComponent } from '../historic-data-view-icon/historic-data-view-icon.component';
import { ImportViewIconComponent } from '../import-view-icon/import-view-icon.component';
import { FlightHistoryControlPanelComponent } from '../flight-history-control-panel/flight-history-control-panel.component';
import { DataUploadIconComponent } from '../data-upload-icon/data-upload-icon.component';

@Component({
  selector: 'app-map-view',
  imports: [
    AboutViewComponent,
    UavsListViewComponent,
    HistoricDataViewIconComponent,
    ImportViewIconComponent,
    FlightHistoryControlPanelComponent,
    DataUploadIconComponent,
  ],
  templateUrl: './map-view.component.html',
  styleUrl: './map-view.component.css',
})
export class MapViewComponent implements OnInit, OnDestroy {
  map: L.Map | undefined;
  remoteid_drones: Remoteid[] = [];
  droneid_drones: Droneid[] = [];
  remoteids_movement: RemoteidMovement[] = [];
  droneids_movement: DroneidMovement[] = [];
  private markers: L.Marker[] = [];
  private uavIcon = L.divIcon({
    className: 'custom-material-icon',
    html: '<i class="material-icons">keyboard_command</i>',
    iconSize: [38, 38],
    popupAnchor: [-0, -20],
  }) as L.Icon;

  private dataFetchingSubscription: Subscription | undefined;
  private tileLayerAdded = false;

  constructor(public service: MapService) {}

  ngOnInit(): void {
    this.initMap();

    this.dataFetchingSubscription = interval(1500)
      .pipe(
        startWith(0),
        switchMap(() =>
          combineLatest([
            this.service.getDroneidInfo(),
            this.service.getRemoteidInfo(),
            this.service.getDroneidMovementInfo(),
            this.service.getRemoteidMovementInfo(),
          ])
        )
      )
      .subscribe(
        ([droneidData, remoteidData, droneidMovements, remoteidMovements]) => {
          this.droneid_drones = droneidData.droneid_info_list;
          this.remoteid_drones = remoteidData.remoteid_info_list;
          this.droneids_movement = droneidMovements.droneid_movement_list;
          this.remoteids_movement = remoteidMovements.remoteid_movement_list;

          if (this.tileLayerAdded) {
            this.updateMapMarkers();
          }
        },
        (error) => {
          console.error('Error fetching map data:', error);
        }
      );
  }

  ngOnDestroy(): void {
    if (this.dataFetchingSubscription) {
      this.dataFetchingSubscription.unsubscribe();
    }
    this.map?.remove();
  }

  private async testOnlineConnection(): Promise<boolean> {
    if (!navigator.onLine) {
      return false;
    }
    const testUrl = 'https://tile.openstreetmap.org/1/1/1.png';
    try {
      await fetch(testUrl, {
        method: 'HEAD',
        mode: 'no-cors',
        cache: 'no-store',
        signal: AbortSignal.timeout(2000)
      });
      return true;
    } catch (error) {
      return false;
    }
  }

  private async initMap(): Promise<void> {
    this.map = L.map('map', {
      center: [54.371684, 18.612406], //pg weti
      zoom: 10,
    });

    if (!this.map) {
      return;
    }

    const isOnline = await this.testOnlineConnection();

    if (isOnline) {
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        minZoom: 2,
        attribution:
          '© <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      }).addTo(this.map);
    } else {
      L.tileLayer('bsp_map/{z}/{x}/{y}.png', {
        maxZoom: 13,
        minZoom: 3,
        attribution:
          '© <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      }).addTo(this.map);
    }
    this.tileLayerAdded = true;

    this.map?.whenReady(() => {
      setTimeout(() => {
        this.map?.invalidateSize();
        if (this.droneid_drones.length > 0 || this.remoteid_drones.length > 0) {
          this.updateMapMarkers();
        }
      }, 30);
    });
  }

  private updateMapMarkers(): void {
    if (!this.map || !this.tileLayerAdded) {
      return;
    }

    const remoteidDronesLength = this.remoteid_drones?.length ?? 0;
    const droneidDronesLength = this.droneid_drones?.length ?? 0;
    const remoteidMovementsLength = this.remoteids_movement?.length ?? 0;
    const droneidMovementsLength = this.droneids_movement?.length ?? 0;

    if (
      !this.remoteid_drones ||
      !this.droneid_drones ||
      !this.remoteids_movement ||
      !this.droneids_movement
    ) {
      // console.warn można zostawić lub usunąć, zależnie od preferencji debugowania
    }

    this.clearMarkers();

    if (this.remoteid_drones && this.remoteids_movement) {
      this.addMarkers(
        this.remoteid_drones,
        this.remoteids_movement,
        this.uavIcon,
        'RemoteID'
      );
    }
    if (this.droneid_drones && this.droneids_movement) {
      this.addMarkers(
        this.droneid_drones,
        this.droneids_movement,
        this.uavIcon,
        'DroneID'
      );
    }
  }

  private clearMarkers(): void {
    if (!this.map) return;
    this.markers.forEach((marker) => this.map!.removeLayer(marker));
    this.markers = [];
  }

  private addMarkers(
    drones: Remoteid[] | Droneid[],
    movements: RemoteidMovement[] | DroneidMovement[],
    icon: L.Icon,
    type: string
  ): void {
    if (!this.map) return;

    drones.forEach((drone) => {
      const movement = movements.find((m: any) =>
        type === 'RemoteID'
          ? m.remoteid_info_id === (drone as Remoteid).id
          : m.droneid_info_id === (drone as Droneid).id
      );

      if (movement) {
        const latitude = (movement as any).lat ?? (movement as any).latitude;
        const longitude = (movement as any).lng ?? (movement as any).longitude;

        if (typeof latitude === 'number' && typeof longitude === 'number') {
          const marker = L.marker([latitude, longitude], {
            icon,
          }).addTo(this.map!);

          marker.bindPopup(
            `<b>Rodzaj protokołu:</b> ${type}<br><b>Numer seryjny:</b> ${drone.serial_number}<br><b>Latitude:</b> ${latitude.toFixed(6)}<br><b>Longitude:</b> ${longitude.toFixed(6)}`
          );
          this.markers.push(marker);
        }
      } else {
        // console.log(
        //   `No movement data for ${type} drone ID: ${drone.id}, Serial number: ${drone.serial_number}`
        // );
      }
    });
  }
}
