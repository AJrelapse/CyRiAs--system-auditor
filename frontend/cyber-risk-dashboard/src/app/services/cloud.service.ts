import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class CloudService {

  private http = inject(HttpClient);
  private api = environment.apiUrl;

  getResources(): Observable<any> {
    return this.http.get<any>(
      `${this.api}/cloud/resources`
    );
  }

}