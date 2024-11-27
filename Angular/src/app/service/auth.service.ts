import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Token } from '../models/token.model';
import { TokenService } from './token.service';
import { BehaviorSubject, tap } from 'rxjs';

interface LoginResponse extends Token {
  is_admin: boolean
}
@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private isLoggedInSubject = new BehaviorSubject<boolean>(false);
  isLoggedIn$ = this.isLoggedInSubject.asObservable();
  apiUrl = 'http://localhost:8000/api'
  constructor(
    private http: HttpClient,
    private tokenService: TokenService
  ) { }

  login(email: string, password: string) {

    return this.http.post<LoginResponse>(`${this.apiUrl}/login/`, {
      email,
      password
    })
    .pipe(
      tap(resp => {
        this.isLoggedInSubject.next(true)
        this.tokenService.createToken(resp.access_token)
      })
    )
  }

  register(first_name: string, last_name: string,email: string, password: string) {
    return this.http.post(`${this.apiUrl}/registro/`, {
      first_name,
      last_name,
      email,
      password
    })
  }

  logout(){
    this.tokenService.removeToken()
    
  }

  isLogged(){
    this.isLoggedInSubject.next(true)
  }
  isNotLogged(){
    this.isLoggedInSubject.next(false)
  }
}
