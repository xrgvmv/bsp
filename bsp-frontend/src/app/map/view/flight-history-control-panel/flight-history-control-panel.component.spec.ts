import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FlightHistoryControlPanelComponent } from './flight-history-control-panel.component';

describe('FlightHistoryControlPanelComponent', () => {
  let component: FlightHistoryControlPanelComponent;
  let fixture: ComponentFixture<FlightHistoryControlPanelComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FlightHistoryControlPanelComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FlightHistoryControlPanelComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
