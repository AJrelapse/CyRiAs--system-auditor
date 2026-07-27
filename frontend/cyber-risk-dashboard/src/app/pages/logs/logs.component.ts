import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';

import { LogsService } from '../../services/logs.service';
import { LogSummaryCardsComponent } from './components/log-summary-cards/log-summary-cards.component';

@Component({
  selector: 'app-logs',
  standalone: true,
  imports: [
    CommonModule,
    LogSummaryCardsComponent
  ],
  templateUrl: './logs.component.html',
  styleUrl: './logs.component.scss'
})
export class LogsComponent implements OnInit {

  private logsService = inject(LogsService);

  summary: any;

  ngOnInit(): void {
    this.loadSummary();
  }

  loadSummary(): void {

    this.logsService.getSummary().subscribe({

      next: (response) => {

        this.summary = response;

      },

      error: console.error

    });

  }

}