import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-stat-card',
  standalone: true,
  imports: [],
  templateUrl: './stat-card.component.html',
  styleUrl: './stat-card.component.scss'
})
export class StatCardComponent {

  @Input() title = '';

  @Input() value: string | number = '';

  @Input() subtitle = '';

  @Input() icon = '';

  @Input() color = '#3B82F6';

}