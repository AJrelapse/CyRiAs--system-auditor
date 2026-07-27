import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';

import { DigitalTwinService } from '../../services/digital-twin.service';
import { TwinOverviewComponent } from './components/twin-overview/twin-overview.component';

@Component({
  selector: 'app-digital-twin',
  standalone: true,
  imports: [
    CommonModule,
    TwinOverviewComponent
  ],
  templateUrl: './digital-twin.component.html',
  styleUrl: './digital-twin.component.scss'
})
export class DigitalTwinComponent implements OnInit {

  private twinService = inject(DigitalTwinService);

  twin: any = null;

  loading = false;

  ngOnInit(): void {
    this.loadTwin();
  }

  loadTwin() {

    this.loading = true;

    this.twinService.buildTwin().subscribe({

      next: (response) => {

        this.twin = response;

        this.loading = false;

      },

      error: (err) => {

        console.error(err);

        this.loading = false;

      }

    });

  }

}