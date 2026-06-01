import { Component, OnInit, computed, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { PagoTemporalService } from '../../services/formas-pago/pago-temporal.service';import {
  CompraService,
  EntradaItem,
  CompraResponse,
  UsuarioApi,
  CompraRequest
} from '../../services/compra.service';

@Component({
  selector: 'app-comprar-entrada',
  imports: [FormsModule, CommonModule],
  templateUrl: './comprar-entrada.html',
  styleUrl: './comprar-entrada.scss',
})

export class ComprarEntrada implements OnInit {
  usuarios = signal<UsuarioApi[]>([]);
  usuarioId = signal<number | null>(null);
  usuarioSeleccionado = signal<UsuarioApi | null>(null);
  emailConfirmacion = signal('');

  fecha = signal('');
  formaPago = signal<'TARJETA' | 'EFECTIVO' | ''>('');
  entradas = signal<EntradaItem[]>([{ edad: 0, tipo_pase: 'REGULAR', precio_unitario: 0 }]);

  cargando = signal(false);
  error = signal('');
  resultado = signal<CompraResponse | null>(null);

  readonly PRECIO_VIP = 20000;
  readonly PRECIO_REGULAR = 10000;

  calcularPrecio(edad: number, tipo_pase: 'VIP' | 'REGULAR'): number {
    const base = tipo_pase === 'VIP' ? this.PRECIO_VIP : this.PRECIO_REGULAR;
    if (edad <= 3) return 0;
    if (edad <= 15 || edad >= 60) return base * 0.5;
    return base;
  }

  descuentoLabel(edad: number): string {
    if (edad <= 3) return '(gratis)';
    if (edad <= 15) return '(50% off - menor de 16)';
    if (edad >= 60) return '(50% off - mayor de 59)';
    return '';
  }

  montoTotal = computed(() => this.entradas().reduce((sum, e) => sum + e.precio_unitario, 0));

  constructor(
  private compraService: CompraService,
  private pagoTemporalService: PagoTemporalService,
  private router: Router
) {}

  ngOnInit() {
    this.compraService.getUsuarios().subscribe({
      next: (usuarios) => {
        this.usuarios.set(usuarios);
        if (usuarios.length > 0) {
          this.usuarioSeleccionado.set(usuarios[0]);
          this.usuarioId.set(usuarios[0].id);
          this.compraService.usuarioActivo.set(usuarios[0]);
          this.emailConfirmacion.set(usuarios[0].email);
        }
      },
      error: () => this.error.set('No se pudieron cargar los usuarios.')
    });
  }

  onUsuarioChange(id: number) {
    const found = this.usuarios().find(u => u.id === +id) ?? null;
    this.usuarioSeleccionado.set(found);
    this.compraService.usuarioActivo.set(found);
    if (found) this.emailConfirmacion.set(found.email);
  }

  agregarEntrada() {
    if (this.entradas().length < 10) {
      this.entradas.update(e => [...e, { edad: 0, tipo_pase: 'REGULAR', precio_unitario: this.PRECIO_REGULAR }]);
    }
  }

  quitarEntrada(index: number) {
    if (this.entradas().length > 1) {
      this.entradas.update(e => e.filter((_, i) => i !== index));
    }
  }

  onTipoPaseChange(index: number, tipo: 'VIP' | 'REGULAR') {
    this.entradas.update(e => e.map((item, i) =>
      i === index
        ? { ...item, tipo_pase: tipo, precio_unitario: this.calcularPrecio(item.edad, tipo) }
        : item
    ));
  }

  updateEdad(index: number, edad: number) {
    this.entradas.update(e => e.map((item, i) =>
      i === index
        ? { ...item, edad: +edad, precio_unitario: this.calcularPrecio(+edad, item.tipo_pase) }
        : item
    ));
  }

  confirmarCompra() {
    this.error.set('');
    this.resultado.set(null);

    if (!this.usuarioSeleccionado()) {
      this.error.set('Seleccioná un usuario para continuar.');
      return;
    }
    if (!this.fecha() || !this.formaPago()) {
      this.error.set('Completá todos los campos antes de continuar.');
      return;
    }
    if (!this.emailConfirmacion() || !this.emailConfirmacion().includes('@')) {
      this.error.set('Ingresá un email válido para recibir la confirmación.');
      return;
    }
    if (this.entradas().some(e => e.edad < 0)) {
      this.error.set('Ingresá la edad de todos los visitantes.');
      return;
    }

    this.cargando.set(true);

  const compra: CompraRequest = {
  usuario: { id: this.usuarioSeleccionado()!.id },
  fecha: this.fecha(),
  forma_pago: this.formaPago() as 'TARJETA' | 'EFECTIVO',
  entradas: this.entradas(),
  email_confirmacion: this.emailConfirmacion(),
};

if (this.formaPago() === 'TARJETA') {

 this.pagoTemporalService.compraPendiente = compra;

this.router.navigate(['/mercado-pago']);


  return;
}

this.cargando.set(true);

this.compraService.realizarCompra(compra)
  .subscribe({
    next: (res) => {
      this.cargando.set(false);
      this.resultado.set(res);
    },
    error: (err) => {
      this.cargando.set(false);
      this.error.set(err.error?.error ?? 'Error al procesar la compra.');
    }
  });
  }

  nuevaCompra() {
    this.fecha.set('');
    this.formaPago.set('');
    this.entradas.set([{ edad: 0, tipo_pase: 'REGULAR', precio_unitario: this.PRECIO_REGULAR }]);
    this.error.set('');
    this.resultado.set(null);
  }
}
