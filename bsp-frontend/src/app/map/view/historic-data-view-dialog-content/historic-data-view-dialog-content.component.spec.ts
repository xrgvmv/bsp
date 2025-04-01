import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HistoricDataViewDialogContentComponent } from './historic-data-view-dialog-content.component';

describe('HistoricDataViewDialogContentComponent', () => {
  let component: HistoricDataViewDialogContentComponent;
  let fixture: ComponentFixture<HistoricDataViewDialogContentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HistoricDataViewDialogContentComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(HistoricDataViewDialogContentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
