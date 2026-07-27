import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-identity-table',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './identity-table.component.html',
  styleUrl: './identity-table.component.scss'
})
export class IdentityTableComponent {

  @Input() identities: any[] = [];

}