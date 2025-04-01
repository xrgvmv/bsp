import { Component, Inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {
  MAT_DIALOG_DATA,
  MatDialogModule,
  MatDialogRef,
} from '@angular/material/dialog';
import { DateAdapter } from '@angular/material/core';
import * as L from 'leaflet';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatListModule } from '@angular/material/list';
import { MatIconModule } from '@angular/material/icon';
import { MatDividerModule } from '@angular/material/divider';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { DroneidFlight } from '../../model/droneid-flight.model';
import { Remoteid } from '../../model/remoteid.model';
import { Droneid } from '../../model/droneid.model';
import { RemoteidFlight } from '../../model/remoteid-flight.model';
import { provideNativeDateAdapter } from '@angular/material/core';
import { FlightService } from '../../service/flight.service';
import { MapService } from '../../service/map.service';

interface ArchiveDialogData {
  flightService: FlightService;
  service: MapService;
  map: L.Map;
}

@Component({
  selector: 'app-historic-data-view-dialog-content',
  templateUrl: './historic-data-view-dialog-content.component.html',
  styleUrls: ['./historic-data-view-dialog-content.component.css'],
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatDialogModule,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatListModule,
    MatIconModule,
    MatDividerModule,
    MatDatepickerModule,
    MatNativeDateModule,
  ],
  providers: [provideNativeDateAdapter()],
})
export class HistoricDataViewDialogContentComponent implements OnInit {
  archived_droneid: Droneid[] = [];
  archived_remoteid: Remoteid[] = [];
  droneidFlights: DroneidFlight[] = [];
  remoteidFlights: RemoteidFlight[] = [];

  selectedDrone: any = null;
  selectedFlight: any = null;

  mapService: MapService;
  map: L.Map;

  // filters
  protocolFilter: string = 'all'; // all, droneid, remoteid
  searchTerm: string = '';
  startDate: Date | null = null;
  endDate: Date | null = null;

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: ArchiveDialogData,
    public dialogRef: MatDialogRef<HistoricDataViewDialogContentComponent>,
    private flightService: FlightService,
    private dateAdapter: DateAdapter<Date>
  ) {
    this.mapService = this.data.service;
    this.map = this.data.map;
    this.dateAdapter.setLocale('en-GB'); // easy way to change date format from dd/mm/yyyy to mm/dd/yyyy
  }

  ngOnInit(): void {
    if (!this.mapService) {
      console.error('Map service error');
      return;
    }

    this.mapService.getAllDroneidInfo().subscribe((data) => {
      this.archived_droneid = data.droneid_info_list;
      // console.log('Archived DroneID data loaded:', this.archived_droneid); // debug
    });

    this.mapService.getAllRemoteidInfo().subscribe((data) => {
      this.archived_remoteid = data.remoteid_info_list;
      // console.log('Archived RemoteID data loaded:', this.archived_remoteid); // debug
    });
  }

  // drones filters
  filteredDrones(): any[] {
    let combined: any[] = [];

    if (this.protocolFilter === 'all' || this.protocolFilter === 'droneid') {
      combined = combined.concat(
        this.archived_droneid.map((drone) => ({
          ...drone,
          type: 'DroneID',
        }))
      );
    }

    if (this.protocolFilter === 'all' || this.protocolFilter === 'remoteid') {
      combined = combined.concat(
        this.archived_remoteid.map((drone) => ({
          ...drone,
          type: 'RemoteID',
        }))
      );
    }

    if (this.searchTerm) {
      const search = this.searchTerm.toLowerCase();
      combined = combined.filter((drone) =>
        drone.serial_number.toLowerCase().includes(search)
      );
    }

    return combined;
  }

  selectDrone(drone: any): void {
    this.selectedDrone = drone;
    this.droneidFlights = [];
    this.remoteidFlights = [];
    // console.log('Selected drone:', this.selectedDrone); // debug

    if (this.selectedDrone.type === 'DroneID') {
      this.mapService
        .getDroneidFlightsInfoBasedOnID(this.selectedDrone.id)
        .subscribe((data: any) => {
          this.droneidFlights = data.droneid_flights || [];
          // console.log('DroneID flights loaded:', this.droneidFlights); // debug
        });
    } else if (this.selectedDrone.type === 'RemoteID') {
      this.mapService
        .getRemoteidFlightsInfoBasedOnID(this.selectedDrone.id)
        .subscribe((data: any) => {
          this.remoteidFlights = data.remoteid_flights || [];
          // console.log('RemoteID flights loaded:', this.remoteidFlights); // debug
        });
    }
  }

  // flights filters
  filteredFlights(): (DroneidFlight | RemoteidFlight)[] {
    if (!this.selectedDrone) {
      return [];
    }

    let flights: (DroneidFlight | RemoteidFlight)[] = [];

    if (this.selectedDrone.type === 'DroneID') {
      flights = [...this.droneidFlights];
    } else {
      flights = [...this.remoteidFlights];
    }

    if (this.startDate) {
      flights = flights.filter(
        (flight) => new Date(flight.start_time) >= new Date(this.startDate!)
      );
    }

    if (this.endDate) {
      flights = flights.filter(
        (flight) => new Date(flight.end_time) <= new Date(this.endDate!)
      );
    }

    return flights;
  }

  confirmSelection(): void {
    if (this.selectedDrone && this.selectedFlight) {
      // send selected flight info to flight service
      this.flightService.selectFlight(
        this.selectedFlight.drone_id,
        this.selectedFlight.flight_id,
        this.selectedDrone.type
      );
    }
  }

  // used in HTML to select flight
  selectFlight(flight: any): void {
    this.selectedFlight = flight;
  }
}
