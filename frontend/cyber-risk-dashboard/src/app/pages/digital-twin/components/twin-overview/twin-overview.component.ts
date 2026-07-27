import {
  Component,
  Input,
  OnChanges
} from '@angular/core';

import { CommonModule } from '@angular/common';

import { DigitalTwinGraphComponent } from '../digital-twin-graph/digital-twin-graph.component';

@Component({
  selector: 'app-twin-overview',
  standalone: true,
  imports: [
    CommonModule,
    DigitalTwinGraphComponent
  ],
  templateUrl: './twin-overview.component.html',
  styleUrl: './twin-overview.component.scss'
})
export class TwinOverviewComponent implements OnChanges {

  @Input()
  twin: any;

  totalNodes = 0;

  totalEdges = 0;

  assets = 0;

  identities = 0;

  cloudIdentities = 0;

  vulnerabilities = 0;

  securityControls = 0;

  criticalAssets = 0;

  ngOnChanges(): void {

    if (!this.twin) {
      return;
    }

    this.totalNodes = this.twin.node_count;

    this.totalEdges = this.twin.edge_count;

    this.assets = this.count('asset');

    this.identities = this.count('identity');

    this.cloudIdentities = this.count('cloud_identity');

    this.vulnerabilities = this.count('vulnerability');

    this.securityControls = this.count('security_control');

    this.criticalAssets = this.twin.nodes.filter(

      (node: any) =>

        node.node_type === 'asset' &&

        node.properties?.criticality === 'critical'

    ).length;

  }

  count(type: string): number {

    return this.twin.nodes.filter(

      (node: any) => node.node_type === type

    ).length;

  }

}