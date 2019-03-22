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
    this.userService.get("A7BU1ZBUgL").subscribe(
      data => {
        this.user = data;
        console.log(this.user)
      }, 
      error => {
        console.log(error)
        console.log("Didn't get user")
      }
    )

    this.userService.getAll().subscribe(
      data => {
        console.log(data)
      }, 
      error => {
        console.log(error)
        console.log("Didn't get user")
      }
    )

    this.userService.get_by_username("lucs").subscribe(
      data => {
        console.log(data)
      }, 
      error => {
        console.log(error)
        console.log("Didn't get user")
      }
    )
  }
}
