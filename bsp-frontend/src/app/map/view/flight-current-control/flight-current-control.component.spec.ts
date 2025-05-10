import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FlightCurrentControlComponent } from './flight-current-control.component';

describe('FlightCurrentControlComponent', () => {
  let component: FlightCurrentControlComponent;
  let fixture: ComponentFixture<FlightCurrentControlComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FlightCurrentControlComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FlightCurrentControlComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
