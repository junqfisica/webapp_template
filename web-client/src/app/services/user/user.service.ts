import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ServerUrl } from '../../statics/server-url';

@Injectable()
export class UserService {

  constructor(private http: HttpClient) { }

  get(id: number): Observable<any> {
    return this.http.get<any>(ServerUrl.rootUrl + '/api/users/' + id);
  }
}
