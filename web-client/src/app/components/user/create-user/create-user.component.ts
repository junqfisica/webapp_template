import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

import { User } from '../../../model/model.user';
import { Role } from '../../../model/model.role';
import { UserService } from '../../../services/user/user.service';
import { NotificationService } from '../../../services/notification/notification.service';
import { AppValidador, UserValidador } from '../../../statics/form-validators';

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
      roleForm[role.role_id] = ['', {validators: [UserValidador.validateRoles(this.roles)], updateOn: 'change'}]
    }

    this.userForm = this.formBuilder.group({
      username: [null, {validators: [Validators.required], asyncValidators: [UserValidador.validateUsername(this.userService)], updateOn: 'change'}],
      firstName: ['', {validators: Validators.required, updateOn: 'change'}],
      lastName: ['', {validators: Validators.required, updateOn: 'change'}],
      password: ['', {validators: [Validators.required, Validators.minLength(this.passwordMinLenght)], updateOn: 'change'}],
      confirmPassword: ['', {validators: [AppValidador.match("password")], updateOn: 'change'}],
      roles: this.formBuilder.group(roleForm)
    });

  }

  get rolesForm (): FormGroup {return <FormGroup> this.userForm.get("roles")}


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
    
    this.userService.createUser(user).subscribe(
      wasCreated => {
        if (wasCreated) {
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
