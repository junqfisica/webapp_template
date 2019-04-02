import { NgModule } from '@angular/core';

import { Routes, RouterModule } from '@angular/router';
import { LoginComponent } from './components/login/login.component';
import { CreateUserComponent } from './components/user/create-user/create-user.component';
import { UrlPermission } from './urlPermission/url.permission';

const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'user/createUser', component: CreateUserComponent, canActivate: [UrlPermission]},

  // otherwise redirect to profile
  { path: '**', redirectTo: '/' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
