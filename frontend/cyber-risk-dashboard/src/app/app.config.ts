import { ApplicationConfig } from '@angular/core';

import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';

import { routes } from './app.routes';

import { provideEchartsCore } from 'ngx-echarts';
import * as echarts from 'echarts/core';

import {
  PieChart,
  LineChart,
  BarChart
} from 'echarts/charts';

import {
  TooltipComponent,
  GridComponent,
  LegendComponent,
  TitleComponent
} from 'echarts/components';

import { CanvasRenderer } from 'echarts/renderers';

echarts.use([
  PieChart,
  LineChart,
  BarChart,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  TitleComponent,
  CanvasRenderer
]);

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideHttpClient(),
    provideEchartsCore({ echarts })
  ]
};