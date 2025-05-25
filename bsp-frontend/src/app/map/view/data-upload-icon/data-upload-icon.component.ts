import { Component, Input } from '@angular/core';
import {MatDialog} from '@angular/material/dialog';
import {DataUploadComponent} from '../data-upload/data-upload.component';
import {MapService} from '../../service/map.service';

@Component({
  selector: 'app-data-upload-icon',
  imports: [],
  templateUrl: './data-upload-icon.component.html',
  styleUrl: './data-upload-icon.component.css'
})

export class DataUploadIconComponent {
  @Input() service: MapService | undefined;
  @Input() map: L.Map | undefined;

  constructor(public dialog: MatDialog) {}

  openDialog(): void {
    const dialogRef = this.dialog.open(DataUploadComponent, {
      width: '80vw',
      maxWidth: '1200px',
      height: '80vh',
      data: {
        service: this.service,
        map: this.map,
      },
    });
  }
}
