import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import {MapViewComponent} from './map/view/map-view/map-view.component';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, MapViewComponent, MapViewComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'bsp-frontend';
}
