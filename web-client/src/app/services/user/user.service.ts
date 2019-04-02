import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ServerUrl } from '../../statics/server-url';
import { User } from '../../model/model.user';
import { Role } from '../../model/model.role';


@Injectable()
export class UserService {

  constructor(private http: HttpClient) { }

  get(id: string): Observable<any> {
    return this.http.get<any>(ServerUrl.rootUrl + '/api/user/' + id);
  }

  getAll(): Observable<any> {
    return this.http.get<any>(ServerUrl.rootUrl + '/api/user/all');
  }

  getByUsername(username: string): Observable<any> {
    return this.http.get<any>(ServerUrl.rootUrl + '/api/user/username/' + username);
  }

  createUser(user: User): Observable<Boolean> {
    return this.http.post<Boolean>(ServerUrl.rootUrl + '/api/user/create', user) 
  }

  getRoles(): Observable<Role[]>{
    return this.http.get<Role[]>(ServerUrl.rootUrl + '/api/user/roles');
  }

  isUsernameTaken(username: string): Observable<boolean>{
    return this.http.get<boolean>(ServerUrl.rootUrl + '/api/user/isTaken/' + username);
  }
}
