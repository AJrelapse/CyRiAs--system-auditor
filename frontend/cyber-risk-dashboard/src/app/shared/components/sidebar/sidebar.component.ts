import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';

import {
  LucideAngularModule,
  LayoutDashboard,
  Server,
  Network,
  Share2,
  TrendingUp,
  ShieldAlert,
  ShieldCheck,
  Cloud,
  Users,
  Settings,
  ScrollText
} from 'lucide-angular';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [
    RouterLink,
    RouterLinkActive,
    LucideAngularModule
  ],
  templateUrl: './sidebar.component.html',
  styleUrl: './sidebar.component.scss'
})
export class SidebarComponent {

  readonly LayoutDashboard = LayoutDashboard;
  readonly Server = Server;
  readonly Network = Network;
  readonly Share2 = Share2;
  readonly TrendingUp = TrendingUp;
  readonly ShieldAlert = ShieldAlert;
  readonly ShieldCheck = ShieldCheck;
  readonly Cloud = Cloud;
  readonly Users = Users;
  readonly Settings = Settings;
  readonly ScrollText = ScrollText;

}