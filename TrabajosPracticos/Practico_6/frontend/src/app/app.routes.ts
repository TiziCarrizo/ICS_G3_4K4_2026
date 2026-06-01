import { Routes } from '@angular/router';
import { Principal } from './pages/principal/principal';
import { MainLayout} from './pages/main-layout/main-layout';
import { ComprarEntrada } from './pages/comprar-entrada/comprar-entrada';
import { MisCompras } from './pages/mis-compras/mis-compras';
import { MercadoPago } from './pages/mercado-pago/mercado-pago';

export const routes: Routes = [
    {
        path: '',
        component: MainLayout,
        children: [
            { path: '', component: Principal},
            { path: 'comprar-entrada', component: ComprarEntrada },
            { path: 'mis-compras', component: MisCompras },
            { path: 'mercado-pago', component: MercadoPago }
        ]   
    }
];
