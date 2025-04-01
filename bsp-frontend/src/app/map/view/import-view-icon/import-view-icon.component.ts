import { Component } from '@angular/core';
import {MatDialog} from '@angular/material/dialog';
import {AboutDialogViewComponent} from '../about-dialog-view/about-dialog-view.component';

@Component({
  selector: 'app-import-view-icon',
  imports: [],
  templateUrl: './import-view-icon.component.html',
  styleUrl: './import-view-icon.component.css'
})
export class ImportViewIconComponent {
  constructor(public dialog: MatDialog) {}

  openDialog(): void {
    const dialogRef = this.dialog.open(AboutDialogViewComponent, {
      width: '300px',
    });
  }
}
