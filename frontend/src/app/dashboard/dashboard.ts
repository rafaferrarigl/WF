import { Component } from '@angular/core';
import { UserService, User } from '../service/user';
import { CommonModule } from '@angular/common';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.css']
})
export class Dashboard {

  user$: Observable<User | null>;

  constructor(private userService: UserService) {
    this.user$ = this.userService.getCurrentUser();
  }
}
