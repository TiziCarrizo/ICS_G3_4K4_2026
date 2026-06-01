import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MainLayout } from './main-layout';
import { MOCK_USER } from '../../app';

import { provideRouter } from '@angular/router';
import { provideLocationMocks } from '@angular/common/testing';

describe('MainLayout', () => {
  let component: MainLayout;
  let fixture: ComponentFixture<MainLayout>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MainLayout],
      providers: [
        provideRouter([]),
        provideLocationMocks(),
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(MainLayout);
    component = fixture.componentInstance;
    await fixture.whenStable();
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('deberia mostrar el logo EcoHarmony Park', () => {
    const compiled = fixture.nativeElement as HTMLElement;
    const logo = compiled.querySelector('header h1 img[alt="EcoHarmony Park"]');

    expect(logo).toBeTruthy();
  });
});