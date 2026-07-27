import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class DigitalTwinService {

  private http = inject(HttpClient);

  private api = environment.apiUrl;

  buildTwin(): Observable<any> {

    return this.http.post(
      `${this.api}/digital-twin/build`,
      {}
    );

  }

}