import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UavsListViewComponent } from './uavs-list-view.component';

describe('UavsListViewComponent', () => {
  let component: UavsListViewComponent;
  let fixture: ComponentFixture<UavsListViewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UavsListViewComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UavsListViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
