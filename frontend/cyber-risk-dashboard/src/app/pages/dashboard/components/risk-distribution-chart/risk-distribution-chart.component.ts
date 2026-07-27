import { Component, Input, OnChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgxEchartsDirective } from 'ngx-echarts';

@Component({
  selector: 'app-risk-distribution-chart',
  standalone: true,
  imports: [CommonModule, NgxEchartsDirective],
  templateUrl: './risk-distribution-chart.component.html',
  styleUrl: './risk-distribution-chart.component.scss'
})
export class RiskDistributionChartComponent implements OnChanges {

  @Input() assessments: any[] = [];

  chartOptions: any = {};

  ngOnChanges(): void {

    const counts = {
      Low: 0,
      Medium: 0,
      High: 0,
      Critical: 0
    };

    this.assessments.forEach(asset => {

      if (counts.hasOwnProperty(asset.risk_level)) {
        counts[asset.risk_level as keyof typeof counts]++;
      }

    });

    this.chartOptions = {

      tooltip: {
        trigger: 'item'
      },

      legend: {
        bottom: 0,
        textStyle: {
          color: '#fff'
        }
      },

      series: [

        {
          type: 'pie',
          radius: ['45%', '75%'],

          data: [

            { value: counts.Low, name: 'Low' },

            { value: counts.Medium, name: 'Medium' },

            { value: counts.High, name: 'High' },

            { value: counts.Critical, name: 'Critical' }

          ]
        }

      ]
    };

  }

}