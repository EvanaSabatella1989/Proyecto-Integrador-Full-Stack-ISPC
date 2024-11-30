import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ServicioService } from 'src/app/service/servicio.service';
import { Servicio } from 'src/app/models/servicio';

@Component({
  selector: 'app-lista-servicios',
  templateUrl: './lista-servicios.component.html',
  styleUrls: ['./lista-servicios.component.css']
})
export class ListaServiciosComponent {

  miList: any;
  
   
  constructor(private list: ServicioService, private activatedRouter: ActivatedRoute, private router: Router) {

  }

  ngOnInit(): void {
    this.listarServicios()

  }

  listarServicios() {
    this.list.obtenerServicios().subscribe({
      next: (todaLaLista) => {
        this.miList = todaLaLista;
        console.log("cargo toda la lista");
        console.log(this.miList);
      },
      error: (errorData) => {
        console.log("no cargo lista");
        console.log(errorData);
        this.router.navigate(['']);
      }
    })
  }

  // delete(item:any){
  //   this.miList.forEach((servicio: any) => {
  //         if (servicio.id == item.id) {
  //           this.list.delete(item.id).subscribe(
  //               res=>this.list.obtenerServicios().subscribe(
  //               Response=>this.miList=Response
  //               )
  //           );
  //           console.log('borre el servicio numero :'+item.id);
  //         }
  //       });
  // }

  delete(item: any) {
    if (confirm(`¿Estás seguro de que deseas eliminar el servicio "${item.nombre}"?`)) {
      this.miList.forEach((servicio: any) => {
        if (servicio.id == item.id) {
          this.list.delete(item.id).subscribe({
            next: () => {
              // Actualizar la lista después de eliminar
              this.list.obtenerServicios().subscribe((Response) => {
                this.miList = Response;
              });
              console.log(`Se eliminó el servicio con ID: ${item.id}`);
            },
            error: (errorData) => {
              console.error('Error al eliminar el servicio:', errorData);
            },
          });
        }
      });
    } else {
      console.log('Eliminación del servicio cancelada por el usuario.');
    }
  }
    
  
  }