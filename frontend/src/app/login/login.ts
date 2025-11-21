import { Component } from '@angular/core';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../service/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './login.html',
  styleUrls: ['./login.css']
})
export class Login {

  form: any;

  constructor(
    private auth: AuthService,
    private router: Router,
    private fb: FormBuilder
  ) {
    this.form = this.fb.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    });
  }

  login() {
    if (this.form.invalid) return;

    const username = this.form.value.username!;
    const password = this.form.value.password!;

    this.auth.login(username, password).subscribe({
      next: () => {
        this.auth.me().subscribe({
          next: (user: any) => {
            console.log("Usuario autenticado:", user);
            if (user.is_admin) {
              this.router.navigate(['/dashboardadmin']);
            } else {
              this.router.navigate(['/dashboard']);
            }
          },
          error: (err) => console.error("Error obteniendo usuario:", err)
        });
      },
      error: (err) => console.error('Login falló', err)
    });
  }
}
