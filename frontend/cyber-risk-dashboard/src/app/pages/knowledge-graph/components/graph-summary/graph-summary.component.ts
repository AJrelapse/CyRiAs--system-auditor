import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-graph-summary',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './graph-summary.component.html',
  styleUrl: './graph-summary.component.scss'
})
export class GraphSummaryComponent {

  @Input() graph: any;

}