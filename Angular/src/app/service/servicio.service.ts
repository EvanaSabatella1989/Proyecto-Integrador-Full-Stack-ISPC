import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import {Observable} from 'rxjs';
import { Servicio } from '../models/servicio';
import { formatDate } from '@angular/common';
import { Sucursal } from '../models/sucursal';
import { Turno } from '../models/turno';

@Injectable({
  providedIn: 'root'
})
export class ServicioService {
// url2:string="http://localhost:8000/photos/photos/";
url:string="http://localhost:8000/api/servicios/"
urlDos:string="http://localhost:8000/api/reserva/"
urlTres:string="http://127.0.0.1:8000/api"
url4:string="http://127.0.0.1:8000/api/sucursal/"
urlTurno:string="http://127.0.0.1:8000/api/turnos/"

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



// lista de sucursales
  // obtenerSucursales(): Observable<any[]> {
  //   return this.http.get<any[]>(`${this.urlTres}/sucursal/`);
  // }
obtenerSucursales(): Observable<Sucursal[]> {
  return this.http.get<Sucursal[]>(`${this.urlTres}/sucursal/`);

}
  // turnos disponibles por sucursal y fecha
  obtenerTurnosDisponibles(sucursalId: number, fecha: string): Observable<any[]> {
    return this.http.get<any[]>(`${this.urlTres}/turnos/disponibles/?sucursal=${sucursalId}&fecha=${fecha}`);
  }

// crear reserva
  crearReserva(reserva: any): Observable<any> {
    const token = localStorage.getItem('token');
    if(!token){
      console.error('No hay token guardado');
    }
    return this.http.post(`${this.urlTres}/reservas/`,reserva,{
      headers:{Authorization:`Bearer ${token}`}
    });
    
  }

  // dias disponibles  de sucursales
 obtenerDiasDisponibles(sucursalId: number) {
  return this.http.get<{ dias_disponibles: string[] }>(
    `${this.urlTres}sucursal/${sucursalId}/dias-disponibles/`
  );
}

//turnos disponibles de por sucursal
obtenerTurnosPorSucursal(sucursalId: number) {
  return this.http.get<any[]>(`${this.urlTres}/turnos/disponibles-por-sucursal/?sucursal=${sucursalId}`);
}


// crud sucursal
createSucursal(sucursal: Sucursal): Observable<Sucursal> {
  return this.http.post<Sucursal>(this.url4, sucursal);
}

updateSucursal(id: number, sucursal: Sucursal): Observable<Sucursal> {
  return this.http.put<Sucursal>(`${this.url4}${id}/`, sucursal);
}

deleteSucursal(id: number): Observable<any> {
  return this.http.delete(`${this.url4}${id}/`);
}

//crud para turnos
  getTurnos(): Observable<Turno[]> {
    return this.http.get<Turno[]>(this.urlTurno);
  }

  createTurno(turno: Turno): Observable<Turno> {
    return this.http.post<Turno>(this.urlTurno, turno);
  }

  updateTurno(id: number, turno: Turno): Observable<Turno> {
    return this.http.put<Turno>(`${this.urlTurno}${id}/`, turno);
  }

  deleteTurno(id: number): Observable<any> {
    return this.http.delete(`${this.urlTurno}${id}/`);
  }
}

