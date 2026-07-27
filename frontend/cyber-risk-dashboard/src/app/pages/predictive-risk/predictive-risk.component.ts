import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';

import { PredictiveRiskService } from '../../services/predictive-risk.service';
import { RiskPredictionsComponent } from './components/risk-predictions/risk-predictions.component';

@Component({
  selector: 'app-predictive-risk',
  standalone: true,
  imports: [
    CommonModule,
    RiskPredictionsComponent
  ],
  templateUrl: './predictive-risk.component.html',
  styleUrl: './predictive-risk.component.scss'
})
export class PredictiveRiskComponent implements OnInit {

  private predictiveService = inject(PredictiveRiskService);

  prediction: any = null;

  ngOnInit(): void {
    this.loadPrediction();
  }

  loadPrediction(): void {

    this.predictiveService.predictRisk().subscribe({

      next: (response) => {

        this.prediction = response;

      },

      error: console.error

    });

  }

}