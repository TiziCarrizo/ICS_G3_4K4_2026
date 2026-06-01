import { Component } from '@angular/core';
import { AbstractControl, FormArray, FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { NgClass } from '@angular/common';
import { TipoEntrada, TiposPaseDb } from '../../services/tipos-pase/tipos-pase-db';
import { Router } from '@angular/router';
import { IntRangeDirective } from '../../directives/int-range.directive';
import { FormaPago, FormasPagoDb } from '../../services/formas-pago/formas-pago-db';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';
import { MOCK_USER } from '../../app';



@Component({
  selector: 'app-comprar-entrada',
  standalone: true, // standalone true porque no tiene rutas hijas
  imports: [ReactiveFormsModule, NgClass, IntRangeDirective],
  templateUrl: './comprar-entrada.html',
  styleUrl: './comprar-entrada.scss',
})
export class ComprarEntrada {

  form: FormGroup;
    hoyISO: string = new Date().toISOString().split('T')[0];
    tiposPase: TipoEntrada[] = [
        { id: 1, nombre: 'VIP' },
        { id: 2, nombre: 'Regular' }
    ];
    formasPago: FormaPago[] = [
        { id: 1, nombre: 'EFECTIVO' },
        { id: 2, nombre: 'TARJETA' }
    ];
    isSubmitting = false;
    submitError = '';
    submitSuccess = '';
    private apiBaseUrl = 'http://127.0.0.1:8000';
    showModal = false;
    modalData = { cantidad: 0, fecha: '', total: 0 };
    mockUser = MOCK_USER;
  // Aquí puedes definir las propiedades y método necesarios para tu componente
  constructor(
        private fb: FormBuilder,
        private tiposPaseDb: TiposPaseDb,
        private formasPagoDb: FormasPagoDb,
        private httpClient: HttpClient,
        private router: Router
    ) {
        this.form = this.buildForm();
    }

        ngOnInit() {
            return;
        }

    private async loadTiposPase() {
      return;
    }
    
     private async loadFormasPago() {
      return;
    }

    buildForm(): FormGroup {
          return this.fb.group({
              fechaVisita: ['', [Validators.required, this.fechaValida.bind(this)]],
              cantidadEntradas: [
                  null,
                  [Validators.required, Validators.min(1), Validators.max(10), Validators.pattern('^[0-9]+$')]
              ],
              visitantes: this.fb.array([], this.visitantesCoinciden.bind(this)),
              formaPago: ['', Validators.required]
          });
      }

    get visitantes(): FormArray {
          return this.form.get('visitantes') as FormArray;
      }

    // Método para manejar el envío del formulario
        // Reemplazá el submitForm() completo
    async submitForm() {
        if (this.form.invalid) {
            this.form.markAllAsTouched();
            return;
        }

        this.isSubmitting = true;
        this.submitError = '';

        const payload = this.buildCompraPayload();

        try {
            const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
            await firstValueFrom(
                this.httpClient.post(`${this.apiBaseUrl}/api/compras/`, payload, { headers })
            );

            this.modalData = {
                cantidad: this.visitantes.length,
                fecha: this.form.get('fechaVisita')?.value,
                total: this.visitantes.controls.reduce((acc, ctrl) => {
                    const tipoPaseNombre = this.getTipoPaseNombre(Number(ctrl.get('tipoPase')?.value));
                    const edad = Number(ctrl.get('edad')?.value);
                    return acc + this.getPrecioUnitario(tipoPaseNombre, edad);
                }, 0)
            };

            this.showModal = true;
            this.form.reset();
            this.visitantes.clear();

        } catch (error) {
            await this.handleSubmitError(error);
        } finally {
            this.isSubmitting = false;
        }
    }

        cerrarModal() {
            this.showModal = false;
        }

        private buildCompraPayload() {
            const fecha = this.form.get('fechaVisita')?.value as string;
            const formaPagoId = this.form.get('formaPago')?.value as number;
            const formaPagoNombre = this.getFormaPagoNombre(formaPagoId);
            const entradas = this.visitantes.controls.map((ctrl) => {
                const edad = Number(ctrl.get('edad')?.value);
                const tipoPaseId = Number(ctrl.get('tipoPase')?.value);
                const tipoPaseNombre = this.getTipoPaseNombre(tipoPaseId);

                return {
                    edad,
                    tipo_pase: tipoPaseNombre,
                    precio_unitario: this.getPrecioUnitario(tipoPaseNombre, edad)
                };
            });

            const payload = {
                usuario: {
                    id: MOCK_USER.id,
                    nombre: `${MOCK_USER.nombre} ${MOCK_USER.apellido}`
                },
                fecha,
                forma_pago: formaPagoNombre,
                entradas
            };

            console.log('Payload enviado:', JSON.stringify(payload, null, 2)); // ← nuevo
            return payload;
        }

        private getTipoPaseNombre(id: number): string {
            return this.tiposPase.find((tp) => tp.id === Number(id))?.nombre ?? '';
        }

        private getFormaPagoNombre(id: number): string {
            return this.formasPago.find((fp) => fp.id === Number(id))?.nombre ?? '';
        }

        private getPrecioUnitario(tipoPaseNombre: string, edad: number): number {
            const priceMap: Record<string, number> = {
                VIP: 20000.0,
                Regular: 10000.0
            };
            
            const base = priceMap[tipoPaseNombre] ?? 0.0;

            // Aplicar descuentos
            // Menores o igual a 3 años
            if (edad <= 3) return 0.0;
            // Menores o iguales a 15 años
            if (edad <= 15) return base * 0.5;
            // Mayores o iguales a 65 años
            if (edad >= 65) return base * 0.5;
            return base;
        }

        private async handleSubmitError(error: unknown) {
            if (!(error instanceof HttpErrorResponse)) {
                this.submitError = 'Lo sentimos, intente mas tarde.';
                return;
            }

            if (error.status === 400) {
                this.submitError = error.error?.error ?? 'Error de validacion en la compra.';
                return;
            }

            if (error.status === 404) {
                this.submitError = error.error?.error ?? 'Dato parametrico no encontrado en la base de datos.';
                await this.loadTiposPase();
                await this.loadFormasPago();
                return;
            }

            if (error.status === 500) {
                this.submitError = 'Lo sentimos, intente mas tarde.';
                return;
            }

            this.submitError = 'No se pudo procesar la compra.';
        }

    fechaValida(control: AbstractControl) { // abstractControl permite validar el control específico al que se le asigna esta función de validación
      const fechaSeleccionada = new Date(control.value + 'T00:00:00'); // Convertir a Date, asumiendo que el valor es una fecha sin hora
      const hoy = new Date();
      hoy.setHours(0, 0, 0, 0); // Establecer la hora a 00:00:00 para comparar solo fechas
      
      // Validar que la fecha seleccionada no sea anterior a hoy
      if (fechaSeleccionada < hoy) {
            return { fechaPasada: true }; // Retorna un error de validación si la fecha es anterior a hoy
          }

      // Validar que no sea domingo (1 = Monday, ...)
      if (fechaSeleccionada.getDay() === 1) return { parqueCerrado: true };
          
      // Validar que no sea feriado
      const month = fechaSeleccionada.getMonth() + 1; // getMonth() 0-11
      const day = fechaSeleccionada.getDate(); // empieza en 0

      if ((month === 12 && day === 25) || (month === 1 && day === 1)) {
          return { parqueCerrado: true };
      }
      
      return null; // Retorna null si la fecha es válida
    }

    control(name: string) {
      return this.form.get(name);
    }

    isInvalid(name: string) {
      const c = this.control(name);
      return !!c && c.invalid && (c.touched || c.dirty);
    }

    hasError(name: string, err: string) {
      const c = this.control(name);
      return !!c?.errors?.[err];
    }

    actualizarVisitantes() {
        const cantidad = this.form.get('cantidadEntradas')?.value || 0;
        const finalCantidad = Math.min(cantidad, 10);

        // Agregar los que faltan
        while (this.visitantes.length < finalCantidad) {
            this.visitantes.push(
            this.fb.group({
                edad: ['', [Validators.required, Validators.pattern('^[0-9]+$'), Validators.min(0), Validators.max(99)]],
                tipoPase: ['', Validators.required]
            })
            );
        }

        // Eliminar los que sobran
        while (this.visitantes.length > finalCantidad) {
            this.visitantes.removeAt(this.visitantes.length - 1);
        }
    }
    visitantesCoinciden(control: AbstractControl) {
          const cantidadEntradas = this.form?.get('cantidadEntradas')?.value || 0;
          const visitantes = (control as FormArray).controls || [];
          if (cantidadEntradas !== visitantes.length) return { visitantesNoCoinciden: true };
          return null;
      }

      edadCtrl(i: number) {
          return (this.visitantes.at(i) as FormGroup).get('edad');
      }
      paseCtrl(i: number) {
          return (this.visitantes.at(i) as FormGroup).get('tipoPase');
      }
      edadInvalid(i: number) {
          const c = this.edadCtrl(i);
          return c?.invalid && (c?.touched || c?.dirty);
      }
      edadHasError(i: number, err: string) {
          return !!this.edadCtrl(i)?.errors?.[err];
      }

      paseInvalid(i: number) {
          const c = this.paseCtrl(i);
          return c?.invalid && (c?.touched || c?.dirty);
      }
  }