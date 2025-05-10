import {
  Component,
  EventEmitter,
  Input,
  OnChanges,
  Output,
  SimpleChanges,
} from '@angular/core';
import { Remoteid } from '../../model/remoteid.model';
import { Droneid } from '../../model/droneid.model';
import { RemoteidMovement } from '../../model/remoteid-movement.model';
import { DroneidMovement } from '../../model/droneid-movement.model';
import { MatCardModule } from '@angular/material/card';
import { MatListModule } from '@angular/material/list';
import { MatIconModule } from '@angular/material/icon';
import { MatDividerModule } from '@angular/material/divider';
import { NgFor, NgIf } from '@angular/common';
import {MapService} from '../../service/map.service';
import {FlightCurrentControlComponent} from '../flight-current-control/flight-current-control.component';
import * as L from 'leaflet';

@Component({
  selector: 'app-uavs-list-view',
  imports: [
    MatCardModule,
    MatListModule,
    MatIconModule,
    MatDividerModule,
    NgFor,
    NgIf,
    FlightCurrentControlComponent,
  ],
  templateUrl: './uavs-list-view.component.html',
  styleUrls: ['./uavs-list-view.component.css'],
  standalone: true,
})
export class UavsListViewComponent implements OnChanges {
  @Input() remoteid_drones: Remoteid[] = [];
  @Input() droneid_drones: Droneid[] = [];
  @Input() remoteids_movement: RemoteidMovement[] = [];
  @Input() droneids_movement: DroneidMovement[] = [];
  @Input() map: L.Map | undefined;
  @Input() mapService: MapService | undefined;

  @Output() droneSelected = new EventEmitter<any>();
  movementData: any[] = [];

  combinedDroneData: any[] = [];
  selectedDrone: any;
  flightInfo: {
    droneId: number;
    flightId: number;
    droneType: string;
  } | null = null;

  ngOnChanges(changes: SimpleChanges): void {
    this.mergeDroneData();
    // console.log(this.combinedDroneData); // debug

    if (this.selectedDrone) {
      const updatedDrone = this.combinedDroneData.find(
        (drone) =>
          drone.info.serial_number === this.selectedDrone.info.serial_number &&
          drone.type === this.selectedDrone.type
      );

      if (updatedDrone) {
        this.selectedDrone = updatedDrone;
        // console.log('Updated drone:', updatedDrone); // debug
      }
    }
  }

  private mergeDroneData(): void {
    this.combinedDroneData = [
      ...this.remoteid_drones.map((drone) => {
        const movement = this.remoteids_movement.find(
          (m) => m.remoteid_info_id === drone.id
        );
        return {
          type: 'RemoteID',
          info: drone,
          movement: movement,
        };
      }),
      ...this.droneid_drones.map((drone) => {
        const movement = this.droneids_movement.find(
          (m) => m.droneid_info_id === drone.id
        );
        return {
          type: 'DroneID',
          info: drone,
          movement: movement,
        };
      }),
    ];
  }

  closeDroneDetails(): void {
    this.selectedDrone = null;
  }

  onDroneClick(drone: any): void {
    this.selectedDrone = drone;
    console.log('Selected drone:', drone); // debug
    this.droneSelected.emit(drone);

    if (this.map && drone.movement) {
      const latitude = drone.movement.lat || drone.movement.latitude;
      const longitude = drone.movement.lng || drone.movement.longitude;
      this.map.panTo([latitude, longitude]);

      // draw flight on map (with flight-history-control-panel)
    if (drone.type === 'DroneID') {
      this.mapService?.getDroneidFlightsBasedOnID(drone.info.id).subscribe((data: any) => {
        if (data && data.droneid_flight) {
          this.flightInfo = {
            droneId: data.droneid_flight.drone_id,
            flightId: data.droneid_flight.flight_id,
            droneType: 'DroneID',
          };
        }
      });
    } else if (drone.type === 'RemoteID') {
        this.mapService?.getRemoteidFlightsBasedOnID(drone.info.id).subscribe((data: any) => {
          if (data && data.remoteid_flight) {
            this.flightInfo = {
              droneId: data.remoteid_flight.drone_id,
              flightId: data.remoteid_flight.flight_id,
              droneType: 'RemoteID',
            };
          }
        });
    }

      // everything below that was temp solution
      // but might be useful in some time so im leaving it here for now


      // if (drone.type === 'DroneID') {
      //   this.mapService!.getCurrentDroneidFlightInfo(drone.info.id, 20).subscribe({
      //     next: (data: any) => {
      //       this.movementData = data.droneid_movements || [];
      //       console.log('Movement data:', this.movementData); // debug
      //       this.displayFlightOnMap();
      //     },
      //   });
      // } else if (drone.type === 'RemoteID') {
      //   this.mapService!.getCurrentRemoteidFlightInfo(drone.info.id, 20).subscribe({
      //     next: (data: any) => {
      //       this.movementData = data.remoteid_movements || [];
      //       console.log('Movement data:', this.movementData); // debug
      //       this.displayFlightOnMap();
      //     },
      //   });
      // }
    }
  }

  // display flight related things to be removed when
  // flight-history-control-panel will be used after api update

  // displayFlightOnMap(): void {
  //   if (!this.map || this.movementData.length === 0) return;
  //
  //   this.removeFlightFromMap();
  //
  //   const coordinates = this.movementData.map((m) => [
  //     m.latitude || m.lat,
  //     m.longitude || m.lng,
  //   ]);
  //
  //   const polyline = L.polyline(coordinates, { color: 'red', weight: 10 }).addTo(this.map);
  //   this.map.fitBounds(polyline.getBounds());
  // }
  //
  // removeFlightFromMap(): void {
  //   if (this.map) {
  //     this.map.eachLayer((layer) => {
  //       if (layer instanceof L.Polyline) {
  //         this.map!.removeLayer(layer);
  //       }
  //     });
  //   }
  // }
}
