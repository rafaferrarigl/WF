import { Routes } from '@angular/router';
import {Login} from './login/login';
import {Register} from './register/register';
import {Dashboard} from './dashboard/dashboard';
import {DashboardAdmin} from './dashboard-admin/dashboard-admin';

export const routes: Routes = [
  { path: "", redirectTo: "Login", pathMatch: "full" },
  {path: "Login", component: Login, pathMatch: "full"},
  {path: "Register", component: Register, pathMatch: "full"},
  {path: "dashboard", component: Dashboard, pathMatch: "full"},
  {path: "dashboardadmin", component: DashboardAdmin, pathMatch: "full"}

];
