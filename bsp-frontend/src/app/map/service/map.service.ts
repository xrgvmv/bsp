import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Remoteid_info_list } from '../model/remoteid_info_list.model';
import { Remoteid_movement_list } from '../model/remoteid_movement_list.model';
import { Droneid_info_list } from '../model/droneid_info_list.model';
import { Droneid_movement_list } from '../model/droneid_movement_list.model';
import { DroneidFlightList } from '../model/droneid-flight-list.model';
import { RemoteidFlightList } from '../model/remoteid-flight-list.model';

@Injectable({
  providedIn: 'root',
})
export class MapService {
  constructor(private http: HttpClient) {}

  // live

  getRemoteidInfo(): Observable<Remoteid_info_list> {
    return this.http.get<Remoteid_info_list>('/api/get_current_remoteid_info');
  }

  getRemoteidMovementInfo(): Observable<Remoteid_movement_list> {
    return this.http.get<Remoteid_movement_list>(
      '/api/get_current_remoteid_movement'
    );
  }

  getDroneidInfo(): Observable<Droneid_info_list> {
    return this.http.get<Droneid_info_list>('/api/get_current_droneid_info');
  }

  getDroneidMovementInfo(): Observable<Droneid_movement_list> {
    return this.http.get<Droneid_movement_list>(
      '/api/get_current_droneid_movement'
    );
  }

  // archive flights

  getAllDroneidInfo(): Observable<Droneid_info_list> {
    return this.http.get<Droneid_info_list>('/api/get_all_droneid_info');
  }

  getAllRemoteidInfo(): Observable<Remoteid_info_list> {
    return this.http.get<Remoteid_info_list>('/api/get_all_remoteid_info');
  }

  getDroneidFlightsInfoBasedOnID(
    droneID: number
  ): Observable<DroneidFlightList> {
    return this.http.get<DroneidFlightList>(
      '/api/get_droneid_flights_based_on_id_of_drone',
      {
        params: {
          drone_id: droneID.toString(),
        },
      }
    );
  }

  getRemoteidFlightsInfoBasedOnID(
    droneID: number
  ): Observable<RemoteidFlightList> {
    return this.http.get<RemoteidFlightList>(
      '/api/get_remoteid_flights_based_on_id_of_drone',
      {
        params: {
          drone_id: droneID.toString(),
        },
      }
    );
  }

  getDroneidMovementInfoBasedOnID(
    droneID: number,
    flightID: number
  ): Observable<Droneid_movement_list> {
    return this.http.get<Droneid_movement_list>(
      '/api/get_droneid_movements_based_on_id_of_drone_and_flight',
      {
        params: {
          drone_id: droneID.toString(),
          flight_id: flightID.toString(),
        },
      }
    );
  }

  getRemoteidMovementInfoBasedOnID(
    droneID: number,
    flightID: number
  ): Observable<Remoteid_movement_list> {
    return this.http.get<Remoteid_movement_list>(
      '/api/get_remoteid_movements_based_on_id_of_drone_and_flight',
      {
        params: {
          drone_id: droneID.toString(),
          flight_id: flightID.toString(),
        },
      }
    );
  }
}
