import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';

import { CloudService } from '../../services/cloud.service';
import { CloudResourcesTableComponent } from './components/cloud-resources-table/cloud-resources-table.component';

@Component({
  selector: 'app-cloud',
  standalone: true,
  imports: [
    CommonModule,
    CloudResourcesTableComponent
  ],
  templateUrl: './cloud.component.html',
  styleUrl: './cloud.component.scss'
})
export class CloudComponent implements OnInit {

  private cloudService = inject(CloudService);

  resources: any[] = [];

  ngOnInit(): void {
    this.loadResources();
  }

  loadResources(): void {

    this.cloudService.getResources().subscribe({

      next: (response) => {

        this.resources = response;

      },

      error: console.error

    });

  }

}