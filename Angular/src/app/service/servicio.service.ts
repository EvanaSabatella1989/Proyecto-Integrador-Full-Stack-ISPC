import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import {Observable} from 'rxjs';
import { Servicio } from '../models/servicio';
import { formatDate } from '@angular/common';


@Injectable({
  providedIn: 'root'
})
export class ServicioService {
// url2:string="http://localhost:8000/photos/photos/";
url:string="http://localhost:8000/api/servicios/"

 constructor(private http:HttpClient) { }

 ngOnInit(){}

 // obtener todos los servicios
 obtenerServicios(): Observable<any> {
  return this.http.get(this.url);
}

// obtener un servicio por ID
obtenerServicio(id: number): Observable<Servicio> {
  return this.http.get<Servicio>(`${this.url}${id}/`);
}

// crear un nuevo servicio (con imagen)
crearServicio(servicio: Servicio, imagen?: File): Observable<Servicio> {
  const formData = new FormData();
  formData.append('nombre', servicio.nombre ?? '');
  formData.append('descripcion', servicio.descripcion ?? '');
  formData.append('precio', servicio.precio ? servicio.precio.toString() : ''); // Asegura que sea string

  // solo agrega la imagen si existe
  if (imagen) {
    formData.append('imagen', imagen, imagen.name);
  }

  return this.http.post<Servicio>(this.url, formData);
}


// ctualizar un servicio
actualizarServicio(id: number, servicio: FormData, imagen?: File): Observable<Servicio> {
  const formData = new FormData();
  if (imagen) {
    formData.append('imagen', imagen);
  }

  return this.http.put<Servicio>(`${this.url}${id}/`, servicio);
}

// Eliminar un servicio
eliminarServicio(id: number): Observable<any> {
  return this.http.delete(`${this.url}${id}/`);
}

}

