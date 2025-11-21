import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private login_url = 'http://127.0.0.1:8443/auth/login';
  private me_url = 'http://127.0.0.1:8443/auth/me';

  constructor(private http: HttpClient) {}

  login(username: string, password: string): Observable<any> {
    const body = new URLSearchParams();
    body.set('username', username);
    body.set('password', password);

    return this.http.post(this.login_url, body.toString(), {
      headers: new HttpHeaders({
        'Content-Type': 'application/x-www-form-urlencoded'
      }),
      withCredentials: true
    });
  }

  me(): Observable<any> {
    return this.http.get(this.me_url, {
      withCredentials: true
    });
  }
}
