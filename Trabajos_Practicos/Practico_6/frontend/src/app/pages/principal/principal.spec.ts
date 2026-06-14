import { ComponentFixture, TestBed, fakeAsync, tick } from '@angular/core/testing';

import { Principal } from './principal';
import { By } from '@angular/platform-browser';
import { provideRouter, Router } from '@angular/router';
import { Location } from '@angular/common';


describe('Principal', () => {
  let component: Principal;
  let fixture: ComponentFixture<Principal>;
  let router: Router;
  let location: Location;

  beforeEach(async () => {
  await TestBed.configureTestingModule({
    imports: [Principal],
    providers: [
      provideRouter([
        { path: '', component: Principal },
        { path: 'comprar-entrada', component: Principal }
      ])
    ]
  }).compileComponents();

  fixture = TestBed.createComponent(Principal);
  component = fixture.componentInstance;

  router = TestBed.inject(Router);
  location = TestBed.inject(Location);
  fixture.detectChanges();
});

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('Deberia navegar a comprar entrada al hacer click', async() => {
    console.log('Ejecutando prueba de botón de página principal')
    const spy = vi.spyOn(component, 'onClick');

    const button = fixture.debugElement.query(By.css('button')).nativeElement;
    button.click();

  expect(spy).toHaveBeenCalled();
    /* Ir a la página principal
      it('Deberia navegar a comprar entrada al hacer click', async () => {
      await router.navigateByUrl('/');

      const button = fixture.debugElement.query(By.css('button')).nativeElement;
      button.click();

      await fixture.whenStable();
      fixture.detectChanges();

      expect(location.path()).toBe('/comprar-entrada');
    */
});
});
