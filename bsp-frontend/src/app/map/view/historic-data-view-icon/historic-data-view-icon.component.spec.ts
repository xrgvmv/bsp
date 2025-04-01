import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HistoricDataViewIconComponent } from './historic-data-view-icon.component';

describe('HistoricDataViewIconComponent', () => {
  let component: HistoricDataViewIconComponent;
  let fixture: ComponentFixture<HistoricDataViewIconComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HistoricDataViewIconComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(HistoricDataViewIconComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
