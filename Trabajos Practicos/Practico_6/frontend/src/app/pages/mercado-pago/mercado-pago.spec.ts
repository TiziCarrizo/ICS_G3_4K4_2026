import { ComponentFixture, TestBed } from '@angular/core/testing';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { of, throwError } from 'rxjs';
import { vi, describe, it, expect, beforeEach, afterEach } from 'vitest';
import { MercadoPago } from './mercado-pago';

describe('MercadoPago', () => {
  let component: MercadoPago;
  let fixture: ComponentFixture<MercadoPago>;
  let navigateMock: ReturnType<typeof vi.fn>;
  let postMock: ReturnType<typeof vi.fn>;

  const mockPayload = {
    usuario: { id: 1, nombre: 'Test User' },
    fecha: '2025-12-01',
    forma_pago: 'TARJETA',
    entradas: [{ edad: 25, tipo_pase: 'Regular', precio_unitario: 10000 }]
  };

  const mockModalData = { cantidad: 1, fecha: '2025-12-01', total: 10000 };

  beforeEach(async () => {
    navigateMock = vi.fn();
    postMock = vi.fn().mockReturnValue(of({}));

    const routerStub = {
      navigate: navigateMock,
      getCurrentNavigation: () => ({
        extras: { state: { payload: mockPayload, modalData: mockModalData } }
      })
    };

    await TestBed.configureTestingModule({
      imports: [MercadoPago, CommonModule, FormsModule],
      providers: [
        { provide: Router, useValue: routerStub },
        { provide: HttpClient, useValue: { post: postMock } }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(MercadoPago);
    component = fixture.componentInstance;
    fixture.detectChanges();
    await fixture.whenStable();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  // ── Creación ──────────────────────────────────────────────────────────────

  it('debería crearse correctamente', () => {
    expect(component).toBeTruthy();
  });

  // ── Valores iniciales ─────────────────────────────────────────────────────

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

  it('debería tener procesando en false inicialmente', () => {
    expect(component.procesando).toBe(false);
  });

  it('debería tener pagoExitoso en false inicialmente', () => {
    expect(component.pagoExitoso).toBe(false);
  });

  // ── Estado durante el pago ────────────────────────────────────────────────

  it('debería poner procesando en true al llamar pagar()', () => {
    vi.useFakeTimers();
    component.pagar();
    expect(component.procesando).toBe(true);
  });

  it('debería llamar al endpoint correcto con el payload', () => {
    vi.useFakeTimers();
    component.pagar();
    expect(postMock).toHaveBeenCalledWith(
      'http://127.0.0.1:8000/api/compras/',
      mockPayload,
      expect.any(Object)
    );
  });

  // ── Pago exitoso ──────────────────────────────────────────────────────────

  it('debería mostrar pagoExitoso tras 500ms', async () => {
    vi.useFakeTimers();
    component.pagar();
    await vi.advanceTimersByTimeAsync(500);
    expect(component.pagoExitoso).toBe(true);
  });

  it('debería deshabilitar el botón mientras está procesando', () => {
    vi.useFakeTimers();
    component.pagar();
    fixture.detectChanges();
    const btn = fixture.nativeElement.querySelector('.btn-pagar');
    expect(btn.disabled).toBe(true);
  });

  it('debería navegar a /comprar-entrada con mostrarModal tras el pago', async () => {
    vi.useFakeTimers();
    component.pagar();
    await vi.advanceTimersByTimeAsync(1000);
    expect(navigateMock).toHaveBeenCalledWith(
      ['/comprar-entrada'],
      { state: { mostrarModal: true, modalData: mockModalData } }
    );
  });

  // ── Manejo de errores ─────────────────────────────────────────────────────

  it('debería restaurar procesando a false si el servidor responde con error', () => {
    postMock.mockReturnValue(throwError(() => new Error('server error')));
    vi.spyOn(window, 'alert').mockImplementation(() => {});
    component.pagar();
    expect(component.procesando).toBe(false);
  });

  it('debería mostrar alerta si el servidor responde con error', () => {
    postMock.mockReturnValue(throwError(() => new Error('server error')));
    const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => {});
    component.pagar();
    expect(alertSpy).toHaveBeenCalledWith('Error al procesar el pago. Intentá de nuevo.');
  });

  it('no debería navegar si el servidor responde con error', () => {
    postMock.mockReturnValue(throwError(() => new Error('server error')));
    vi.spyOn(window, 'alert').mockImplementation(() => {});
    component.pagar();
    expect(navigateMock).not.toHaveBeenCalled();
  });

  // ── Validación de campos ──────────────────────────────────────────────────

  it('debería mostrar alerta si el número de tarjeta es incorrecto', () => {
    const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => {});
    component.numeroTarjeta = '123';
    component.pagar();
    expect(alertSpy).toHaveBeenCalledWith('Completá correctamente todos los campos');
    expect(postMock).not.toHaveBeenCalled();
  });

  it('debería mostrar alerta si el titular es muy corto', () => {
    const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => {});
    component.titular = 'AB';
    component.pagar();
    expect(alertSpy).toHaveBeenCalledWith('Completá correctamente todos los campos');
    expect(postMock).not.toHaveBeenCalled();
  });

  it('debería mostrar alerta si el vencimiento tiene formato incorrecto', () => {
    const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => {});
    component.vencimiento = '1230';
    component.pagar();
    expect(alertSpy).toHaveBeenCalledWith('Completá correctamente todos los campos');
    expect(postMock).not.toHaveBeenCalled();
  });

  it('debería mostrar alerta si el CVV es incorrecto', () => {
    const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => {});
    component.cvv = '12';
    component.pagar();
    expect(alertSpy).toHaveBeenCalledWith('Completá correctamente todos los campos');
    expect(postMock).not.toHaveBeenCalled();
  });

  // ── formatearVencimiento ──────────────────────────────────────────────────

  it('debería formatear el vencimiento con barra al superar 2 dígitos', () => {
    component.vencimiento = '1230';
    component.formatearVencimiento();
    expect(component.vencimiento).toBe('12/30');
  });

  it('no debería modificar el vencimiento si tiene menos de 3 dígitos', () => {
    component.vencimiento = '12';
    component.formatearVencimiento();
    expect(component.vencimiento).toBe('12');
  });

  it('debería eliminar caracteres no numéricos del vencimiento', () => {
    component.vencimiento = '12/ab';
    component.formatearVencimiento();
    expect(component.vencimiento).toBe('12');
  });

  // ── Template ──────────────────────────────────────────────────────────────

  it('debería mostrar el texto "Pagar" cuando no está procesando', () => {
    const btn = fixture.nativeElement.querySelector('.btn-pagar');
    expect(btn.textContent).toContain('Pagar');
  });

  it('no debería mostrar el mensaje de éxito antes del pago', () => {
    const exito = fixture.nativeElement.querySelector('.mensaje-exito');
    expect(exito).toBeNull();
  });

  it('debería mostrar el mensaje de éxito en el DOM tras pagoExitoso', async () => {
    component.pagoExitoso = true;
    component.procesando = false;
    fixture.detectChanges();
    const exito = fixture.nativeElement.querySelector('.mensaje-exito');
    expect(exito).not.toBeNull();
  });
  it('debería tener todos los inputs deshabilitados', () => {
    const inputs = fixture.nativeElement.querySelectorAll('input');
    inputs.forEach((input: HTMLInputElement) => {
      expect(input.disabled).toBe(true);
    });
  });

  it('debería mostrar el texto "Procesando pago..." mientras procesa', () => {
    vi.useFakeTimers();
    component.pagar();
    fixture.detectChanges();
    const btn = fixture.nativeElement.querySelector('.btn-pagar');
    expect(btn.textContent).toContain('Procesando pago...');
  });
});