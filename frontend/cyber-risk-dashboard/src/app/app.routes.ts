import { Routes } from '@angular/router';

import { DashboardLayoutComponent } from './layouts/dashboard-layout/dashboard-layout.component';

import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { AssetDiscoveryComponent } from './pages/asset-discovery/asset-discovery.component';
import { DigitalTwinComponent } from './pages/digital-twin/digital-twin.component';
import { KnowledgeGraphComponent } from './pages/knowledge-graph/knowledge-graph.component';
import { PredictiveRiskComponent } from './pages/predictive-risk/predictive-risk.component';
import { AttackPathComponent } from './pages/attack-path/attack-path.component';
import { RiskAssessmentComponent } from './pages/risk-assessment/risk-assessment.component';
import { CloudComponent } from './pages/cloud/cloud.component';
import { IdentityComponent } from './pages/identity/identity.component';
import { ConfigurationComponent } from './pages/configuration/configuration.component';
import { LogsComponent } from './pages/logs/logs.component';

export const routes: Routes = [
  {
    path: '',
    component: DashboardLayoutComponent,
    children: [
      { path: '', component: DashboardComponent },
      { path: 'asset-discovery', component: AssetDiscoveryComponent },
      { path: 'digital-twin', component: DigitalTwinComponent },
      { path: 'knowledge-graph', component: KnowledgeGraphComponent },
      { path: 'predictive-risk', component: PredictiveRiskComponent },
      { path: 'attack-path', component: AttackPathComponent },
      { path: 'risk-assessment', component: RiskAssessmentComponent },
      { path: 'cloud', component: CloudComponent },
      { path: 'identity', component: IdentityComponent },
      { path: 'configuration', component: ConfigurationComponent },
      { path: 'logs', component: LogsComponent }
    ]
  },
  {
    path: '**',
    redirectTo: ''
  }
];