import {
  Component,
  Input,
  OnChanges
} from '@angular/core';

import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-risk-predictions',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './risk-predictions.component.html',
  styleUrl: './risk-predictions.component.scss'
})
export class RiskPredictionsComponent implements OnChanges {

  @Input()
  prediction: any;

  averageRisk = 0;

  critical = 0;

  high = 0;

  medium = 0;

  low = 0;

  highestAsset: any;

  ngOnChanges(): void {

    if (!this.prediction?.predictions) {
      return;
    }

    const predictions = this.prediction.predictions;

    this.averageRisk =
      predictions.reduce(
        (sum: number, asset: any) =>
          sum + asset.predicted_score,
        0
      ) / predictions.length;

    this.highestAsset =
      [...predictions]
      .sort(
        (a, b) =>
          b.predicted_score -
          a.predicted_score
      )[0];

    predictions.forEach((asset: any) => {

      switch (asset.risk_level) {

        case 'Critical':
          this.critical++;
          break;

        case 'High':
          this.high++;
          break;

        case 'Medium':
          this.medium++;
          break;

        default:
          this.low++;

      }

    });

  }

  badge(level: string): string {

    switch (level) {

      case 'Critical':
        return 'critical';

      case 'High':
        return 'high';

      case 'Medium':
        return 'medium';

      default:
        return 'low';

    }

  }

}