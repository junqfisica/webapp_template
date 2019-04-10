import { Injectable } from '@angular/core';
import { Router, CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';

import { LocalStorage } from '../statics/local-storage';
import { Role } from '../model/model.role';

@Injectable()
export class LoginPermission implements CanActivate {

  constructor(private router: Router) { }

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
    if (LocalStorage.currentUser) {
      // logged in so return true
      return true;
    }

    // not logged in so redirect to login page with the return url
    this.router.navigate(['/login'], { queryParams: { returnUrl: state.url }});
    return false;
  }
}

@Injectable()
export class AdminPermission implements CanActivate {

  constructor(private router: Router) { }

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
    if (LocalStorage.currentUser && LocalStorage.currentUser.roles.includes("ROLE_ADMIN")) {
      return true;
    }

    // Don't have admin role.
    this.router.navigate(['/'], { queryParams: { returnUrl: state.url }});
    return false;
  }
}

@Injectable()
export class SameUserPermission implements CanActivate {

  constructor(private router: Router) { }

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
    if (LocalStorage.currentUser) {
      if (route.params.id && route.params.id == LocalStorage.currentUser.id) {
        return true;
      } else if (route.params.username && route.params.username == LocalStorage.currentUser.username){
        return true;
      } else {
        // Not the same user.
        this.router.navigate(['/'], { queryParams: { returnUrl: state.url }});
        return false;
      }
    }
  }
}