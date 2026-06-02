import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';



@Component({
  selector: 'app-mercado-pago',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './mercado-pago.html',
  styleUrl: './mercado-pago.scss'
})
export class MercadoPago {

  numeroTarjeta = '4509953566233704';
  titular = 'Manuel Dávila';
  vencimiento = '12/30';
  cvv = '123';

  procesando = false;
  pagoExitoso = false;
  private payload: any;
  private modalData: any;

constructor(
    private router: Router,
    private httpClient: HttpClient
  ) {
    const nav = this.router.getCurrentNavigation();
    this.payload = nav?.extras?.state?.['payload'];
    this.modalData = nav?.extras?.state?.['modalData'];
  }

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

  const headers = new HttpHeaders({ 'Content-Type': 'application/json' });

  this.httpClient.post('http://127.0.0.1:8000/api/compras/', this.payload, { headers })
    .subscribe({
      next: () => {
          setTimeout(() => {
              this.procesando = false;
              this.pagoExitoso = true;
              setTimeout(() => {
                  this.router.navigate(['/comprar-entrada'], {   // ← cambiar ruta
                      state: {
                          mostrarModal: true,
                          modalData: this.modalData
                      }
                  });
              }, 500);
          }, 500);
      },
      error: () => {
        this.procesando = false;
        alert('Error al procesar el pago. Intentá de nuevo.');
      }
    });
}
}