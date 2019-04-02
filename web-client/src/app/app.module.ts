import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';

import { ButtonsModule } from 'ngx-bootstrap/buttons';
import { AlertModule } from 'ngx-bootstrap/alert';
import { TabsModule } from 'ngx-bootstrap/tabs';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { UserService } from './services/user/user.service';
import { TokenInterceptor } from './interceptors/token.interceptor';
import { AuthService } from './services/auth/auth.service';
import { LoginComponent } from './components/login/login.component';
import { NotificationService } from './services/notification/notification.service';
import { CreateUserComponent } from './components/user/create-user/create-user.component';
import { UrlPermission } from './urlPermission/url.permission';


@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    CreateUserComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    AppRoutingModule,
    HttpClientModule,
    ButtonsModule.forRoot(),
    AlertModule.forRoot(),
    TabsModule.forRoot()
  ],
  providers: [
    AuthService,
    NotificationService,
    UserService,
    {
      provide: HTTP_INTERCEPTORS,
      useClass: TokenInterceptor,
      multi: true
    },
    UrlPermission
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
