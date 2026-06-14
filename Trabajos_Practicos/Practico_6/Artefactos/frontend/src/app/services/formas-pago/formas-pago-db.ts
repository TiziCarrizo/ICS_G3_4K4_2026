import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { firstValueFrom } from 'rxjs';

export interface FormaPago {
    id: number;
    nombre: string;
}

@Injectable({
    providedIn: 'root'
})
export class FormasPagoDb {
    private baseUrl = 'http://127.0.0.1:8000/formas_pago';

    constructor(private httpClient: HttpClient) { }

    getAll(): Promise<FormaPago[]> {
        return firstValueFrom(this.httpClient.get<FormaPago[]>(this.baseUrl));
    }
}
