import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { MisCompras } from './mis-compras';
import { MOCK_USER } from '../../app';
import { describe, it, expect, beforeEach, afterEach } from 'vitest';

describe('MisCompras', () => {
  let component: MisCompras;
  let fixture: ComponentFixture<MisCompras>;
  let httpMock: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MisCompras],
      providers: [
        provideRouter([]),
        // Proveedores necesarios para testear peticiones HTTP en componentes standalone
        provideHttpClient(),
        provideHttpClientTesting(),
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(MisCompras);
    component = fixture.componentInstance;
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    // Verificamos que no queden peticiones HTTP pendientes entre cada test
    httpMock.verify();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('debería mostrar "Cargando..." al iniciar el componente', () => {
    // Dispara la detección de cambios (ejecuta ngOnInit pero aún no resolvemos la petición HTTP)
    fixture.detectChanges(); 
    
    const compiled = fixture.nativeElement as HTMLElement;
    const estadoElement = compiled.querySelector('.estado');
    
    expect(estadoElement).toBeTruthy();
    expect(estadoElement?.textContent).toContain('Cargando...');

    // Limpiamos la petición pendiente para que afterEach no falle
    const req = httpMock.expectOne(`http://127.0.0.1:8000/api/mis-compras/?usuario_id=${MOCK_USER.id}`);
    req.flush({ compras: [] });
  });

  it('debería mostrar mensaje de lista vacía si el usuario no tiene compras', () => {
    fixture.detectChanges(); // Ejecuta ngOnInit

    // Interceptamos la petición
    const req = httpMock.expectOne(`http://127.0.0.1:8000/api/mis-compras/?usuario_id=${MOCK_USER.id}`);
    expect(req.request.method).toBe('GET');
    
    // Simulamos una respuesta exitosa pero sin compras
    req.flush({ compras: [] }); 

    fixture.detectChanges(); // Actualizamos la vista con los nuevos datos

    const compiled = fixture.nativeElement as HTMLElement;
    const estadoVacio = compiled.querySelector('.estado.vacio');
    
    expect(estadoVacio).toBeTruthy();
    expect(estadoVacio?.textContent).toContain('Todavía no tenés compras registradas.');
  });

  it('debería renderizar la lista de compras cuando la API responde con datos', () => {
    fixture.detectChanges(); 

    const mockCompras = [
      {
        id: 101,
        fecha: '2026-06-05',
        fecha_compra: '2026-06-02',
        cantidad_entradas: 2,
        monto_total: 5000,
        forma_pago: 'TARJETA',
        mercado_pago_redirect_url: null,
        entradas: [
          { edad: 25, tipo: 'Adulto', precio_unitario: 2500 },
          { edad: 28, tipo: 'Adulto', precio_unitario: 2500 }
        ]
      }
    ];

    const req = httpMock.expectOne(`http://127.0.0.1:8000/api/mis-compras/?usuario_id=${MOCK_USER.id}`);
    // Simulamos que la API devuelve un array con una compra
    req.flush({ compras: mockCompras });

    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;
    const cards = compiled.querySelectorAll('.compra-card');
    
    // Verificamos que se renderice la tarjeta y contenga los datos correctos
    expect(cards.length).toBe(1);
    expect(compiled.querySelector('.compra-id')?.textContent).toContain('#101');
    expect(compiled.querySelector('.forma-pago')?.textContent).toContain('Tarjeta (MP)');
    
    // Verificamos que se rendericen los chips de las entradas
    const entradaChips = compiled.querySelectorAll('.entrada-chip');
    expect(entradaChips.length).toBe(2);
  });

  it('debería mostrar un mensaje de error si falla la petición HTTP', () => {
    fixture.detectChanges(); 

    const req = httpMock.expectOne(`http://127.0.0.1:8000/api/mis-compras/?usuario_id=${MOCK_USER.id}`);
    
    // Simulamos un error de red o de servidor
    req.error(new ProgressEvent('Network error'));

    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;
    const estadoError = compiled.querySelector('.estado.error');
    
    expect(estadoError).toBeTruthy();
    expect(estadoError?.textContent).toContain('No se pudieron cargar tus compras. Intentá de nuevo más tarde.');
  });
});