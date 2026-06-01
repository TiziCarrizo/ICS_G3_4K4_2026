import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MercadoPago } from './mercado-pago';

describe('MercadoPago', () => {
  let component: MercadoPago;
  let fixture: ComponentFixture<MercadoPago>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MercadoPago],
    }).compileComponents();

    fixture = TestBed.createComponent(MercadoPago);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
