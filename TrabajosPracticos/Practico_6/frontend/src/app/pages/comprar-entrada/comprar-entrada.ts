import { Component, OnInit, computed, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { CompraService, EntradaItem, CompraResponse, UsuarioApi } from '../../services/compra.service';

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

  fecha = signal('');
  formaPago = signal<'TARJETA' | 'EFECTIVO' | ''>('');
  entradas = signal<EntradaItem[]>([{ edad: 0, tipo_pase: 'REGULAR', precio_unitario: 2500 }]);

  cargando = signal(false);
  error = signal('');
  resultado = signal<CompraResponse | null>(null);

  readonly PRECIO_VIP = 5000;
  readonly PRECIO_REGULAR = 2500;

  montoTotal = computed(() => this.entradas().reduce((sum, e) => sum + e.precio_unitario, 0));

  constructor(private compraService: CompraService) {}

  ngOnInit() {
    this.compraService.getUsuarios().subscribe({
      next: (usuarios) => {
        this.usuarios.set(usuarios);
        if (usuarios.length > 0) {
          this.usuarioSeleccionado.set(usuarios[0]);
          this.usuarioId.set(usuarios[0].id);
          this.compraService.usuarioActivo.set(usuarios[0]);
        }
      },
      error: () => this.error.set('No se pudieron cargar los usuarios.')
    });
  }

  onUsuarioChange(id: number) {
    const found = this.usuarios().find(u => u.id === +id) ?? null;
    this.usuarioSeleccionado.set(found);
    this.compraService.usuarioActivo.set(found);
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
        ? { ...item, tipo_pase: tipo, precio_unitario: tipo === 'VIP' ? this.PRECIO_VIP : this.PRECIO_REGULAR }
        : item
    ));
  }

  updateEdad(index: number, edad: number) {
    this.entradas.update(e => e.map((item, i) => i === index ? { ...item, edad: +edad } : item));
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
    if (this.entradas().some(e => !e.edad || e.edad <= 0)) {
      this.error.set('Ingresá la edad de todos los visitantes.');
      return;
    }

    this.cargando.set(true);

    this.compraService.realizarCompra({
      usuario: { id: this.usuarioSeleccionado()!.id },
      fecha: this.fecha(),
      forma_pago: this.formaPago() as 'TARJETA' | 'EFECTIVO',
      entradas: this.entradas(),
    }).subscribe({
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
