import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';

import { AttackPathService } from '../../services/attack-path.service';
import { AttackPathTableComponent } from './components/attack-path-table/attack-path-table.component';

@Component({
  selector: 'app-attack-path',
  standalone: true,
  imports: [
    CommonModule,
    AttackPathTableComponent
  ],
  templateUrl: './attack-path.component.html',
  styleUrl: './attack-path.component.scss'
})
export class AttackPathComponent implements OnInit {

  private attackPathService = inject(AttackPathService);

  paths: any[] = [];

  ngOnInit(): void {
    this.loadAttackPaths();
  }

  loadAttackPaths(): void {

    this.attackPathService.generatePaths().subscribe({

      next: (response) => {

        this.paths = response.attack_paths;

      },

      error: console.error

    });

  }

}