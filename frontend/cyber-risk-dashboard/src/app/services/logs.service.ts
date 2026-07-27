import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class LogsService {

  private http = inject(HttpClient);

  private api = environment.apiUrl;

  getSummary(window: number = 60): Observable<any> {

    return this.http.get<any>(
      `${this.api}/logs/summary?window_minutes=${window}`
    );

  }

}