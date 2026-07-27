import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';

import { StatCardComponent } from '../../shared/components/stat-card/stat-card.component';
import { RiskDistributionChartComponent } from './components/risk-distribution-chart/risk-distribution-chart.component';

import { RiskAssessmentService } from '../../services/risk-assessment.service';
import { HighestRiskAssetsComponent } from './components/highest-risk-assets/highest-risk-assets.component';
import { RiskTrendChartComponent } from './components/risk-trend-chart/risk-trend-chart.component';
@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    StatCardComponent,
    RiskDistributionChartComponent,
    HighestRiskAssetsComponent,
    RiskTrendChartComponent
  ],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss'
})
export class DashboardComponent implements OnInit {

  private riskService = inject(RiskAssessmentService);

  totalAssets = 0;
  averageRisk = 0;
  criticalAssets = 0;
  highestRiskAsset = '';

  riskAssessments: any[] = [];

  ngOnInit(): void {
    this.loadDashboard();
  }

  loadDashboard(): void {

    this.riskService.getRiskAssessment().subscribe({

      next: (response) => {

        this.totalAssets = response.total_assets;

        this.averageRisk = response.average_risk_score;

        this.highestRiskAsset = response.highest_risk_asset;

        this.riskAssessments = response.assessments;

        this.criticalAssets = this.riskAssessments.filter(
          (asset: any) =>
            asset.risk_level === 'Critical' ||
            asset.risk_level === 'High'
        ).length;

      },

      error: (err) => {
        console.error(err);
      }

    });

  }

}