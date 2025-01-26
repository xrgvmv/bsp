import {
  Component,
  OnInit,
} from '@angular/core';
import * as L from 'leaflet';
import { combineLatest, Observable } from 'rxjs';
import { MapService } from '../../service/map.service';
import { AboutViewComponent } from '../about-view/about-view/about-view.component';
import { UavsListViewComponent } from '../uavs-list-view/uavs-list-view/uavs-list-view.component';
import { RemoteidMovement } from '../../model/remoteid-movement.model';
import { DroneidMovement } from '../../model/droneid-movement.model';
import { Remoteid } from '../../model/remoteid.model';
import { Droneid } from '../../model/droneid.model';

@Component({
  selector: 'app-map-view',
  imports: [AboutViewComponent, UavsListViewComponent],
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

  constructor(private service: MapService) {}

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
    }, 5000); // 5s
  }

  private initMap(): void {
    this.map = L.map('map', {
      center: [54.371684, 18.612406], // pg weti
      zoom: 20,
    });

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
      minZoom: 3,
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

        console.log('Droneid drones:', this.droneid_drones); // debug
        console.log('Remoteid drones:', this.remoteid_drones); // debug
        console.log('Droneids movement:', this.droneids_movement); // debug
        console.log('Remoteids movement:', this.remoteids_movement); // debug

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
    this.addMarkers(this.remoteid_drones, this.remoteids_movement, this.uavIcon, 'RemoteID'); // remoteid
    this.addMarkers(this.droneid_drones, this.droneids_movement, this.uavIcon, 'DroneID'); // droneid
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
      const movement = movements.find(
        (m: any) => m.drone_id === drone.id || m.remote_id === drone.id
      );

      if (movement) {
        const marker = L.marker([movement.latitude, movement.longitude], {
          icon,
        }).addTo(this.map!);

        marker.bindPopup(
          `<b>Rodzaj protokołu:</b> ${type}<br><b>Numer seryjny:</b> ${
            drone.serial_number || drone.serial_number
          }<br><b>Latitude:</b> ${movement.latitude}<br><b>Longitude:</b> ${
            movement.longitude
          }`
        );
        this.markers.push(marker);

      } else {
        console.log(
          `No movement data for drone ID: ${drone.id || drone.remote_id} Serial number: ${drone.serial_number}`
        );
      }
    });
  }
}
