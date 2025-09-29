import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { Servicio } from 'src/app/models/servicio';
import { AuthService } from 'src/app/service/auth.service';

import { ServicioService } from 'src/app/service/servicio.service';
import { TokenService } from 'src/app/service/token.service';
declare var bootstrap: any;

@Component({
  selector: 'app-servicios',
  templateUrl: './servicios.component.html',
  styleUrls: ['./servicios.component.css']
})
export class ServiciosComponent implements OnInit {

  miServi: any[] = [];
  serviciosFiltrados: any[] = [];
  isLogged: boolean = false;
  isAdmin: boolean = false;  // verifica si el usuario es admin
  servicioActual: Servicio | null = null;
  servicioForm!: FormGroup;
  imagenSeleccionada?: File | null = null;
  modalInstance: any;
  nombre: string = '';
  descripcion: string = '';
  precio: number = 0;
  categorias: any[] = [];
  categoriaSeleccionada: number | null = null;
  catSelec: any = { id: 0, nombre: 'Todos' };

  constructor(private tokenService: TokenService, private authService: AuthService, private serv: ServicioService, private activatedRouter: ActivatedRoute, private router: Router, private fb: FormBuilder) {

  }

   ngOnInit(): void {
    this.authService.isLoggedIn$.subscribe(resp => this.isLogged = resp);
    this.authService.isAdmin$.subscribe(isAdmin => this.isAdmin = isAdmin);

    // 🔹 Traer categorías de tipo servicio
    this.serv.obtenerCategorias('servicio').subscribe({
      next: (resp) => {
        this.categorias = resp;
        console.log("Categorías de servicios cargadas", this.categorias);
        this.cargarServicios();
      },
      error: (error) => {
        console.error("Error al traer categorías de servicios", error);
      }
    });

    
  }

  cargarServicios(): void {
  this.serv.obtenerServicios().subscribe({
    next: (serviciosTodos) => {
      this.miServi = serviciosTodos.map((s: any) => {
        const categoriaEncontrada = this.categorias.find((c: any) => c.id === s.categoria);
        return {
          ...s,
          categoriaNombre: categoriaEncontrada ? categoriaEncontrada.nombre : 'Sin categoría'
        };
      });

      // Por defecto mostramos todos
      this.serviciosFiltrados = [...this.miServi];
    },
    error: (errorData) => {
      console.error('Error cargando servicios', errorData);
      this.router.navigate(['']);
    }
  });
  
}


 filtrarPorCategoria(cat: any) {
  this.catSelec = cat;

  if (cat.id === 0) {
    // Todas las categorías
    this.serviciosFiltrados = [...this.miServi];
  } else {
    // Solo la seleccionada
    this.serviciosFiltrados = this.miServi.filter(s => s.categoria === cat.id);
  }
}


  irAReservar(servicioId: number) {
  if (!this.isLogged) {
    // si no esta logueado, lo mandamos al login
    alert('Debes iniciar sesión para reservar un servicio.');
    this.router.navigate(['/login']);
    return;
  }

  // si lo esta lo llevamos a la ruta de reserva
  this.router.navigate(['/servicios', servicioId, 'reservar']);
}

  // Modal
  abrirModal(servicio?: Servicio) {
    this.servicioActual = servicio || null;

    if (servicio) {
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

  guardarServicio() {
   if (!this.nombre?.trim() || !this.descripcion?.trim() || this.precio == null || !this.imagenSeleccionada) {
  alert('⚠️ Todos los campos excepto la imagen son obligatorios.');
  return;
}

    const formData = new FormData();
    formData.append('nombre', this.nombre);
    formData.append('descripcion', this.descripcion);
    formData.append('precio', this.precio.toString());

    if (this.categoriaSeleccionada) {
      formData.append('categoria', this.categoriaSeleccionada.toString());
    } else {
      alert("⚠️ Debes seleccionar una categoría");
      return;
    }

    if (this.imagenSeleccionada) {
      formData.append('imagen', this.imagenSeleccionada);
    }

    if (this.servicioActual?.id) {
      if (!window.confirm('¿Confirmas actualizar este servicio?')) return;

      this.serv.actualizarServicio(this.servicioActual.id, formData).subscribe({
        next: () => {
          alert('✅ Servicio actualizado con éxito');
          this.cargarServicios();
          this.modalInstance.hide();
        },
        error: (error) => {
          console.error(error);
          alert('❌ Error al actualizar servicio.');
        }
      });
    } else {
      if (!window.confirm('¿Confirmas crear este servicio?')) return;

      this.serv.crearServicio(formData).subscribe({
        next: () => {
          alert('✅ Servicio creado con éxito');
          console.log("categoria elegida:" + this.categoriaSeleccionada)
          this.cargarServicios();
          this.modalInstance.hide();
        },
        error: (error) => {
          console.error(error);
          console.log("categoria elegida:" + this.categoriaSeleccionada)
          alert('❌ Error al crear servicio.');
        }
      });
    }
  }

  // delete(item: Servicio) {
  //   if (window.confirm(`⚠️ ¿Seguro que deseas eliminar "${item.nombre}"?`)) {
  //     this.serv.eliminarServicio(item.id!).subscribe({
  //       next: () => {
  //         alert(`✅ Servicio "${item.nombre}" eliminado.`);
  //         this.cargarServicios();
  //       },
  //       error: (error) => {
  //         console.error('Error eliminando servicio:', error);
  //         alert('❌ No se pudo eliminar el servicio.');
  //       }
  //     });
  //   }
  // }

}