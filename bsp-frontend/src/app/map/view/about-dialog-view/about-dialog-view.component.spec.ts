import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AboutDialogViewComponent } from './about-dialog-view.component';

describe('AboutDialogViewComponent', () => {
  let component: AboutDialogViewComponent;
  let fixture: ComponentFixture<AboutDialogViewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AboutDialogViewComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AboutDialogViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
