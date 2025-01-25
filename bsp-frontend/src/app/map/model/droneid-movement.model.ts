export interface DroneidMovement {
  id: number;
  drone_id: number;
  timestamp: number;
  pkt_len: number;
  longitude: number;
  latitude: number;
  altitude: number;
  height: number;
  v_north: number;
  v_east: number;
  v_up: number;
  d_1_angle: number;
  app_lat: number;
  app_lon: number;
  longitude_home: number;
  latitude_home: number;
}
