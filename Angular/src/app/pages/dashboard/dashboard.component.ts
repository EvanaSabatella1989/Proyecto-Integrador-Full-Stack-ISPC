import { Component, OnInit } from '@angular/core';
import { ServicioService } from 'src/app/service/servicio.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

  //para cargar los servicios dinamicamente
  servicios: any[] = [];

  constructor(private servicioService: ServicioService) { }

  ngOnInit(): void {
   this.cargarServicios();
    
  }

  cargarServicios():void{
    this.servicioService.obtenerServicios().subscribe({
   
      next:(todosServicios)=>this.servicios=todosServicios,
      
    
      error:(errorData)=>{
        console.error('error al cargas los servicios',errorData);
        
      }
    })
  }
  

}
