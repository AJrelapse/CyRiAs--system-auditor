import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';

import { IdentityService } from '../../services/identity.service';
import { IdentityTableComponent } from './components/identity-table/identity-table.component';

@Component({
  selector: 'app-identity',
  standalone: true,
  imports: [
    CommonModule,
    IdentityTableComponent
  ],
  templateUrl: './identity.component.html',
  styleUrl: './identity.component.scss'
})
export class IdentityComponent implements OnInit {

  private identityService = inject(IdentityService);

  identities: any[] = [];

  ngOnInit(): void {
    this.loadIdentities();
  }

  loadIdentities(): void {

    this.identityService.getIdentities().subscribe({

      next: (response) => {

        this.identities = response;

      },

      error: console.error

    });

  }

}