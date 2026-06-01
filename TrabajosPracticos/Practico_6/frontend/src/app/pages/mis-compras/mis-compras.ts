import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { CompraService, CompraHistorial } from '../../services/compra.service';

@Component({
  selector: 'app-mis-compras',
  imports: [CommonModule, RouterModule],
  templateUrl: './mis-compras.html',
  styleUrl: './mis-compras.scss',
})
export class MisCompras implements OnInit {
  compras = signal<CompraHistorial[]>([]);
  cargando = signal(true);
  error = signal('');

  constructor(private compraService: CompraService) {}

  ngOnInit() {
    const usuario = this.compraService.usuarioActivo();
    if (!usuario) {
      this.error.set('Seleccioná un usuario desde "Comprar Entradas" para ver tus compras.');
      this.cargando.set(false);
      return;
    }
    this.compraService.getMisCompras(usuario.id).subscribe({
      next: (data) => {
        this.compras.set(data);
        this.cargando.set(false);
      },
      error: () => {
        this.error.set('No se pudieron cargar las compras.');
        this.cargando.set(false);
      }
    });
  }

  formatFecha(fecha: string): string {
    const [y, m, d] = fecha.split('-');
    return `${d}/${m}/${y}`;
  }

  get usuarioActivo() {
    return this.compraService.usuarioActivo();
  }
}
