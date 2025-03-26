import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ServicioService } from 'src/app/service/servicio.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { TokenService } from 'src/app/service/token.service';
import { HttpClient } from '@angular/common/http';
import { ChangeDetectorRef } from '@angular/core';
import { AuthService } from 'src/app/service/auth.service';

@Component({
  selector: 'app-servicio',
  templateUrl: './servicio.component.html',
  styleUrls: ['./servicio.component.css']
})
export class ServicioComponent implements OnInit {
  servicioForm!: FormGroup;
  servicio: any = {};
  reservaForm: FormGroup;
  sucursales: any[] = [];
  turnos: any[] = []
  clienteId = 1;  // id de usuario autenticado
  mensajeConfirmacion='';



  constructor(
    private miservicio: ServicioService,
    private activatedRouter: ActivatedRoute,
    private router: Router,
    private fb: FormBuilder,
    private tokenService: TokenService,
    private http: HttpClient,
    private authService: AuthService
  ) {
    //  this.clienteId = this.authService.getClienteId();

    this.reservaForm = this.fb.group({
      sucursal: [''],
      turno: ['']
    });
  }

  ngOnInit(): void {
    this.cargarServicio();
    this.cargarSucursales();
  }

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
 
  
  cargarSucursales() {
    this.miservicio.obtenerSucursales().subscribe(data => {
      this.sucursales = data;
    });
  }
  
  cargarTurnos() {
    const sucursalId = this.reservaForm.value.sucursal;
  console.log("Sucursal seleccionada:", sucursalId);

  if (sucursalId) {
    this.miservicio.obtenerTurnos(sucursalId).subscribe(
      (data) => {
        this.turnos = data;
        if (this.turnos.length === 0) {
          console.warn("No hay turnos disponibles para esta sucursal.");
        }
      },
      (error) => {
        console.error("Error al obtener turnos:", error);
      }
    );
  }
}

reservar() {
  // Verificar si el usuario está logueado
    if (!this.tokenService.isValidToken()) {
      alert('Debes iniciar sesión antes de continuar');
      this.router.navigate(['/login']);
      return;
    }
  const datosReserva = {
    cliente_id: this.clienteId,
    turno_id: this.reservaForm.value.turno,
    confirmado: true
  };

  // llamada al servicie para reservar el turno
  this.miservicio.reservarTurno(datosReserva).subscribe(
    (response) => {
      // mensaje de éxito si la reserva fue confirmada
      alert('Reserva confirmada. Revisa tu correo para más detalles.');
      this.router.navigate(['/servicios']);
    },
    (error) => {
      // si hay un error, significa que no se pudo reservar el turno
      if (error.status === 400 && error.error.error === 'Turno no disponible') {
        // mensaje cuando no hay turnos disponibles
        alert('Lo sentimos, no hay horarios disponibles para esa sucursal. Intenta con otro turno.');
      } else {
        // mensaje genérico de error
        alert('Hubo un error al reservar el turno. Intenta nuevamente.');
      }
    }
  );
  console.log(datosReserva);
}

  }

 
  // reservar() {tambien sirve para reservar
  //   const datosReserva = {
  //     cliente_id: this.clienteId,
  //     turno_id: this.reservaForm.value.turno,
  //     confirmado: true
  //   };

  //   this.miservicio.reservarTurno(datosReserva).subscribe(response => {
  //     alert('Reserva confirmada');
  //   });
  // }


 