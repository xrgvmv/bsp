import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ImportViewIconComponent } from './import-view-icon.component';

describe('ImportViewIconComponent', () => {
  let component: ImportViewIconComponent;
  let fixture: ComponentFixture<ImportViewIconComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ImportViewIconComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ImportViewIconComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
