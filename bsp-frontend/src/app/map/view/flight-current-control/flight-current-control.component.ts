import { Component, OnInit, OnDestroy, Input, OnChanges } from '@angular/core';
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

// TODO: currently this component interferes with flight-history-control-panel

@Component({
  selector: 'app-flight-current-control',
  imports: [
    CommonModule,
    MatButtonModule,
    MatIconModule,
    MatCardModule,
    MatSliderModule,
    FormsModule,
    MatListModule,
  ],
  templateUrl: './flight-current-control.component.html',
  styleUrl: './flight-current-control.component.css',
})
export class FlightCurrentControlComponent
  implements OnInit, OnDestroy, OnChanges
{
  @Input() map: L.Map | undefined;
  @Input() mapService: MapService | undefined;
  @Input() flightData: {
    droneId: number;
    flightId: number;
    droneType: string;
  } | null = null;
  droneId: number | null = null;
  flightId: number | null = null;
  droneType: string | null = null;
  movementData: any[] = [];
  visible = false;
  flightPath: L.Polyline | null = null;
  maxTimestamps = 100; // default limit
  refreshInterval: any;

  constructor(private flightService: FlightService) {}

  ngOnInit(): void {
    if (
      this.flightData &&
      this.flightData.droneId &&
      this.flightData.flightId
    ) {
      this.showPanel(
        this.flightData.droneId,
        this.flightData.flightId,
        this.flightData.droneType
      );
    }

    this.refreshInterval = setInterval(() => {
      if (this.visible) {
        this.refreshMarker();
        // console.log('refresh'); // debug
      }
    }, 500); // 0.5s
  }

  ngOnChanges(): void {
    if (this.flightData) {
      this.showPanel(
        this.flightData.droneId,
        this.flightData.flightId,
        this.flightData.droneType
      );
    }

    this.refreshInterval = setInterval(() => {
      if (this.visible) {
        this.refreshMarker();
        // console.log('refresh'); // debug
      }
    }, 500); // 0.5s
  }

  ngOnDestroy(): void {
    this.removeFlightFromMap();
  }

  refreshMarker(): void {
    if (this.droneId && this.flightId && this.droneType) {
      this.loadFlightData();
    }
  }

  showPanel(droneId: number, flightId: number, droneType: string): void {
    this.visible = true;
    this.droneId = droneId;
    this.flightId = flightId;
    this.droneType = droneType;

    this.loadFlightData();
  }

  hidePanel(): void {
    this.visible = false;
    this.removeFlightFromMap();

    if (this.refreshInterval) {
      clearInterval(this.refreshInterval);
      this.refreshInterval = null;
    }
  }

  loadFlightData(): void {
    // console.log('Loading flight, data: ', this.droneId, this.flightId, this.droneType); // debug
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

    const limitedData = this.movementData.slice(-this.maxTimestamps).reverse();
    const coordinates = limitedData.map((m) => [
      m.latitude || m.lat,
      m.longitude || m.lng,
    ]);

    this.flightPath = L.polyline(coordinates, {
      color: 'blue',
      weight: 4,
      opacity: 0.7,
    }).addTo(this.map);
  }

  onMaxTimestampsChange(event: any): void {
    const value = event.value || event; // Obsługa zarówno zdarzenia, jak i liczby
    this.maxTimestamps = value;
    if (this.visible) {
      this.displayFlightOnMap();
    }
  }

  removeFlightFromMap(): void {
    if (this.flightPath && this.map) {
      this.map.removeLayer(this.flightPath);
      this.flightPath = null;
    }
  }
}
