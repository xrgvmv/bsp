export interface Uav {
  altitudeBaro: number;
  altitudeGeo: number;
  baroAccuracy: number;
  direction: number;
  height: number;
  heightType: number;
  horizAccuracy: number;
  id: number;
  latitude: string;
  longitude: string;
  speedAccuracy: number;
  speedHorizontal: number;
  speedVertical: number;
  status: number;
  timestamp: number;
  tsAccuracy: number;
  vertAccuracy: number;
}
