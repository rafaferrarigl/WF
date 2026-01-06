import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private login_url = 'https://rfg.stickm4n.dev/api/auth/login';
  private me_url = 'https://rfg.stickm4n.dev/api/auth/me';

  constructor(private http: HttpClient) {}

  login(username: string, password: string): Observable<any> {
    const body = new URLSearchParams();
    body.set('username', username);
    body.set('password', password);

    return this.http.post(this.login_url, body.toString(), {
      headers: new HttpHeaders({
        'Content-Type': 'application/x-www-form-urlencoded'
      })
    });
  }


  me(): Observable<any> {
    const token = localStorage.getItem('token');

    return this.http.get<any>(this.me_url, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
  }
}
