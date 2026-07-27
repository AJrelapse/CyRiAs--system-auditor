import {
  Component,
  Input,
  OnChanges
} from '@angular/core';

import {
  NgxEchartsDirective,
  provideEchartsCore
} from 'ngx-echarts';

import { CommonModule } from '@angular/common';

import * as echarts from 'echarts/core';

import {
  GraphChart
} from 'echarts/charts';

import {
  TooltipComponent,
  LegendComponent
} from 'echarts/components';

import {
  CanvasRenderer
} from 'echarts/renderers';

echarts.use([
  GraphChart,
  TooltipComponent,
  LegendComponent,
  CanvasRenderer
]);

@Component({
  selector: 'app-knowledge-graph-visualization',
  standalone: true,
  imports: [
    CommonModule,
    NgxEchartsDirective
  ],
  providers: [
    provideEchartsCore({
      echarts
    })
  ],
  templateUrl:
    './knowledge-graph-visualization.component.html',
  styleUrls: [
    './knowledge-graph-visualization.component.scss'
  ]
})
export class KnowledgeGraphVisualizationComponent
implements OnChanges {

  @Input()
  graph: any;

  options: any;

  ngOnChanges(): void {

    if (!this.graph) {
      return;
    }

    this.options = {

      tooltip: {

        formatter: (params: any) => {

          if (params.dataType === 'node') {

            return `
              <b>${params.data.label}</b><br>
              ${params.data.category}
            `;

          }

          return `
            ${params.data.relationship}
          `;
        }

      },

      legend: {

        top: 20

      },

      animationDuration: 1500,

      series: [

        {

          type: 'graph',

          layout: 'force',

          roam: true,

          draggable: true,

          focusNodeAdjacency: true,

          edgeSymbol: ['none', 'arrow'],

          edgeSymbolSize: 8,

          label: {

            show: true,

            position: 'right',

            fontSize: 12

          },

          force: {

            repulsion: 900,

            gravity: 0.08,

            edgeLength: 180

          },

          categories: [

            { name: 'asset' },

            { name: 'identity' },

            { name: 'cloud_identity' },

            { name: 'external' },

            { name: 'vulnerability' },

            { name: 'attack_technique' },

            { name: 'security_control' }

          ],

          data: this.graph.nodes.map(
            (node: any) => ({

              id: node.id,

              name: node.label,

              label: {

                show: true

              },

              value: node.label,

              category: node.type,

              symbolSize: this.getNodeSize(node.type),

              itemStyle: {

                color: this.getColor(node.type)

              }

            })
          ),

          links: this.graph.edges.map(
            (edge: any) => ({

              source: edge.source,

              target: edge.target,

              relationship: edge.relationship,

              lineStyle: {

                width: 2

              },

              label: {

                show: false

              }

            })
          )

        }

      ]

    };

  }

  private getNodeSize(type: string): number {

    switch (type) {

      case 'asset':
        return 55;

      case 'vulnerability':
        return 40;

      case 'attack_technique':
        return 35;

      case 'security_control':
        return 35;

      case 'identity':
        return 45;

      case 'cloud_identity':
        return 45;

      case 'external':
        return 65;

      default:
        return 40;

    }

  }

  private getColor(type: string): string {

    switch (type) {

      case 'asset':
        return '#1976d2';

      case 'identity':
        return '#43a047';

      case 'cloud_identity':
        return '#00acc1';

      case 'external':
        return '#ef6c00';

      case 'vulnerability':
        return '#d32f2f';

      case 'attack_technique':
        return '#8e24aa';

      case 'security_control':
        return '#2e7d32';

      default:
        return '#757575';

    }

  }

}