import { Component, Input, OnChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgxEchartsDirective } from 'ngx-echarts';

@Component({
  selector: 'app-risk-trend-chart',
  standalone: true,
  imports: [CommonModule, NgxEchartsDirective],
  templateUrl: './risk-trend-chart.component.html',
  styleUrl: './risk-trend-chart.component.scss'
})
export class RiskTrendChartComponent implements OnChanges {

  @Input() assessments: any[] = [];

  chartOptions: any = {};

  ngOnChanges(): void {

    this.chartOptions = {

      tooltip: {
        trigger: 'axis'
      },

      xAxis: {
        type: 'category',
        data: this.assessments.map(a => a.asset_name),
        axisLabel: {
          color: '#fff'
        }
      },

      yAxis: {
        type: 'value',
        axisLabel: {
          color: '#fff'
        }
      },

      series: [

        {
          name: 'Risk Score',
          type: 'line',
          smooth: true,
          data: this.assessments.map(a => a.overall_score)
        }

      ]

    };

  }

}