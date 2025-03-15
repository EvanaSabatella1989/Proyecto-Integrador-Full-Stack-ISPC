import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ServicioService } from 'src/app/service/servicio.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { TokenService } from 'src/app/service/token.service';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-servicio',
  templateUrl: './servicio.component.html',
  styleUrls: ['./servicio.component.css']
})
export class ServicioComponent implements OnInit {

  servicioForm!: FormGroup;
  servicio: any = {}; // Información del servicio seleccionado
  sucursales: any[] = []; // Sucursales disponibles
  horariosDisponibles: string[] = []; // Horarios disponibles para la sucursal y fecha seleccionadas
  mensaje: string = ''; // Mensaje para mostrar al usuario

  constructor(
    private miservicio: ServicioService,
    private activatedRouter: ActivatedRoute,
    private router: Router,
    private fb: FormBuilder,
    private tokenService: TokenService,
    private http: HttpClient
  ) {}

  ngOnInit(): void {
    this.inicializarFormulario();
    this.cargarServicio();
    this.cargarSucursales();
  }

  // Inicializar el formulario reactivo
  inicializarFormulario() {
    this.servicioForm = this.fb.group({
      nombre: ['', [Validators.required, Validators.minLength(2)]],
      email: ['', [Validators.required, Validators.email]],
      fecha_reserva: ['', Validators.required],
      hora_reserva: ['', Validators.required],
      sucursal: ['', Validators.required],
      servicio: ['', Validators.required], // Nombre del servicio
      servicioId: ['', Validators.required] // ID del servicio
    });

    // Escuchar cambios en la fecha y la sucursal para obtener horarios disponibles
    this.servicioForm.get('fecha_reserva')?.valueChanges.subscribe(() => this.obtenerHorariosDisponibles());
    this.servicioForm.get('sucursal')?.valueChanges.subscribe(() => this.obtenerHorariosDisponibles());
  }

  // Cargar detalles del servicio seleccionado
  cargarServicio() {
    const id = this.activatedRouter.snapshot.params['id'];
    this.miservicio.obtenerServicio(id).subscribe(
      data => {
        this.servicio = data;
        this.servicioForm.patchValue({
          servicio: this.servicio.nombre,
          servicioId: this.servicio.id
        });
      },
      err => {
        alert('Error al cargar el servicio');
        this.router.navigate(['']);
      }
    );
  }

  // Obtener la lista de sucursales
  cargarSucursales() {
    this.http.get('http://127.0.0.1:8000/api/sucursal/').subscribe(
      (data: any) => {
        this.sucursales = data;
      },
      error => {
        console.error('Error al cargar sucursales', error);
      }
    );
  }

  // Obtener horarios disponibles según la sucursal y fecha seleccionadas
  obtenerHorariosDisponibles() {
    const sucursalId = this.servicioForm.value.sucursal;
    const fecha = this.servicioForm.value.fecha_reserva;

    if (sucursalId && fecha) {
      this.http.get(`http://127.0.0.1:8000/api/disponibilidad/${sucursalId}/${fecha}/`)
        .subscribe(
          (data: any) => {
            this.horariosDisponibles = data.horarios;
          },
          error => {
            console.error('Error al obtener horarios disponibles', error);
            this.horariosDisponibles = [];
          }
        );
    }
  }

  // Método para reservar turno
  reservarTurno() {
    if (this.servicioForm.invalid) {
      return;
    }

    // Verificar si el usuario está logueado
    if (!this.tokenService.isValidToken()) {
      alert('Debes iniciar sesión antes de continuar');
      this.router.navigate(['/login']);
      return;
    }

    // Datos de la reserva
    const reservaData = {
      nombre: this.servicioForm.value.nombre,
      email: this.servicioForm.value.email,
      fecha_reserva: this.servicioForm.value.fecha_reserva,
      hora_reserva: this.servicioForm.value.hora_reserva,
      servicio: this.servicioForm.value.servicioId,
      sucursal: this.servicioForm.value.sucursal
    };

    // Enviar la reserva al backend
    this.http.post('http://127.0.0.1:8000/api/reserva/', reservaData).subscribe(
      () => {
        this.mensaje = '✅ Reserva realizada con éxito';
        setTimeout(() => {
          this.router.navigate(['servicios/']);
        }, 3000);
      },
      error => {
        console.error('Error al realizar la reserva', error);
        if (error.error?.non_field_errors) {
          this.mensaje = '❌ ' + error.error.non_field_errors[0];
        } else {
          this.mensaje = '❌ Hubo un error, por favor intenta nuevamente';
        }
      }
    );
  }
}

