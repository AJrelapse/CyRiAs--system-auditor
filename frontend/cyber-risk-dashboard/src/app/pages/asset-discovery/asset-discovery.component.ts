import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';

import { AssetDiscoveryService } from '../../services/asset-discovery.service';
import { AssetTableComponent } from './components/asset-table/asset-table.component';

@Component({
  selector: 'app-asset-discovery',
  standalone: true,
  imports: [
    CommonModule,
    AssetTableComponent
  ],
  templateUrl: './asset-discovery.component.html',
  styleUrl: './asset-discovery.component.scss'
})
export class AssetDiscoveryComponent implements OnInit {

  private assetService = inject(AssetDiscoveryService);

  assets: any[] = [];

  loading = false;

  ngOnInit(): void {
    this.loadAssets();
  }

  loadAssets() {

    this.loading = true;

    this.assetService.discoverAssets().subscribe({

      next: (response) => {

        this.assets = response;
        this.loading = false;

      },

      error: (err) => {

        console.error(err);
        this.loading = false;

      }

    });

  }

}