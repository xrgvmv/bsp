import { Component, OnInit, OnDestroy, Input } from '@angular/core';
import { Subscription } from 'rxjs';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatCardModule } from '@angular/material/card';
import { MatSliderModule } from '@angular/material/slider';
import { FormsModule } from '@angular/forms';
import { MapService } from '../../service/map.service';
import { FlightService } from '../../service/flight.service';
import { MatListModule } from '@angular/material/list';
import * as L from 'leaflet';

@Component({
  selector: 'app-flight-history-control-panel',
  templateUrl: './flight-history-control-panel.component.html',
  styleUrls: ['./flight-history-control-panel.component.css'],
  standalone: true,
  imports: [
    CommonModule,
    MatButtonModule,
    MatIconModule,
    MatCardModule,
    MatSliderModule,
    FormsModule,
    MatListModule,
  ],
})
export class FlightHistoryControlPanelComponent implements OnInit, OnDestroy {
  @Input() map: L.Map | undefined;
  @Input() mapService: MapService | undefined;
  private flightSubscription?: Subscription;
  visible = false;

  flightData: { droneId: number; flightId: number; droneType: string } | null =
    null;
  droneId: number | null = null;
  flightId: number | null = null;
  droneType: string | null = null;
  currentIndex = 0;
  movementData: any[] = [];
  flightPath: L.Polyline | null = null;
  droneMarker: L.Marker | null = null;
  // droneInfo: any = null; // waiting for api update

  constructor(private flightService: FlightService) {}

  ngOnInit(): void {
    this.flightSubscription = this.flightService.flight.subscribe((flight) => {
      // console.log('Flight selected:', flight); // debug
      this.flightData = flight;
      this.visible = true;

      this.showPanel(flight.droneId, flight.flightId, flight.droneType);
    });
  }

  ngOnDestroy(): void {
    this.removeFlightFromMap();
    if (this.flightSubscription) {
      this.flightSubscription.unsubscribe();
    }
  }

  showPanel(droneId: number, flightId: number, droneType: string): void {
    this.visible = true;
    this.droneId = droneId;
    this.flightId = flightId;
    this.droneType = droneType;
    this.currentIndex = 0;

    // TODO: fix when api is updated
    // currently this doesn't do anything because api structure doesn't allow to ask for a single drone info based on drone id
    // if (droneType === 'DroneID') {
    //   this.mapService?.getDroneidInfo().subscribe((data) => {
    //     // this.droneInfo = data;
    //     // console.log('Drone info:', this.droneInfo); // debug
    //   });
    // } else if (droneType === 'RemoteID') {
    //   this.mapService?.getRemoteidInfo().subscribe((data) => {
    //     // this.droneInfo = data;
    //     // console.log('Drone info:', this.droneInfo); // debug
    //   });
    // }

    this.loadFlightData();
  }

  hidePanel(): void {
    this.visible = false;
    this.removeFlightFromMap();
  }

  loadFlightData(): void {
    if (!this.droneId || !this.flightId || !this.droneType) return;

    if (this.droneType === 'DroneID') {
      this.mapService!.getDroneidMovementInfoBasedOnID(
        this.droneId,
        this.flightId
      ).subscribe({
        next: (data: any) => {
          this.movementData = data.droneid_movements || [];
          // console.log('Movement data:', this.movementData); // debug
          this.displayFlightOnMap();
        },
      });
    } else {
      this.mapService!.getRemoteidMovementInfoBasedOnID(
        this.droneId,
        this.flightId
      ).subscribe({
        next: (data: any) => {
          this.movementData = data.remoteid_movements || [];
          // console.log('Movement data:', this.movementData); // debug
          this.displayFlightOnMap();
        },
      });
    }
  }

  displayFlightOnMap(): void {
    if (!this.map || this.movementData.length === 0) return;

    this.removeFlightFromMap();

    const coordinates = this.movementData.map((m) => [
      m.latitude || m.lat,
      m.longitude || m.lng,
    ]);

    this.flightPath = L.polyline(coordinates, {
      color: 'black',
      weight: 5,
      opacity: 1.0,
    }).addTo(this.map);

    this.showTimestampAtIndex(0);
  }

  showTimestampAtIndex(index: number): void {
    if (!this.map || this.movementData.length === 0) return;

    this.currentIndex = index;
    const movement = this.movementData[index];

    const lat = movement.latitude || movement.lat;
    const lng = movement.longitude || movement.lng;

    if (this.droneMarker) {
      this.droneMarker.setLatLng([lat, lng]);
    } else {
      this.droneMarker = L.marker([lat, lng], {
        icon: L.divIcon({
          className: 'custom-material-icon',
          html: '<i class="material-icons" style="color: blue;">keyboard_command</i>',
          iconSize: [38, 38],
          popupAnchor: [-0, -20],
        }),
      }).addTo(this.map);
    }

    this.map.panTo([lat, lng]);
  }

  previousTimestamp(): void {
    if (this.currentIndex > 0) {
      this.showTimestampAtIndex(this.currentIndex - 1);
    }
  }

  nextTimestamp(): void {
    if (this.currentIndex < this.movementData.length - 1) {
      this.showTimestampAtIndex(this.currentIndex + 1);
    }
  }

  onSliderChange(value: number): void {
    this.showTimestampAtIndex(value);
  }

  removeFlightFromMap(): void {
    if (this.flightPath && this.map) {
      this.map.removeLayer(this.flightPath);
      this.flightPath = null;
    }

    if (this.droneMarker && this.map) {
      this.map.removeLayer(this.droneMarker);
      this.droneMarker = null;
    }
  }
}
