import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Remoteid_info_list } from '../model/remoteid_info_list.model';
import { Remoteid_movement_list } from '../model/remoteid_movement_list.model';
import { Droneid_info_list } from '../model/droneid_info_list.model';
import { Droneid_movement_list } from '../model/droneid_movement_list.model';

@Injectable({
  providedIn: 'root',
})
export class MapService {
  constructor(private http: HttpClient) {}

  getRemoteidInfo(): Observable<Remoteid_info_list> {
    return this.http.get<Remoteid_info_list>('/api/get_remoteid_info');
  }

  getRemoteidMovementInfo(): Observable<Remoteid_movement_list> {
    return this.http.get<Remoteid_movement_list>('/api/get_remoteid_movement');
  }

  getDroneidInfo(): Observable<Droneid_info_list> {
    return this.http.get<Droneid_info_list>('/api/get_droneid_info');
  }

  getDroneidMovementInfo(): Observable<Droneid_movement_list> {
    return this.http.get<Droneid_movement_list>('/api/get_droneid_movement');
  }
}
