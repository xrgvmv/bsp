import { Component } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { AboutDialogViewComponent } from '../about-dialog-view/about-dialog-view.component';

@Component({
  selector: 'app-about-view',
  imports: [],
  templateUrl: './about-view.component.html',
  styleUrl: './about-view.component.css',
})
export class AboutViewComponent {
  constructor(public dialog: MatDialog) {}

  // currently about view
  openDialog(): void {
    const dialogRef = this.dialog.open(AboutDialogViewComponent, {
      width: '300px',
    });

    // dialogRef.afterClosed().subscribe((result) => {
    //   console.log('Zamknieto okno dialogowe "o nas"');
    // });
  }
}
