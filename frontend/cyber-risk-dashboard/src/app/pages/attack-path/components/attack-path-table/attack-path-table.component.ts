import {
  Component,
  Input,
  OnChanges
} from '@angular/core';

import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-attack-path-table',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './attack-path-table.component.html',
  styleUrl: './attack-path-table.component.scss'
})
export class AttackPathTableComponent implements OnChanges {

  @Input()
  paths: any[] = [];

  totalPaths = 0;

  highestRisk = 0;

  uniqueTargets = 0;

  criticalCVEs = 0;

  ngOnChanges(): void {

    if (!this.paths?.length) {
      return;
    }

    this.totalPaths = this.paths.length;

    this.highestRisk = Math.max(
      ...this.paths.map(path => path.risk_score)
    );

    this.uniqueTargets = new Set(
      this.paths.map(path => path.target_asset)
    ).size;

    this.criticalCVEs = this.paths.filter(path =>
      path.vulnerabilities.some(
        (v: any) => v.severity === 'Critical'
      )
    ).length;

  }

  badgeClass(level: string): string {

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

  riskWidth(score: number): number {

    return Math.min(score, 100);

  }

  uniqueTechniques(path: any): any[] {

    return path.techniques.filter(
      (technique: any, index: number, array: any[]) =>
        index === array.findIndex(
          item => item.technique_id === technique.technique_id
        )
    );

  }

  uniqueControls(path: any): string[] {
    return Array.from(
      new Set<string>(path.missing_controls as string[])
    );

  }

}