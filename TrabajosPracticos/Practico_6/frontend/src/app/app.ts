import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';

interface AppUser {
    id: number;
    nombre: string;
    apellido: string;
    email: string;
}

export const MOCK_USER: AppUser = {
    nombre: "Manuel",
    apellido: "Dávila",
    email: "chaito109@yahoo.com.ar",
    id: 1
}

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected readonly title = signal('frontend');
}
