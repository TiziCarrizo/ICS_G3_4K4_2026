import { Routes } from '@angular/router';
import { Principal } from './pages/principal/principal';
import { MainLayout} from './pages/main-layout/main-layout';
import { ComprarEntrada } from './pages/comprar-entrada/comprar-entrada';

export const routes: Routes = [
    {
        path: '',
        component: MainLayout,
        children: [
            { path: '', component: Principal},
            { path: 'comprar-entrada', component: ComprarEntrada }
        ]   
    }
];
