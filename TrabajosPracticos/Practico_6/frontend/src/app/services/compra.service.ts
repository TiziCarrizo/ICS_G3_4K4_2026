import { Injectable, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface UsuarioApi {
  id: number;
  nombre: string;
  apellido: string;
  email: string;
}

export interface EntradaItem {
  edad: number;
  tipo_pase: 'VIP' | 'REGULAR';
  precio_unitario: number;
}

export interface CompraRequest {
  usuario: { id: number };
  fecha: string;
  forma_pago: 'TARJETA' | 'EFECTIVO';
  entradas: EntradaItem[];
}

export interface CompraResponse {
  id: number;
  cantidad_entradas: number;
  fecha: string;
  monto_total: number;
  mercado_pago_redirect_url: string | null;
}

@Injectable({ providedIn: 'root' })
export class CompraService {
  private apiUrl = 'http://localhost:8000/api';
  usuarioActivo = signal<UsuarioApi | null>(null);

  constructor(private http: HttpClient) {}

  getUsuarios(): Observable<UsuarioApi[]> {
    return this.http.get<UsuarioApi[]>(`${this.apiUrl}/usuarios/`);
  }

  realizarCompra(datos: CompraRequest): Observable<CompraResponse> {
    return this.http.post<CompraResponse>(`${this.apiUrl}/comprar/`, datos);
  }
}
