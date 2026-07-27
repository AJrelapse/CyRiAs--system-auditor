import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-highest-risk-assets',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './highest-risk-assets.component.html',
  styleUrl: './highest-risk-assets.component.scss'
})
export class HighestRiskAssetsComponent {

  @Input() assessments: any[] = [];

}