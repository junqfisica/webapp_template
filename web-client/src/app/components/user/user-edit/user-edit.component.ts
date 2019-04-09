import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';

import { forkJoin } from 'rxjs';

import { NotificationService } from '../../../services/notification/notification.service';
import { UserService } from '../../../services/user/user.service';
import { User } from '../../../model/model.user';
import { Role } from '../../../model/model.role';
import { UserValidador } from '../../../statics/form-validators';

@Component({
  selector: 'app-user-edit',
  templateUrl: './user-edit.component.html',
  styleUrls: ['./user-edit.component.css']
})
export class UserEditComponent implements OnInit {

  user: User
  userForm: FormGroup;
  submitted = false;
  roles: Role[] = []

  constructor(private route: ActivatedRoute, private router: Router, private formBuilder: FormBuilder, 
    private notificationService: NotificationService, private userService: UserService) {
      this.route.params.subscribe(
        params => {
          if (params && params.id) {
            forkJoin(
              this.userService.get(params.id),
              this.userService.getRoles()
            ).subscribe(
              data => {
                this.user = data[0]
                this.roles = data[1]
                this.buildForm(this.user)
              },
              error => {
                this.notificationService.showErrorMessage(error.message)
                console.log(error);
              }
            )
          }
        },
        error => {
          console.log(error);
        }
      ); 
  }

  ngOnInit() {
  }

  buildForm(user: User){
    const roleForm = {}
    for (const role of this.roles){
      if (this.user.roles.includes(role.role_id)){
        role.selected = true
      }
      roleForm[role.role_id] = ['', {validators: [UserValidador.validateRoles(this.roles)], updateOn: 'change'}]
    }

    this.userForm = this.formBuilder.group({
      username: [this.user.username, {validators: [Validators.required], asyncValidators: [UserValidador.validateUsername(this.userService, 500, [this.user.username])], updateOn: 'change'}],
      firstName: [user.name, {validators: Validators.required, updateOn: 'change'}],
      lastName: [user.surname, {validators: Validators.required, updateOn: 'change'}],
      roles: this.formBuilder.group(roleForm)
    });
  }

  get f() { return this.userForm.controls }
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

  private formToUser(): User{
    this.user.username = this.f.username.value
    this.user.name = this.f.firstName.value
    this.user.surname = this.f.lastName.value
    return this.user
  }

  updateRoles(user: User) {
    // Clean roles
    user.roles = []
    // Add selected
    this.roles.forEach(role => {
      if (role.selected){
        user.roles.push(role.role_id)
      }
    })
  }

  onSubmit() {
    this.submitted = true;

    // stop here if form is invalid
    if (this.userForm.invalid) {
        return;
    }

    const user = this.formToUser();
    this.updateRoles(user)
    this.userService.updateUser(user).subscribe(
      wasUpdate => {
        if (wasUpdate) {
          this.notificationService.showSuccessMessage("User was update.")
          this.router.navigate(["/user/users"])
        } else {
          this.notificationService.showErrorMessage("Fail to update user.")
        }
      },
      error => {
        console.log(error);
        this.notificationService.showErrorMessage(error.message)
      }
    );
  }

}
