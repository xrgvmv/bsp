import { Component, Input } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MapService } from '../../service/map.service';
import { HistoricDataViewDialogContentComponent } from '../historic-data-view-dialog-content/historic-data-view-dialog-content.component';

@Component({
  selector: 'app-historic-data-view-icon',
  imports: [],
  templateUrl: './historic-data-view-icon.component.html',
  styleUrl: './historic-data-view-icon.component.css',
})
export class HistoricDataViewIconComponent {
  @Input() service: MapService | undefined;
  @Input() map: L.Map | undefined;

  constructor(public dialog: MatDialog) {}

  openDialog(): void {
    const dialogRef = this.dialog.open(HistoricDataViewDialogContentComponent, {
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
