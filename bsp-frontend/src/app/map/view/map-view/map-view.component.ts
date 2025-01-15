import { AfterViewInit, Component, OnInit } from '@angular/core';
import * as L from 'leaflet';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Uavs } from '../../model/uavs.model';
import { MapService } from '../../service/map.service';
import { Uav } from '../../model/uav.model';
import { AboutViewComponent } from '../about-view/about-view/about-view.component';
import { UavsListViewComponent } from '../uavs-list-view/uavs-list-view/uavs-list-view.component';

@Component({
  selector: 'app-map-view',
  imports: [AboutViewComponent, UavsListViewComponent],
  templateUrl: './map-view.component.html',
  styleUrl: './map-view.component.css',
})
export class MapViewComponent implements OnInit {
  private map: L.Map | undefined;
  private uavs: Uavs | undefined; // list of UAVs to be displayed on the map
  private markers: L.Marker[] = [];
  private uavIcon = L.divIcon({
    className: 'custom-material-icon',
    html: '<i class="material-icons">keyboard_command</i>', // yes this is macbook command key icon
    iconSize: [38, 38],
    popupAnchor: [-0, -20],
  });

  constructor(private service: MapService) {}

  ngOnInit(): void {
    this.initMap();

    // this is needed to fix incorrect map rendering, might try to find better solution later
    this.map?.whenReady(() => {
      setTimeout(() => {
        this.map?.invalidateSize();
      }, 20);
    });

    setInterval(() => {
      this.startFetchingMapView();
    }, 10000); // 10s
  }

  private initMap(): void {
    this.map = L.map('map', {
      center: [54.371684, 18.612406], // pg weti
      zoom: 20,
    });

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
      minZoom: 3,
      attribution:
        '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    }).addTo(this.map);
  }

  private startFetchingMapView(): void {
    this.service.getUAVs().subscribe((data: Uavs) => {
      console.log('Fetched UAV data:', data); // debug
      // currently backend always sends just one object, so lets make it an array
      this.uavs = Array.isArray(data) ? data : [data];
      // this.uavs = data;
      this.updateMapMarkers();
    });
  }

  private updateMapMarkers(): void {
    if (this.map && Array.isArray(this.uavs)) {
      // remove old markers
      this.markers.forEach((marker) => this.map!.removeLayer(marker));
      this.markers = [];

      // add new markers to the map
      this.uavs.forEach((uav: Uav) => {
        const marker = L.marker(
          [parseFloat(uav.latitude), parseFloat(uav.longitude)],
          { icon: this.uavIcon }
        ).addTo(this.map!);
        marker
          .bindPopup(
            `ID: ${uav.id}<br>Latitude: ${uav.latitude}<br>Longitude: ${uav.longitude}`
          )
          .openPopup();
        this.markers.push(marker);
      });
    } else {
      console.log('Map or UAVs data is not available'); // Debug log
    }
  }
}
