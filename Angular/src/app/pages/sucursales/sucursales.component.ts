import { Component, OnInit } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { Sucursal } from '../../models/sucursal';
import { ServicioService } from 'src/app/service/servicio.service';



@Component({
  selector: 'app-sucursales',
  templateUrl: './sucursales.component.html',
  styleUrls: ['./sucursales.component.css']
})
export class SucursalesComponent implements OnInit {
  sucursales: Sucursal[] = []; 
  

  constructor(private sucursaleService: ServicioService,private sanitizer: DomSanitizer) { }

  ngOnInit() {
    this.sucursaleService.obtenerSucursales().subscribe((data: any[]) => {
      this.sucursales = data.map((item: any) => ({
        id: item.id,
        nombre: item.nombre,
        direccion: item.direccion,
        telefono: item.telefono,
        latitud: parseFloat(item.latitud),
        longitud: parseFloat(item.longitud),
        mapaUrl: this.sanitizer.bypassSecurityTrustResourceUrl(
          'https://www.google.com/maps/d/embed?mid=1SuapcyNcs8InyT3uud3cQwyXiE-h0Ls&ehbc=2E312F&ll=' + item.latitud + ',' + item.longitud
        )
      }));
    });
  }
  }




