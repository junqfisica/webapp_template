import { Component, OnInit, TemplateRef } from '@angular/core';
import { HttpParams } from '@angular/common/http';

import { Observable } from 'rxjs';
import { mergeMap, map } from 'rxjs/operators';

import { BsModalService, BsModalRef } from 'ngx-bootstrap/modal'
import { PageChangedEvent } from 'ngx-bootstrap/pagination';
import { TypeaheadMatch } from 'ngx-bootstrap/typeahead/';

import { UserService } from '../../../services/user/user.service';
import { NotificationService } from '../../../services/notification/notification.service';
import { ComponentUtils } from '../../component.utils';
import { User } from '../../../model/model.user';

@Component({
  selector: 'app-user-list',
  templateUrl: './user-list.component.html',
  styleUrls: ['./user-list.component.css']
})
export class UserListComponent extends ComponentUtils implements OnInit {

  deleteModalRef: BsModalRef | null;
  deleteUser: User;
  users: User[] = []
  page = 1;
  itemsPerPage = 10;
  totalItems = 0;
  dataSource: Observable<User>
  searchUsername: string
  typeaheadLoading: boolean

  constructor(private userService: UserService, private notificationService: NotificationService, private modalService: BsModalService) {
    super(notificationService) 
    this.searchUsers()

    // Search for user
    this.dataSource = Observable.create((observer: any) => {
      // Runs on every search
      observer.next(this.searchUsername);
    }).pipe(
      mergeMap((term: string) => this.userService.search(this.buildQueryParams(term))
      .pipe(
        // Map search result observable to result list.
        map((data) => {
          return data.result;
        }))
      )
    );
  }

  ngOnInit() {
  }

  buildQueryParams(username="", orderBy=""): HttpParams {
    const params = {};

    params['SearchBy'] = "username";
    params['SearchValue'] = username
    params['OrderBy'] = orderBy;
    params['OrderDesc'] = false
    params['Page'] = this.page;
    params['PerPage'] = this.itemsPerPage;

    return new HttpParams({ fromObject: params });
  }

  isCurrentUser(user: User): boolean {
    return this.currentUser.username == user.username
  }

  openDeleteModal(template: TemplateRef<any>, user: User) {
    this.deleteModalRef = this.modalService.show(template);
    this.deleteUser = user;
  }

  closeDeleteModal() {
    this.deleteModalRef.hide();
    this.deleteModalRef = null;
  }

  private removeUserFromList() {
    if (this.deleteUser) {
      const index = this.users.indexOf(this.deleteUser);
      if (index > -1) {
        this.users.splice(index, 1);
      }
    }
  }

  deleteUserFromModal() {
    this.userService.deleteUser(this.deleteUser).subscribe(
      wasDeleted => {
        if (wasDeleted) {
          this.notificationService.showSuccessMessage("User " + this.deleteUser.username + " has been deleted.")
          this.removeUserFromList()
        } else {
          this.notificationService.showWarningMessage("Fail to delete user " + this.deleteUser.username + ".")
        }
        this.deleteUser = null
        this.closeDeleteModal()
      },
      error => {
        console.log(error);
        this.notificationService.showErrorMessage(error.error.message)
        this.closeDeleteModal()    
      }
    )
  }

  pageChanged(event: PageChangedEvent) {
    this.page = event.page;
    this.searchUsers();
  }

  itemsPerPageChanged(itemsPerPage: number) {
    this.itemsPerPage = itemsPerPage;
    this.page = 1;
    this.searchUsers();
  }

  changeTypeaheadLoading(e: boolean): void {
    this.typeaheadLoading = e;
  }

  typeaheadOnSelect(e: TypeaheadMatch): void {
    this.searchUsers(e.value, "username");
  }

  searchUsers(username="", orderBy=""){
    this.userService.search(this.buildQueryParams(username, orderBy)).subscribe(
      data => {        
        this.totalItems = data.total
        this.users = data.result        
      },
      error => {
        console.log(error);
        this.notificationService.showErrorMessage(error.message)
      }      
    )
    
  }

}