// import { Component, OnInit } from '@angular/core';
// import { ActivatedRoute, Router } from '@angular/router';
// import { ServicioService } from 'src/app/service/servicio.service';
// import { FormBuilder, FormGroup, Validators } from '@angular/forms';
// import { TokenService } from 'src/app/service/token.service';
// import { HttpClient, HttpHeaders } from '@angular/common/http';

// @Component({
//   selector: 'app-servicio',
//   templateUrl: './servicio.component.html',
//   styleUrls: ['./servicio.component.css']
// })
// export class ServicioComponent implements OnInit {

//   servicioForm!: FormGroup;
//   servicio: any = {}; //información del servicio seleccionado
//   servicios: any = {}; //listado de servicios
//   sucursales: any[] = []; //sucursales disponibles
//   nombre: string = '';
//   email: string = '';
//   // telefono: number = 0;
//   fecha: string = new Date().toISOString().split('T')[0];

//   constructor(
//     private miservicio: ServicioService,
//     private activatedRouter: ActivatedRoute,
//     private router: Router,
//     private fb: FormBuilder,
//     private tokenService: TokenService,
//     private http: HttpClient
   
//   ) {
//     //cargar los detalles del servicio elegido
//     const id = this.activatedRouter.snapshot.params['id'];
//     this.miservicio.obtenerServicio(id).subscribe(
//       data => {
//         this.servicios = data;
//         //cargar el servicio seleccionado en el formulario
//         this.servicioForm.patchValue({
//           servicio: this.servicios.nombre, //enviamos el nombre solo para mostrarlo en el formulario
//           servicioId: this.servicios.id //se manda el ID del servicio
//         });
//       },
//       err => {
//         alert('Error al cargar el servicio');
//         this.router.navigate(['']);
//       }
//     );
//   }

//   ngOnInit(): void {
//     //obtener las sucursales disponibles
//     this.http.get('http://127.0.0.1:8000/api/sucursal/').subscribe(
//       (data: any) => {
//         this.sucursales = data;
//       },
//       error => {
//         console.error('Error al cargar sucursales', error);
//       }
//     );

//     //inicializar el formulario reactivo
//     this.servicioForm = this.fb.group({
//       nombre: ['', [Validators.required, Validators.minLength(2)]],
//       email: ['', [Validators.required, Validators.email]],
//       // telefono: ['', [Validators.required, Validators.pattern('^[0-9]{10}$')]],
//       fecha: ['', Validators.required],
//       // descripcion: [''],
//       sucursal: ['', Validators.required],
//       servicio: ['', Validators.required], //esto solo muestra el nombre
//       servicioId: ['', Validators.required] //este campo contiene el ID que enviamos al backend
//     });
//   }

//   // metodo para reservar turno
//   reservarTurno() {
//     if (this.servicioForm.invalid) {
//       console.log(this.servicioForm.value);
//       return;
//     }

//     //verificar si el token es valido (usuario logueado y token no expirado)
//     if (!this.tokenService.isValidToken()) {
//       alert('Debes iniciar sesión antes de continuar');
//       this.router.navigate(['/login']); //redirige a login si no hay token válido
//       return; //detiene el envío
//     }

//     //convertir la fecha al formato adecuado
//     const fechaTurno = new Date(this.servicioForm.value.fecha);
//     const fechaISO = fechaTurno.toISOString().slice(0, 16);

//     //crear el objeto de reserva con los datos del formulario
//     const reservaData = {
//       nombre: this.servicioForm.value.nombre,
//       email: this.servicioForm.value.email,
//       // telefono: this.servicioForm.value.telefono,
//       fecha: fechaISO,
//       // descripcion: this.servicioForm.value.descripcion,
//       servicio: this.servicioForm.value.servicioId, //enviamos el ID del servicio
//       sucursal: this.servicioForm.value.sucursal
//     };

//     //enviar la reserva al backend
//     this.http.post('http://127.0.0.1:8000/api/reserva/', reservaData).subscribe(
//       () => {
//         alert('✅ Reserva realizada con éxito');
//         this.router.navigate(['servicios/']);
//       },
//       error => {
//         console.error('Error al realizar la reserva', error);
//         alert('❌ Hubo un error, por favor intenta nuevamente');
//       }
//     );
//   }
// }
