import {Component, EventEmitter, Input, OnChanges, Output, SimpleChanges} from '@angular/core';
import { Remoteid } from '../../../model/remoteid.model';
import { Droneid } from '../../../model/droneid.model';
import { RemoteidMovement } from '../../../model/remoteid-movement.model';
import { DroneidMovement } from '../../../model/droneid-movement.model';
import { MatCardModule } from '@angular/material/card';
import { MatListModule } from '@angular/material/list';
import { MatIconModule } from '@angular/material/icon';
import { MatDividerModule } from '@angular/material/divider';
import { NgFor, NgIf } from '@angular/common';
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
  ],
  templateUrl: './uavs-list-view.component.html',
  styleUrls: ['./uavs-list-view.component.css'],
})
export class UavsListViewComponent implements OnChanges {
  @Input() remoteid_drones: Remoteid[] = [];
  @Input() droneid_drones: Droneid[] = [];
  @Input() remoteids_movement: RemoteidMovement[] = [];
  @Input() droneids_movement: DroneidMovement[] = [];
  @Input() map: L.Map | undefined;

  @Output() droneSelected = new EventEmitter<any>();

  combinedDroneData: any[] = [];
  selectedDrone: any;

  ngOnChanges(changes: SimpleChanges): void {
    this.mergeDroneData();
  }

  private mergeDroneData(): void {
    this.combinedDroneData = [
      ...this.remoteid_drones.map((drone) => {
        const movement = this.remoteids_movement.find(
          (m) => m.drone_id === drone.id
        );
        return {
          type: 'RemoteID',
          info: drone,
          movement: movement || null,
        };
      }),
      ...this.droneid_drones.map((drone) => {
        const movement = this.droneids_movement.find(
          (m) => m.drone_id === drone.id
        );
        return {
          type: 'DroneID',
          info: drone,
          movement: movement || null,
        };
      }),
    ];
  }

  closeDroneDetails(): void {
    this.selectedDrone = null;
  }

  onDroneClick(drone: any): void {
    this.selectedDrone = drone;
    this.droneSelected.emit(drone);

    if (this.map) {
      this.map.panTo([drone.movement.latitude, drone.movement.longitude]);
    }
  }
}
