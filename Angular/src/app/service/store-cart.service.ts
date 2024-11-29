import { Injectable } from '@angular/core';
import {BehaviorSubject} from 'rxjs'
import { Producto } from '../models/product.model';

@Injectable({
  providedIn: 'root'
})
export class StoreCartService {
  private myShoppingCart: Producto[]= [];
  private myCart = new BehaviorSubject<Producto[]>([]);

  myCart$ = this.myCart.asObservable();
  totalCart = 0;

  constructor(){
    const storageCart = sessionStorage.getItem('cart')
    if(storageCart){
      this.myShoppingCart = JSON.parse(storageCart)
      this.myCart.next(this.myShoppingCart)
    }
  }
  addProduct(product: Producto) {
    this.myShoppingCart.push(product)
    this.saveProduct()
  }
  
  getShoppingCart() {
    return this.myShoppingCart
  }
  getTotal() {
    return 1
  }

  deleteProduct(id:number) {
    this.myShoppingCart = this.myShoppingCart.filter(p => p.id !== id)
    this.saveProduct()
  }

  updateQuality(id: number, cantidad: number) {
    this.myShoppingCart = this.myShoppingCart.map(p => {
      if(p.id === id){
        return {
          ...p,
          cantidad: cantidad
        }
      }
      return p
    })
    console.log(this.myShoppingCart)
    this.saveProduct()
  }
  private saveProduct() {
    sessionStorage.setItem('cart', JSON.stringify(this.myShoppingCart))
    this.myCart.next(this.myShoppingCart);
  }

  isProductInCart(productId: number): boolean {
    return this.myShoppingCart.some(product => product.id === productId);
  }
}
