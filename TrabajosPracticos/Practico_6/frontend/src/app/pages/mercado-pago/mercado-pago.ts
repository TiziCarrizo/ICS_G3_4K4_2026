import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { PagoTemporalService } from '../../services/formas-pago/pago-temporal.service';

@Component({
  selector: 'app-mercado-pago',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './mercado-pago.html',
  styleUrl: './mercado-pago.scss'
})
export class MercadoPago {

  numeroTarjeta = '';
  titular = '';
  vencimiento = '';
  cvv = '';

  procesando = false;
  pagoExitoso = false;

constructor(
  private router: Router,
  private pagoTemporal: PagoTemporalService,
  private httpClient: HttpClient
) {}

  formatearVencimiento() {
    let valor = this.vencimiento.replace(/\D/g, '');

    if (valor.length >= 3) {
      valor = valor.substring(0, 2) + '/' + valor.substring(2, 4);
    }

    this.vencimiento = valor;
  }

  pagar() {

    if (
      this.numeroTarjeta.length !== 16 ||
      this.titular.trim().length < 3 ||
      this.vencimiento.length !== 5 ||
      this.cvv.length !== 3
    ) {
      alert('Completá correctamente todos los campos');
      return;
    }

    this.procesando = true;

    setTimeout(() => {

      this.procesando = false;
      this.pagoExitoso = true;

      setTimeout(() => {
        this.router.navigate(['/mis-compras']);
      }, 2000);

    }, 3000);
  }
}