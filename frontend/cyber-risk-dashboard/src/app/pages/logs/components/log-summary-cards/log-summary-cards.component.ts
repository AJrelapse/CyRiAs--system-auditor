import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-log-summary-cards',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './log-summary-cards.component.html',
  styleUrl: './log-summary-cards.component.scss'
})
export class LogSummaryCardsComponent {

  @Input() summary: any;

}