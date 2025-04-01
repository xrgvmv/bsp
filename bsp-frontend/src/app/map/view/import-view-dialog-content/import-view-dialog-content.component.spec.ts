import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ImportViewDialogContentComponent } from './import-view-dialog-content.component';

describe('ImportViewDialogContentComponent', () => {
  let component: ImportViewDialogContentComponent;
  let fixture: ComponentFixture<ImportViewDialogContentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ImportViewDialogContentComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ImportViewDialogContentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
