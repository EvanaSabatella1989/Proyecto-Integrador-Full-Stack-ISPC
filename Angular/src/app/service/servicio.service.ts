import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import {Observable} from 'rxjs';
import { Servicio } from '../models/servicio';


@Injectable({
  providedIn: 'root'
})
export class ServicioService {
// url2:string="http://localhost:8000/photos/photos/";
url:string="http://localhost:8000/api/"

 constructor(private http:HttpClient) { }

 ngOnInit(){}

//servicios
 obtenerServicios():Observable<any>{
    return this.http.get(this.url+"servicio");
    
  }

// servicio
// obtener servicio
  public detail(Id:number): Observable<any>{
    return this.http.get<any>(this.url + 'servicio/'+ Id);
  };

//alta de un servicio
public create(data:any):Observable<any>{
  let  servicio =new Servicio(data.nombre,data.descripcion,data.precio,data.fecha_creacion,data.imagen);
  
  return this.http.post(this.url+'servicio/',data);
} 

//actualizar servicio
public update(id:any,data:any): Observable<any>{
  return this.http.put(`${this.url}/${id}`,data);
}

//eliminar servicio
public delete(id:number):Observable<any>{
  return this.http.delete<Servicio>(this.url+'servicio/delete/'+id+'/');
}


  


  
}
