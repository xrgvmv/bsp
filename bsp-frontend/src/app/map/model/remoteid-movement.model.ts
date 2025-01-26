export interface RemoteidMovement {
  id: number;
  drone_id: number;
  status: number;
  timestamp: number;
  direction: number;
  speed_horizontal: number;
  speed_vertical: number;
  latitude: number;
  longitude: number;
  altitude_baro: number;
  altitude_geo: number;
  height: number;
}
