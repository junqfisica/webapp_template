import { Component, OnInit } from '@angular/core';
import { User } from 'src/app/model/model.user';
import { AuthService } from 'src/app/services/auth/auth.service';
import { NotificationService } from 'src/app/services/notification/notification.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  user: User = new User();
  constructor(private authService: AuthService, private notificationService: NotificationService) { }

  ngOnInit() {
  }

  login() {
    this.authService.login(this.user).subscribe(
      user => {
        if (user) {
          this.notificationService.showSuccessMessage("Logged in as " + user.username)
          console.log(user);
        } else {
          this.notificationService.showErrorMessage("Username or password don't match, try again.")
        }
      },
      error => {
        this.notificationService.showErrorMessage(error.message)
        console.log(error);
      }
    );
  }

}
