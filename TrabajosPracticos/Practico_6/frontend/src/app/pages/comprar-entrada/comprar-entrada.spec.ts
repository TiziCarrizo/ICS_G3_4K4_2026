import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { ComprarEntrada } from './comprar-entrada';
import { TiposPaseDb } from '../../services/tipos-pase/tipos-pase-db';
import { FormasPagoDb } from '../../services/formas-pago/formas-pago-db';

describe('ComprarEntrada', () => {
  let component: ComprarEntrada;
  let fixture: ComponentFixture<ComprarEntrada>;
  let httpMock: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ComprarEntrada, ReactiveFormsModule, HttpClientTestingModule, RouterTestingModule],
      providers: [TiposPaseDb, FormasPagoDb],
    }).compileComponents();

    fixture = TestBed.createComponent(ComprarEntrada);
    component = fixture.componentInstance;
    httpMock = TestBed.inject(HttpTestingController);
    await fixture.whenStable();
  });

  afterEach(() => httpMock.verify());

  // ── Creación ──────────────────────────────────────────────────────────────

  it('debería crearse correctamente', () => {
    expect(component).toBeTruthy();
  });

  it('debería inicializar el formulario con campos vacíos', () => {
    expect(component.form.get('fechaVisita')?.value).toBe('');
    expect(component.form.get('cantidadEntradas')?.value).toBeNull();
    expect(component.form.get('formaPago')?.value).toBe('');
    expect(component.visitantes.length).toBe(0);
  });

  // ── Validación: fechaVisita ───────────────────────────────────────────────

  it('debería marcar fechaVisita como inválida si está vacía', () => {
    component.form.get('fechaVisita')?.markAsTouched();
    expect(component.hasError('fechaVisita', 'required')).toBe(true);
  });

  it('debería rechazar una fecha pasada', () => {
    component.form.get('fechaVisita')?.setValue('2020-01-01');
    expect(component.hasError('fechaVisita', 'fechaPasada')).toBe(true);
  });

  it('debería rechazar el lunes como día de visita (parque cerrado)', () => {
    // Busca el próximo lunes a partir de hoy
    const date = new Date();
    date.setDate(date.getDate() + ((1 + 7 - date.getDay()) % 7 || 7));
    const lunes = date.toISOString().split('T')[0];
    component.form.get('fechaVisita')?.setValue(lunes);
    expect(component.hasError('fechaVisita', 'parqueCerrado')).toBe(true);
  });

  it('debería rechazar el 25 de diciembre como feriado', () => {
    const year = new Date().getFullYear() + 1; // año futuro para evitar fecha pasada
    component.form.get('fechaVisita')?.setValue(`${year}-12-25`);
    expect(component.hasError('fechaVisita', 'parqueCerrado')).toBe(true);
  });

  it('debería aceptar una fecha futura válida que no sea lunes ni feriado', () => {
    // Busca el próximo martes
    const date = new Date();
    date.setDate(date.getDate() + ((2 + 7 - date.getDay()) % 7 || 7));
    const martes = date.toISOString().split('T')[0];
    component.form.get('fechaVisita')?.setValue(martes);
    expect(component.form.get('fechaVisita')?.valid).toBe(true);
  });

  // ── Validación: cantidadEntradas ─────────────────────────────────────────

  it('debería rechazar cantidad de entradas vacía', () => {
    component.form.get('cantidadEntradas')?.markAsTouched();
    expect(component.isInvalid('cantidadEntradas')).toBe(true);
  });

  it('debería rechazar cantidad de entradas mayor a 10', () => {
    component.form.get('cantidadEntradas')?.setValue(11);
    component.form.get('cantidadEntradas')?.markAsTouched();
    expect(component.hasError('cantidadEntradas', 'max')).toBe(true);
  });

  it('debería rechazar cantidad de entradas menor a 1', () => {
    component.form.get('cantidadEntradas')?.setValue(0);
    component.form.get('cantidadEntradas')?.markAsTouched();
    expect(component.hasError('cantidadEntradas', 'min')).toBe(true);
  });

  // ── Visitantes ────────────────────────────────────────────────────────────

  it('debería agregar visitantes al cambiar la cantidad de entradas', () => {
    component.form.get('cantidadEntradas')?.setValue(3);
    component.actualizarVisitantes();
    expect(component.visitantes.length).toBe(3);
  });

  it('debería eliminar visitantes si se reduce la cantidad de entradas', () => {
    component.form.get('cantidadEntradas')?.setValue(3);
    component.actualizarVisitantes();
    component.form.get('cantidadEntradas')?.setValue(1);
    component.actualizarVisitantes();
    expect(component.visitantes.length).toBe(1);
  });

  it('debería limitar a 10 visitantes aunque se ingrese un número mayor', () => {
    component.form.get('cantidadEntradas')?.setValue(99);
    component.actualizarVisitantes();
    expect(component.visitantes.length).toBe(10);
  });

  it('debería marcar visitante como inválido si la edad está vacía', () => {
    component.form.get('cantidadEntradas')?.setValue(1);
    component.actualizarVisitantes();
    component.edadCtrl(0)?.markAsTouched();
    expect(component.edadInvalid(0)).toBe(true);
  });

  it('debería marcar tipo de pase como inválido si no se seleccionó', () => {
    component.form.get('cantidadEntradas')?.setValue(1);
    component.actualizarVisitantes();
    component.paseCtrl(0)?.markAsTouched();
    expect(component.paseInvalid(0)).toBe(true);
  });

  // ── Validación: formaPago ─────────────────────────────────────────────────

  it('debería marcar formaPago como inválido si está vacío', () => {
    component.form.get('formaPago')?.markAsTouched();
    expect(component.isInvalid('formaPago')).toBe(true);
  });

  // ── Submit ────────────────────────────────────────────────────────────────

  it('no debería enviar si el formulario es inválido', async () => {
    await component.submitForm();
    httpMock.expectNone('http://127.0.0.1:8000/api/compras/');
  });

  it('debería mostrar el modal tras una compra exitosa', async () => {
    // Armar un formulario válido con 1 visitante
    const martes = (() => {
      const d = new Date();
      d.setDate(d.getDate() + ((2 + 7 - d.getDay()) % 7 || 7));
      return d.toISOString().split('T')[0];
    })();

    component.form.get('fechaVisita')?.setValue(martes);
    component.form.get('cantidadEntradas')?.setValue(1);
    component.actualizarVisitantes();
    component.visitantes.at(0).setValue({ edad: 25, tipoPase: 1 });
    component.form.get('formaPago')?.setValue(1);

    const submitPromise = component.submitForm();
    const req = httpMock.expectOne('http://127.0.0.1:8000/api/compras/');
    req.flush({});
    await submitPromise;

    expect(component.showModal).toBe(true);
  });

  it('debería mostrar error 400 con el mensaje del servidor', async () => {
    const martes = (() => {
      const d = new Date();
      d.setDate(d.getDate() + ((2 + 7 - d.getDay()) % 7 || 7));
      return d.toISOString().split('T')[0];
    })();

    component.form.get('fechaVisita')?.setValue(martes);
    component.form.get('cantidadEntradas')?.setValue(1);
    component.actualizarVisitantes();
    component.visitantes.at(0).setValue({ edad: 25, tipoPase: 1 });
    component.form.get('formaPago')?.setValue(1);

    const submitPromise = component.submitForm();
    const req = httpMock.expectOne('http://127.0.0.1:8000/api/compras/');
    req.flush({ error: 'Fecha no disponible.' }, { status: 400, statusText: 'Bad Request' });
    await submitPromise;

    expect(component.submitError).toBe('Fecha no disponible.');
  });

  it('debería resetear el formulario y los visitantes tras compra exitosa', async () => {
    const martes = (() => {
      const d = new Date();
      d.setDate(d.getDate() + ((2 + 7 - d.getDay()) % 7 || 7));
      return d.toISOString().split('T')[0];
    })();

    component.form.get('fechaVisita')?.setValue(martes);
    component.form.get('cantidadEntradas')?.setValue(1);
    component.actualizarVisitantes();
    component.visitantes.at(0).setValue({ edad: 30, tipoPase: 2 });
    component.form.get('formaPago')?.setValue(2);

    const submitPromise = component.submitForm();
    const req = httpMock.expectOne('http://127.0.0.1:8000/api/compras/');
    req.flush({});
    await submitPromise;

    expect(component.visitantes.length).toBe(0);
    expect(component.form.get('fechaVisita')?.value).toBeNull();
  });

  // ── Modal ─────────────────────────────────────────────────────────────────

  it('debería cerrar el modal al llamar cerrarModal()', () => {
    component.showModal = true;
    component.cerrarModal();
    expect(component.showModal).toBe(false);
  });

  // ── Precios ───────────────────────────────────────────────────────────────

  it('debería calcular precio 0 para menores de 3 años', () => {
    const precio = (component as any).getPrecioUnitario('Regular', 2);
    expect(precio).toBe(0);
  });

  it('debería aplicar 50% de descuento a menores de 15 años', () => {
    const precio = (component as any).getPrecioUnitario('Regular', 10);
    expect(precio).toBe(5000);
  });

  it('debería aplicar 50% de descuento a mayores de 65 años', () => {
    const precio = (component as any).getPrecioUnitario('VIP', 70);
    expect(precio).toBe(10000);
  });

  it('debería cobrar precio completo a adultos entre 16 y 64 años', () => {
    const precio = (component as any).getPrecioUnitario('VIP', 30);
    expect(precio).toBe(20000);
  });
});