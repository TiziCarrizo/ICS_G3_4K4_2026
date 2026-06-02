import { ComponentFixture, TestBed } from '@angular/core/testing';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { MercadoPago } from './mercado-pago';
import { PagoTemporalService } from '../../services/formas-pago/pago-temporal.service';

describe('MercadoPago', () => {
  let component: MercadoPago;
  let fixture: ComponentFixture<MercadoPago>;
  let navigateSpy: any;
  let pagoTemporalStub: { compraPendiente: null };

  beforeEach(async () => {
    navigateSpy = { calls: [] as any[] };
    const routerStub = {
      navigate: (...args: any[]) => { navigateSpy.calls.push(args); }
    };
    pagoTemporalStub = { compraPendiente: null };
    const httpStub = { post: () => {} };

    await TestBed.configureTestingModule({
      imports: [MercadoPago, CommonModule, FormsModule],
      providers: [
        { provide: Router, useValue: routerStub },
        { provide: PagoTemporalService, useValue: pagoTemporalStub },
        { provide: HttpClient, useValue: httpStub }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(MercadoPago);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  // ── Creación ──────────────────────────────────────────────────────────────

  it('debería crearse correctamente', () => {
    expect(component).toBeTruthy();
  });

  // ── Valores mockeados iniciales ───────────────────────────────────────────

  it('debería tener el número de tarjeta pre-cargado', () => {
    expect(component.numeroTarjeta).toBe('4509953566233704');
  });

  it('debería tener el titular pre-cargado', () => {
    expect(component.titular).toBe('Manuel Dávila');
  });

  it('debería tener el vencimiento pre-cargado', () => {
    expect(component.vencimiento).toBe('12/30');
  });

  it('debería tener el CVV pre-cargado', () => {
    expect(component.cvv).toBe('123');
  });

  it('debería navegar a /mis-compras después de 5 segundos', (done: Function) => {
    component.pagar();
    setTimeout(() => {
      expect(navigateSpy.calls[0][0]).toEqual(['/mis-compras']);
      done();
    }, 5100);
  });

  // ── Template ──────────────────────────────────────────────────────────────

  it('debería mostrar el texto "Pagar" cuando no está procesando', () => {
    fixture.detectChanges();
    const btn = fixture.nativeElement.querySelector('.btn-pagar');
    expect(btn.textContent).toContain('Pagar');
  });

  it('debería deshabilitar el botón mientras está procesando', (done: Function) => {
    component.pagar();
    fixture.detectChanges();
    const btn = fixture.nativeElement.querySelector('.btn-pagar');
    expect(btn.disabled).toBe(true);
    setTimeout(() => done(), 5100);
  });

  it('no debería mostrar el mensaje de éxito antes del pago', () => {
    fixture.detectChanges();
    const exito = fixture.nativeElement.querySelector('.mensaje-exito');
    expect(exito).toBeNull();
  });

  it('debería tener todos los inputs deshabilitados', () => {
    fixture.detectChanges();
    const inputs = fixture.nativeElement.querySelectorAll('input');
    inputs.forEach((input: HTMLInputElement) => {
      expect(input.disabled).toBe(true);
    });
  });
});