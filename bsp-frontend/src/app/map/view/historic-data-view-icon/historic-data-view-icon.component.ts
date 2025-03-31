import { Component } from '@angular/core';
import {MatDialog} from '@angular/material/dialog';
import {
  HistoricDataViewDialogContentComponent
} from '../historic-data-view-dialog-content/historic-data-view-dialog-content.component';

@Component({
  selector: 'app-historic-data-view-icon',
  imports: [],
  templateUrl: './historic-data-view-icon.component.html',
  styleUrl: './historic-data-view-icon.component.css'
})
export class HistoricDataViewIconComponent {
  constructor(public dialog: MatDialog) {}

  // currently about view
  openDialog(): void {
    const dialogRef = this.dialog.open(HistoricDataViewDialogContentComponent, {
      width: '600px',
    });
  }
}
