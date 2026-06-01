import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ComprarEntrada } from './comprar-entrada';

describe('ComprarEntrada', () => {
  let component: ComprarEntrada;
  let fixture: ComponentFixture<ComprarEntrada>;
  let httpMock: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ComprarEntrada],
      providers: [provideHttpClient(), provideHttpClientTesting()],
    }).compileComponents();

    fixture = TestBed.createComponent(ComprarEntrada);
    component = fixture.componentInstance;
    httpMock = TestBed.inject(HttpTestingController);
    await fixture.whenStable();
  });

  afterEach(() => httpMock.verify());

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('deberia mostrar error si no se selecciona forma de pago', () => {
    component.fecha = '2026-06-10';
    component.formaPago = '';
    component.confirmarCompra();
    expect(component.error()).toBe('Completá todos los campos antes de continuar.');
  });

  it('deberia mostrar error si no se ingresa fecha', () => {
    component.fecha = '';
    component.formaPago = 'TARJETA';
    component.confirmarCompra();
    expect(component.error()).toBe('Completá todos los campos antes de continuar.');
  });

  it('deberia mostrar error si hay entradas sin edad', () => {
    component.fecha = '2026-06-10';
    component.formaPago = 'EFECTIVO';
    component.entradas = [{ edad: 0, tipo_pase: 'REGULAR', precio_unitario: 2500 }];
    component.confirmarCompra();
    expect(component.error()).toBe('Ingresá la edad de todos los visitantes.');
  });

  it('deberia llamar al backend con datos correctos y mostrar resultado', () => {
    component.fecha = '2026-06-10';
    component.formaPago = 'TARJETA';
    component.entradas = [{ edad: 25, tipo_pase: 'VIP', precio_unitario: 5000 }];

    component.confirmarCompra();

    const req = httpMock.expectOne('http://localhost:8000/api/comprar/');
    expect(req.request.method).toBe('POST');
    req.flush({ id: 1, cantidad_entradas: 1, fecha: '2026-06-10', monto_total: 5000, mercado_pago_redirect_url: 'https://mercadopago.com/checkout?pref_id=COMPRA-1' });

    expect(component.resultado()?.id).toBe(1);
    expect(component.resultado()?.mercado_pago_redirect_url).toBeTruthy();
  });

  it('deberia mostrar error cuando el backend devuelve 400', () => {
    component.fecha = '2026-06-10';
    component.formaPago = 'TARJETA';
    component.entradas = [{ edad: 25, tipo_pase: 'REGULAR', precio_unitario: 2500 }];

    component.confirmarCompra();

    const req = httpMock.expectOne('http://localhost:8000/api/comprar/');
    req.flush({ error: 'El parque está cerrado los lunes' }, { status: 400, statusText: 'Bad Request' });

    expect(component.error()).toBe('El parque está cerrado los lunes');
  });

  it('agregar entrada no debe superar 10', () => {
    for (let i = 0; i < 15; i++) component.agregarEntrada();
    expect(component.entradas.length).toBe(10);
  });

  it('quitar entrada no debe bajar de 1', () => {
    component.quitarEntrada(0);
    expect(component.entradas.length).toBe(1);
  });

  it('monto total debe sumar correctamente', () => {
    component.entradas = [
      { edad: 25, tipo_pase: 'VIP', precio_unitario: 5000 },
      { edad: 12, tipo_pase: 'REGULAR', precio_unitario: 2500 },
    ];
    expect(component.montoTotal).toBe(7500);
  });
});

