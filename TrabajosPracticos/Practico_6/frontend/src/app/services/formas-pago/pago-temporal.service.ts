import { Injectable } from '@angular/core';
import { CompraRequest } from '../compra.service';

@Injectable({
  providedIn: 'root'
})
export class PagoTemporalService {

  compraPendiente: CompraRequest | null = null;

}