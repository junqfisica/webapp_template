import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, AbstractControl, ValidatorFn } from '@angular/forms';

import { debounceTime, distinctUntilChanged } from 'rxjs/operators'; 

import { User } from '../../../model/model.user';
import { Role } from '../../../model/model.role';
import { UserService } from '../../../services/user/user.service';
import { NotificationService } from '../../../services/notification/notification.service';
import { AppValidador } from '../../../statics/form-validators';


@Component({
  selector: 'app-create-user',
  templateUrl: './create-user.component.html',
  styleUrls: ['./create-user.component.css']
})
export class CreateUserComponent implements OnInit {
  userForm: FormGroup;
  submitted = false;
  passwordMinLenght = 6
  roles: Role[] = []
  hasUsername = false

  constructor(private formBuilder: FormBuilder, private userService: UserService, private notificationService: NotificationService) { 
    this.userService.getRoles().subscribe(
      roles=> {
        roles.forEach(role => {
          this.roles.push(role)
        });
        this.buildForm()
      }, 
      error => {
        console.log(error)
        notificationService.showErrorMessage(error.error.message)
      }
      
    );
  }

  ngOnInit() {
    
  }

  buildForm(){
    const roleForm = {}
    for (const role of this.roles){
      roleForm[role.role_id] = ['', {validators: [this.validadeRoles(this.roles)], updateOn: 'change'}]
    }

    this.userForm = this.formBuilder.group({
      username: ['', {validators: [Validators.required, this.validadeUsername()], updateOn: 'change'}],
      firstName: ['', {validators: Validators.required, updateOn: 'change'}],
      lastName: ['', {validators: Validators.required, updateOn: 'change'}],
      password: ['', {validators: [Validators.required, Validators.minLength(this.passwordMinLenght)], updateOn: 'change'}],
      confirmPassword: ['', {validators: [AppValidador.match("password")], updateOn: 'change'}],
      roles: this.formBuilder.group(roleForm)
    });

    // Regiter username valueChanges to check if username is already taken.
    this.userForm.get('username').valueChanges.pipe(
      debounceTime(200),
      // Avoid infinity loop.
      distinctUntilChanged())
      .subscribe(
        username => {
        this.checkUserAvailability(username)
      }
    );
  }

  get rolesForm (): FormGroup {return <FormGroup> this.userForm.get("roles")}

  validadeRoles (roles : Role[]): ValidatorFn {
    return (control: AbstractControl): { [key: string]: boolean } | null => {
      // console.log(control);
      
      for (const role of roles){
        if (role.selected) {
          return null
        }
      }
      return { 'notSelected': true }
    };
  }

  checkUserAvailability(username: string){
    if(username) {
      this.userService.isUsernameTaken(username).subscribe(
        isTaken => {
          this.hasUsername = isTaken
          this.f.username.updateValueAndValidity()          
        }, 
        error => {
          console.error(error);
          this.notificationService.showErrorMessage(error.error.message)
        }
      );
    }
  }

  validadeUsername (): ValidatorFn {
    return (control: AbstractControl): { [key: string]: boolean } | null => {
      if(this.hasUsername) {
        return { 'isTaken': true }
      }
      return null 
    };
  }

  onToogleRole(role: Role) {
    role.selected = !role.selected

    if (role.role_id == "ROLE_ADMIN" && role.selected) {
      this.roles.forEach(role => {
        if (role.role_id != "ROLE_ADMIN"){
          this.rolesForm.get(role.role_id).disable()
        }
        role.selected = true}
      )
    } else if (role.role_id == "ROLE_ADMIN" && !role.selected){
      this.roles.forEach(role =>  this.rolesForm.get(role.role_id).enable())
    }

    // Force validation of roles to sync. 
    this.roles.forEach(role => {      
      this.rolesForm.get(role.role_id).updateValueAndValidity()
    })
    
  }

  // convenience getter for easy access to form fields
  get f() { return this.userForm.controls }
  get roleControls() { return this.rolesForm.controls}

  private formToUser(): User{
    const user = new User()
    user.id = null
    user.token = null
    user.username = this.f.username.value
    user.name = this.f.firstName.value
    user.surname = this.f.lastName.value
    user.password = this.f.password.value
    return user
  }

  addRoles(user: User) {
    this.roles.forEach(role => {
      if (role.selected){
        user.roles.push(role.role_id)
      }
    })
  }

  onSubmit() {
    this.submitted = true;
    
    // Validade confirmPassowrd before submit.
    this.f.confirmPassword.updateValueAndValidity()

    // stop here if form is invalid
    if (this.userForm.invalid) {
        return;
    }

    const user = this.formToUser();
    this.addRoles(user)

    console.log(user)
    this.userService.createUser(user).subscribe(
      wasCreated => {
        if (wasCreated) {
          console.log("User created.")
          this.notificationService.showSuccessMessage("User " + user.username + " was created.")
        } else {
          console.log("Fail.")
          this.notificationService.showWarningMessage("Fail to create user. Check if this username already exists.")
        } 
      },
      error => {
        console.log(error)
        this.notificationService.showErrorMessage(error.error.message)
      } 
    );
  }

}
