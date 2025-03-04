import { Component, OnInit } from '@angular/core';
import { Producto } from 'src/app/models/product.model';
import { RequestStatus } from 'src/app/models/statusrequest';
import { PayService } from 'src/app/service/pay.service';
import { StoreCartService } from 'src/app/service/store-cart.service';
import { ProductoService } from 'src/app/service/producto.service';
import { forkJoin } from 'rxjs';

@Component({
  selector: 'app-carrito',
  templateUrl: './carrito.component.html',
  styleUrls: ['./carrito.component.css']
})
export class CarritoComponent implements OnInit {
  cartItems: any[] = [];
  products: Producto[] = []
  status: RequestStatus = 'init'
  total_precio = 0
  constructor(
    private serviceStore: StoreCartService,
    private payService: PayService,
    private productService: ProductoService,
  ){

  }

  ngOnInit(): void {
      // this.serviceStore.myCart$.subscribe(products => {
      //   this.products = products
      //   const precio =  products.map(p => p.precio * (p.cantidad ?? 1)).reduce((a, b) => a + b, 0)
      //   this.total_precio = Number(Number.parseFloat(precio.toString()).toFixed(2))
      // })

      this.serviceStore.getCarrito();
  //     this.serviceStore.myCart$.subscribe(products => {
  //     this.products = products;

      
  //     console.log("Items: " + products)
  //     // forkJoin(products.map(p => this.productService.detail(p.producto))).subscribe(results => {
  //     //   console.log(results); 
  //     // });
  //     //agrego lo del precio pero no estoy segura (no se donde se ve el cambio)
  //     const precio =  products.map(p => p.precio * (p.cantidad ?? 1)).reduce((a, b) => a + b, 0)
      
  //     this.total_precio = Number(Number.parseFloat(precio.toString()).toFixed(2))
      
  // });
      this.serviceStore.myCart$.subscribe(items => {
       this.cartItems = items;
       console.log(this.cartItems)
       this.total_precio = items
         .map(item => item.producto.precio * item.cantidad)
          .reduce((acc, precio) => acc + precio, 0);
     });
  }

  preferenceMP(){
    this.status = 'loading'
    this.payService.preference(this.products)
    .subscribe({
      next: (resp) => {
        console.log(resp)
        window.location.replace(resp.init_point)
      },
      error: (error) => {
        this.status = 'failed'
        console.log(error)
      }
    })
  }

}
