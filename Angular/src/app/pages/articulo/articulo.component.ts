import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService } from 'src/app/service/auth.service';
import { ProductoService } from 'src/app/service/producto.service';
import { StoreCartService } from 'src/app/service/store-cart.service';
import { TokenService } from 'src/app/service/token.service';

import {  Producto, Rating } from 'src/app/models/product.model';

@Component({
  selector: 'app-articulo',
  templateUrl: './articulo.component.html',
  styleUrls: ['./articulo.component.css']
})
export class ArticuloComponent implements OnInit {
  isLogged: boolean = false;
  productos: any = {};
  catSelec: any = {};

  id: string="";
  nombre: string ="";
  precio: string="";
  imagen: string="";
  descripcion: string="";
  categoria: string="";
  // cantidad: string="1";
  cantidad: number= 1;

  


  constructor(private tokenService: TokenService, private authService: AuthService, private miCarrito: StoreCartService, private miProductos: ProductoService, private activatedRouter: ActivatedRoute, private router: Router) {
    const id = this.activatedRouter.snapshot.params['id'];
    let datos: any = {};
    this.miProductos.detail(id).subscribe(
      data => {
        this.productos = data;


      }, err => {
        alert("Error al cargar");
        this.router.navigate(['']);
      }
    )


  }
  ngOnInit(): void {
    this.authService.isLoggedIn$.subscribe(resp => this.isLogged = resp)


  }

  guardarCantidad(event: any) {
    // this.cantidad=this.cantidad+1
    // console.log(this.cantidad = event.target.value)
    // return this.cantidad
    this.cantidad = parseInt(event.target.value, 10);
  }



  agregarCarrito() {
    this.productos.cantidad = this.cantidad;
    console.log(this.productos.id);
    console.log(this.productos.nombre);
    console.log(this.productos.descripcion);
    console.log(this.productos.precio);
    console.log(this.productos.date_created);
    console.log(this.productos.imagen);
    console.log(this.productos.cantidad)
    // let producto = this.productos;
    // producto.id = this.productos.id;

    this.miCarrito.addProduct(this.productos);
    this.router.navigate(['/carrito'])

  }


}
