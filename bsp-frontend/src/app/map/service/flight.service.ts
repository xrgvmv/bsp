import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class FlightService {
  private flightSelected = new Subject<{
    droneId: number;
    flightId: number;
    droneType: string;
  }>();

  flight = this.flightSelected.asObservable();

  selectFlight(droneId: number, flightId: number, droneType: string): void {
    this.flightSelected.next({ droneId, flightId, droneType });
  }
}
