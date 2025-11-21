import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';

export interface User {
  user_id: number;
  username: string;
  is_admin: boolean;
  birth_date?: string;
  height?: number;
  weight?: number;
  gender?: string;
}

@Injectable({
  providedIn: 'root'
})
export class UserService {

  private me_url = 'http://127.0.0.1:8443/auth/me';
  private http = inject(HttpClient);

  getCurrentUser(): Observable<User | null> {

    // 🟡 En SSR window no existe, evitar error
    if (typeof window === 'undefined') {
      return of(null);
    }

    return this.http.get<User>(this.me_url, {
      withCredentials: true    // 🟢 Se envía la cookie automáticamente
    });
  }
}
