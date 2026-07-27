import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class KnowledgeGraphService {

  private http = inject(HttpClient);

  private api = environment.apiUrl;

  buildGraph(): Observable<any> {
    return this.http.post(
      `${this.api}/knowledge-graph/build`,
      {}
    );
  }

  getGraph(): Observable<any> {
    return this.http.get(
      `${this.api}/knowledge-graph/graph`
    );
  }

}