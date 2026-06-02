import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { MOCK_USER } from '../../app';

interface EntradaDetalle {
  edad: number;
  tipo: string;
  precio_unitario: number;
}

interface CompraHistorial {
  id: number;
  fecha: string;
  fecha_compra: string;
  cantidad_entradas: number;
  monto_total: number;
  forma_pago: string;
  mercado_pago_redirect_url: string | null;
  entradas: EntradaDetalle[];
}

@Component({
  selector: 'app-mis-compras',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './mis-compras.html',
  styleUrl: './mis-compras.scss'
})
export class MisCompras implements OnInit {
  compras: CompraHistorial[] = [];
  cargando = true;
  error = '';
  mockUser = MOCK_USER;

  private apiBaseUrl = 'http://127.0.0.1:8000';

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.http.get<{ compras: CompraHistorial[] }>(
      `${this.apiBaseUrl}/api/mis-compras/?usuario_id=${this.mockUser.id}`
    ).subscribe({
      next: (res) => {
        this.compras = res.compras;
        this.cargando = false;
      },
      error: () => {
        this.error = 'No se pudieron cargar tus compras. Intentá de nuevo más tarde.';
        this.cargando = false;
      }
    });
  }
}
