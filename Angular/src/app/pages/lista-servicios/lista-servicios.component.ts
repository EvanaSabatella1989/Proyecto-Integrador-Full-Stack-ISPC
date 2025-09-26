import { Component } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { Servicio } from 'src/app/models/servicio';
import { ServicioService } from 'src/app/service/servicio.service';
declare var bootstrap: any;
@Component({
  selector: 'app-lista-servicios',
  templateUrl: './lista-servicios.component.html',
  styleUrls: ['./lista-servicios.component.css']
})
export class ListaServiciosComponent {

  miList: any;
  miServi: any;
  isLogged: boolean = false;
  isAdmin: boolean = false;  // verifica si el usuario es admin
  servicioActual: Servicio | null = null;
  servicioForm!: FormGroup;
  imagenSeleccionada?: File | null = null;
  modalInstance: any;
  nombre: string = '';
  descripcion: string = '';
  precio: number = 0;


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

  abrirModal(servicio?:Servicio){
    this.servicioActual=servicio || null;
    if(servicio){
       this.nombre = servicio.nombre ?? '';
      this.descripcion = servicio.descripcion ?? '';
      this.precio = servicio.precio;
    } else {
      this.nombre = '';
      this.descripcion = '';
      this.precio = 0;
      this.imagenSeleccionada = null;
    }

    const modalEl = document.getElementById('modalServicio');
    this.modalInstance = new bootstrap.Modal(modalEl);
    this.modalInstance.show();
  }

  seleccionarImagen(event: any): void {
    if (event.target.files.length > 0) {
      this.imagenSeleccionada = event.target.files[0];
    }
  }

  guardarServicio(){
     const formData = new FormData();
    formData.append('nombre', this.nombre);
    formData.append('descripcion', this.descripcion);
    formData.append('precio', this.precio.toString());

    if (this.imagenSeleccionada) {
      formData.append('imagen', this.imagenSeleccionada);
    }

    if (this.servicioActual?.id) {
      if (!window.confirm('Deseas actualizar este servicio?')) return;

      this.list.actualizarServicio(this.servicioActual.id, formData).subscribe({
        next: () => {
          alert('✅ Servicio actualizado con éxito');
          this.  listarServicios();
          this.modalInstance.hide();
        },
        error: (error) => {
          console.error(error);
          alert('❌ Error al actualizar servicio.');
        }
      });
  }
}

  delete(item: any) {
    if(window.confirm(`⚠️ Deseas eliminar el servicio :"${item.nombre}"?`)){
    this.miList.forEach((servicio: any) => {
      if (servicio.id == item.id) {
        alert('✅ Servicio eliminado con éxito');
        this.list.eliminarServicio(item.id).subscribe(
          res => this.list.obtenerServicios().subscribe(
            Response => this.miList = Response
          )
        );
        console.log('borre el servicio numero :' + item.id);
      }
    });
  }
  }
}
