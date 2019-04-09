import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

import { Observable } from 'rxjs';

import { ServerUrl } from '../../statics/server-url';
import { User } from '../../model/model.user';
import { Role } from '../../model/model.role';
import { SearchResult } from '../../model/model.search-result';


@Injectable()
export class UserService {

  constructor(private http: HttpClient) { }

  get(id: string): Observable<User> {
    return this.http.get<User>(ServerUrl.rootUrl + '/api/user/' + id);
  }

  getAll(): Observable<User[]> {
    return this.http.get<User[]>(ServerUrl.rootUrl + '/api/user/all');
  }

  search(params: HttpParams): Observable<SearchResult> {
    return this.http.get<SearchResult>(ServerUrl.rootUrl + '/api/user/search', { params });
  }

  getByUsername(username: string): Observable<any> {
    return this.http.get<any>(ServerUrl.rootUrl + '/api/user/username/' + username);
  }

  createUser(user: User): Observable<Boolean> {
    return this.http.post<Boolean>(ServerUrl.rootUrl + '/api/user/create', user) 
  }

  updateUser(user: User): Observable<Boolean> {
    return this.http.post<Boolean>(ServerUrl.rootUrl + '/api/user/update', user) 
  }

  getRoles(): Observable<Role[]>{
    return this.http.get<Role[]>(ServerUrl.rootUrl + '/api/user/roles');
  }

  isUsernameTaken(username: string): Observable<boolean>{
    return this.http.get<boolean>(ServerUrl.rootUrl + '/api/user/isTaken/' + username);
  }

  deleteUser(user: User): Observable<boolean> {
    return this.http.delete<boolean>(ServerUrl.rootUrl + '/api/user/delete/' + user.id);
  }
}
