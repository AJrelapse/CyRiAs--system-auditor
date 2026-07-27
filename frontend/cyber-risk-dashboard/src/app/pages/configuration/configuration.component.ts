import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ConfigurationService } from '../../services/configuration.service';
import { ConfigurationTableComponent } from './components/configuration-table/configuration-table.component';

@Component({
  selector: 'app-configuration',
  standalone: true,
  imports: [
    CommonModule,
    ConfigurationTableComponent
  ],
  templateUrl: './configuration.component.html',
  styleUrl: './configuration.component.scss'
})
export class ConfigurationComponent implements OnInit {

  private configurationService = inject(ConfigurationService);

  configurations: any[] = [];

  ngOnInit(): void {
    this.loadConfigurations();
  }

  loadConfigurations(): void {

    this.configurationService.getConfigurations().subscribe({

      next: (response) => {

        this.configurations = response;

      },

      error: console.error

    });

  }

}