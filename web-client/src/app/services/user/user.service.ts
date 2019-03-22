import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ServerUrl } from '../../statics/server-url';

@Injectable()
export class UserService {

  constructor(private http: HttpClient) { }

  get(id: string): Observable<any> {
    return this.http.get<any>(ServerUrl.rootUrl + '/api/user/' + id);
  }

  getAll(): Observable<any> {
    return this.http.get<any>(ServerUrl.rootUrl + '/api/users');
  }

  get_by_username(username: string): Observable<any> {
    return this.http.get<any>(ServerUrl.rootUrl + '/api/user/username/' + username);
  }
}
