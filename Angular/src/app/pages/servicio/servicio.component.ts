import {OnInit,  Component} from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ServicioService } from 'src/app/service/servicio.service';
import {FormBuilder, FormControl, FormGroup, Validators} from '@angular/forms';

import { TokenService } from 'src/app/service/token.service'

@Component({
  selector: 'app-servicio',
  templateUrl: './servicio.component.html',
  styleUrls: ['./servicio.component.css']
})
export class ServicioComponent{

  servicios: any={};

  constructor(private miservicio: ServicioService, private activatedRouter: ActivatedRoute, private router: Router,private fb:FormBuilder,private tokenService: TokenService){
    const id = this.activatedRouter.snapshot.params['id'];
    let datos:any= {};
    this.miservicio.detail(id).subscribe(
      data => {
        this.servicios=data;
        console.log(this.servicios);
        
        
      }, err => {
        alert("Error al cargar");
        this.router.navigate(['']);
      }
    )


    this.completarDatos();
  }

  datos!:FormGroup;


  completarDatos(){
    this.datos=this.fb.group({
      nombre:['',[Validators.required, Validators.minLength(2)]],
      apellido:['',Validators.required],
      // correo:['',[Validators.required,Validators.pattern('[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$')]],
      correo:['',[Validators.required,Validators.email]],

      numero:['',[Validators.required, Validators.minLength(5)]],

    })
  }

  get Nombre(){
    return this.datos.get("nombre");
  }

  get Apellido(){
    return this.datos.get("apellido");
  }

  get Correo(){
    return this.datos.get("correo");
  }

  get Numero(){
    return this.datos.get("numero");
  }

  // enviarDatos(){
  //   console.log(this.datos);
  // }
  onEnviar(event:Event){
      // se verifica si el usuario esta logueado
  if (!this.tokenService.getToken()) {
    // Si no esta logueado, redirigimos a la página de login
    this.router.navigate(['/login']);
    return; // Salimos de la función para evitar agregar el producto al carrito
  }

    event.preventDefault;


    if (this.datos.valid) {
      alert("enviar datos al servidor");
    }else{
      this.datos.markAllAsTouched();
    }
    
  }
  

}

