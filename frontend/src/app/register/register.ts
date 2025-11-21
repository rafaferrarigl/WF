import { Component } from '@angular/core';
import {FormsModule, ReactiveFormsModule} from "@angular/forms";

@Component({
  selector: 'app-register',
    imports: [
        FormsModule,
        ReactiveFormsModule
    ],
  templateUrl: './register.html',
  styleUrl: './register.css',
})
export class Register {

}
