import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AssetDiscoveryService {

  private http = inject(HttpClient);

  private api = environment.apiUrl;

  discoverAssets(): Observable<any> {

    return this.http.get<any>(
      `${this.api}/assets/discover`
    );

  }

}