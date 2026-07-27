import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AttackPathService {

  private http = inject(HttpClient);

  private api = environment.apiUrl;

  generatePaths(): Observable<any> {

    return this.http.post(
      `${this.api}/attack-path/generate`,
      {}
    );

  }

}