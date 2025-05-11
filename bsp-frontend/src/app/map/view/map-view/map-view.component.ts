import { Component, OnInit } from '@angular/core';
import { combineLatest } from 'rxjs';
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
export class MapViewComponent implements OnInit {
  map: L.Map | undefined;
  remoteid_drones: Remoteid[] = [];
  droneid_drones: Droneid[] = [];
  remoteids_movement: RemoteidMovement[] = [];
  droneids_movement: DroneidMovement[] = [];
  private markers: L.Marker[] = [];
  private uavIcon = L.divIcon({
    className: 'custom-material-icon',
    html: '<i class="material-icons">keyboard_command</i>', // yes this is macbook command key icon
    iconSize: [38, 38],
    popupAnchor: [-0, -20],
  }) as L.Icon;

  constructor(public service: MapService) {}

  ngOnInit(): void {
    this.initMap();

    // this is needed to fix incorrect map rendering, might try to find better solution later
    this.map?.whenReady(() => {
      setTimeout(() => {
        this.map?.invalidateSize();
      }, 20);
    });

    setInterval(() => {
      this.startFetchingMapView();
    }, 1500); // 1.5s
  }

  private initMap(): void {
    this.map = L.map('map', {
      center: [54.371684, 18.612406], // pg weti
      zoom: 10,
    });

      if (!this.map) return;

      // offline maps
    // L.tileLayer('bsp_map/{z}/{x}/{y}.png', { // 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
    //   maxZoom: 11,
    //   minZoom: 3,
    //   attribution:
    //     '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    // }).addTo(this.map);

      // online maps
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { // 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
        maxZoom: 19,
        minZoom: 2,
        attribution:
          '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      }).addTo(this.map);
  }

  private startFetchingMapView(): void {
    combineLatest([
      this.service.getDroneidInfo(),
      this.service.getRemoteidInfo(),
      this.service.getDroneidMovementInfo(),
      this.service.getRemoteidMovementInfo(),
    ]).subscribe(
      ([droneidData, remoteidData, droneidMovements, remoteidMovements]) => {
        this.droneid_drones = droneidData.droneid_info_list;
        this.remoteid_drones = remoteidData.remoteid_info_list;
        this.droneids_movement = droneidMovements.droneid_movement_list;
        this.remoteids_movement = remoteidMovements.remoteid_movement_list;

        // console.log('Droneid drones:', this.droneid_drones); // debug
        // console.log('Remoteid drones:', this.remoteid_drones); // debug
        // console.log('Droneids movement:', this.droneids_movement); // debug
        // console.log('Remoteids movement:', this.remoteids_movement); // debug

        this.updateMapMarkers();
      }
    );
  }

  private updateMapMarkers(): void {
    if (!this.map) {
      console.error('Map not initialized');
      return;
    }

    if (
      !this.remoteid_drones ||
      !this.droneid_drones ||
      !this.remoteids_movement ||
      !this.droneids_movement
    ) {
      console.error('Some data is missing:', {
        remoteidDronesLength: this.remoteid_drones?.length || 0,
        droneidDronesLength: this.droneid_drones?.length || 0,
        remoteidMovementsLength: this.remoteids_movement?.length || 0,
        droneidMovementsLength: this.droneids_movement?.length || 0,
      });
      return;
    }

    this.clearMarkers(); // clear all markers

    this.addMarkers(
      this.remoteid_drones,
      this.remoteids_movement,
      this.uavIcon,
      'RemoteID'
    ); // remoteid
    this.addMarkers(
      this.droneid_drones,
      this.droneids_movement,
      this.uavIcon,
      'DroneID'
    ); // droneid
  }

  private clearMarkers(): void {
    this.markers.forEach((marker) => this.map!.removeLayer(marker));
    this.markers = [];
  }

  private addMarkers(
    drones: any[],
    movements: any[],
    icon: L.Icon,
    type: string
  ): void {
    drones.forEach((drone) => {
      const movement =
        type === 'RemoteID'
          ? movements.find((m: any) => m.remoteid_info_id === drone.id)
          : movements.find((m: any) => m.droneid_info_id === drone.id);

      if (movement) {
        const latitude = movement.lat || movement.latitude;
        const longitude = movement.lng || movement.longitude;

        if (latitude && longitude) {
          const marker = L.marker([latitude, longitude], {
            icon,
          }).addTo(this.map!);

          marker.bindPopup(
            `<b>Rodzaj protokołu:</b> ${type}<br><b>Numer seryjny:</b> ${drone.serial_number}<br><b>Latitude:</b> ${latitude}<br><b>Longitude:</b> ${longitude}`
          );
          this.markers.push(marker);
        }
      } else {
        console.log(
          `No movement data for ${type} drone ID: ${drone.id}, Serial number: ${drone.serial_number}`
        );
      }
    });
  }
}
