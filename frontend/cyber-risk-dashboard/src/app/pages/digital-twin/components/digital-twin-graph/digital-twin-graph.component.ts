import {
  Component,
  Input,
  OnChanges
} from '@angular/core';

import { CommonModule } from '@angular/common';

import {
  NgxEchartsDirective,
  provideEchartsCore
} from 'ngx-echarts';

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
  selector: 'app-digital-twin-graph',
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
  templateUrl: './digital-twin-graph.component.html',
  styleUrl: './digital-twin-graph.component.scss'
})
export class DigitalTwinGraphComponent
implements OnChanges {

  @Input()
  twin: any;

  options: any;

  ngOnChanges(): void {

    if (!this.twin) {
      return;
    }

    this.buildGraph();

  }

  buildGraph(): void {

    const nodes = this.twin.nodes.map(
      (node: any) => ({

        id: node.node_id,

        name: node.label,

        category: this.category(node),

        value: node,

        symbol: this.symbol(node),

        symbolSize: this.size(node),

        itemStyle: {

          color: this.color(node)

        }

      })
    );

    const links = this.twin.edges.map(
      (edge: any) => ({

        source: edge.source,

        target: edge.target,

        value: edge.relationship,

        lineStyle: {

          color: this.edgeColor(
            edge.relationship
          ),

          width: 2,

          curveness: 0.18

        }

      })
    );

    this.options = {

      backgroundColor: 'transparent',

      tooltip: {

        formatter: (params: any) => {

          if (!params.data.value) {

            return params.data.value;

          }

          const node = params.data.value;

          return `
            <b>${node.label}</b><br>
            Type: ${node.node_type}<br>
            ${
              node.properties?.asset_type ??
              ''
            }
          `;

        }

      },

      series: [

        {

          type: 'graph',

          layout: 'force',

          draggable: true,

          roam: true,

          focusNodeAdjacency: true,

          edgeSymbol: [
            'none',
            'arrow'
          ],

          force: {

            repulsion: 650,

            edgeLength: 180

          },

          label: {

            show: true,

            color: '#fff',

            fontSize: 12

          },

          data: nodes,

          links,

          categories: [

            { name: 'asset' },

            { name: 'identity' },

            { name: 'cloud_identity' },

            { name: 'external' },

            { name: 'vulnerability' },

            { name: 'attack_technique' },

            { name: 'security_control' }

          ]

        }

      ]

    };

  }

  category(node: any): number {

    const map: any = {

      asset: 0,

      identity: 1,

      cloud_identity: 2,

      external: 3,

      vulnerability: 4,

      attack_technique: 5,

      security_control: 6

    };

    return map[node.node_type] ?? 0;

  }

  color(node: any): string {

    switch (node.node_type) {

      case 'asset':
        return '#3B82F6';

      case 'identity':
        return '#22C55E';

      case 'cloud_identity':
        return '#06B6D4';

      case 'external':
        return '#F97316';

      case 'vulnerability':
        return '#EF4444';

      case 'attack_technique':
        return '#8B5CF6';

      case 'security_control':
        return '#10B981';

      default:
        return '#94A3B8';

    }

  }

  symbol(node: any): string {

    if (node.node_type === 'external')
      return 'circle';

    if (node.node_type === 'identity')
      return 'diamond';

    if (node.node_type === 'cloud_identity')
      return 'triangle';

    if (node.node_type === 'vulnerability')
      return 'pin';

    if (node.node_type === 'attack_technique')
      return 'rect';

    if (node.node_type === 'security_control')
      return 'roundRect';

    const type =
      node.properties?.asset_type;

    switch (type) {

      case 'server':
        return 'rect';

      case 'database':
        return 'circle';

      case 'application':
        return 'roundRect';

      case 'endpoint':
        return 'diamond';

      default:
        return 'circle';

    }

  }

  size(node: any): number {

    if (
      node.properties?.criticality ===
      'critical'
    ) {

      return 75;

    }

    if (
      node.properties?.criticality ===
      'high'
    ) {

      return 65;

    }

    return 55;

  }

  edgeColor(type: string): string {

    switch (type) {

      case 'CONNECTS_TO':
        return '#3B82F6';

      case 'ADMIN_ACCESS':
        return '#EF4444';

      case 'HAS_ACCESS':
        return '#22C55E';

      case 'MEMBER_OF':
        return '#8B5CF6';

      case 'ASSUMES_ROLE':
        return '#06B6D4';

      case 'AFFECTED_BY':
        return '#F97316';

      case 'MITIGATES':
        return '#10B981';

      default:
        return '#64748B';

    }

  }

}