import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-principal',
  imports: [],
  templateUrl: './principal.html',
  styleUrl: './principal.scss',
})
export class Principal {
  constructor(private router: Router) {}

  onClick() {
    this.router.navigate(['/comprar-entrada']);
  }
}
