import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-configuration-table',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './configuration-table.component.html',
  styleUrl: './configuration-table.component.scss'
})
export class ConfigurationTableComponent {

  @Input() configurations: any[] = [];

}