import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { MOCK_USER } from '../../app';

@Component({
  selector: 'app-main-layout',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './main-layout.html',
  styleUrl: './main-layout.scss',
})
export class MainLayout {
  protected mockUser = MOCK_USER;

}
