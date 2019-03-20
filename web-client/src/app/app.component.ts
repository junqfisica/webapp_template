import { Component } from '@angular/core';
import { UserService } from './services/user/user.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'web-client';
  user: string

  constructor(private userService: UserService) {
    this.userService.get(1).subscribe(
      data => {
        this.user = data;
      }, 
      error => {
        console.log(error)
        console.log("Didn't get user")
      }
    )
  }
}
