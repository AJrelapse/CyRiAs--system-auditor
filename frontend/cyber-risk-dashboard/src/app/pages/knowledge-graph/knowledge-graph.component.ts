import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';

import { KnowledgeGraphService } from '../../services/knowledge-graph.service';
import { KnowledgeGraphVisualizationComponent } from './components/knowledge-graph-visualization/knowledge-graph-visualization.component';

@Component({
  selector: 'app-knowledge-graph',
  standalone: true,
  imports: [
    CommonModule,
    KnowledgeGraphVisualizationComponent
  ],
  templateUrl: './knowledge-graph.component.html',
  styleUrl: './knowledge-graph.component.scss'
})
export class KnowledgeGraphComponent implements OnInit {

  private service = inject(KnowledgeGraphService);

  graph: any;

  ngOnInit(): void {

    this.service.buildGraph().subscribe({

      next: () => {

        this.service.getGraph().subscribe({

          next: response => {

            this.graph = response;

          },

          error: console.error

        });

      },

      error: console.error

    });

  }

}