import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-cloud-resources-table',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './cloud-resources-table.component.html',
  styleUrl: './cloud-resources-table.component.scss'
})
export class CloudResourcesTableComponent {

  @Input() resources: any[] = [];

}