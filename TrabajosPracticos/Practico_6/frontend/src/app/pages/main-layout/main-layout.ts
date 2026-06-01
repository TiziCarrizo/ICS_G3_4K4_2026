import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CompraService } from '../../services/compra.service';

@Component({
  selector: 'app-main-layout',
  standalone: true,
  imports: [RouterModule],
  templateUrl: './main-layout.html',
  styleUrl: './main-layout.scss',
})
export class MainLayout {
  constructor(protected compraService: CompraService) {}
}
