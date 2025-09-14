import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService } from 'src/app/service/auth.service';
import { ServicioService } from 'src/app/service/servicio.service';
import { TokenService } from 'src/app/service/token.service';

@Component({
  selector: 'app-reserva',
  templateUrl: './reserva.component.html',
  styleUrls: ['./reserva.component.css']
})
export class ReservaComponent {
  reservaForm!: FormGroup;
  servicio: any = {};
  sucursales: any[] = [];
  turnosDisponibles: any[] = [];
  mensaje = '';
  diasDisponibles: string[] = [];
  clienteId?='';

 constructor(private authService: AuthService, private servicioService: ServicioService, 
  private fb: FormBuilder, private route: ActivatedRoute, 
  private router: Router, private tokenService: TokenService) { }

ngOnInit(): void {
    const servicioId = this.route.snapshot.params['id'];

     // cargar servicio
    this.servicioService.obtenerServicio(servicioId).subscribe(data => {
      this.servicio = data;
      this.reservaForm.patchValue({ servicio: this.servicio.id });
    });

    // cargar sucursales
    this.servicioService.obtenerSucursales().subscribe(data => {
      this.sucursales = data;
      console.log(data)
    });

     // Formulario
    this.reservaForm = this.fb.group({
      sucursal: ['', Validators.required],
      servicio: ['', Validators.required],
      turno: ['', Validators.required]
    });  
}

  alCambiarSucursal() {
   const sucursalId = this.reservaForm.value.sucursal;
  if (sucursalId) {
    this.servicioService.obtenerTurnosPorSucursal(sucursalId).subscribe(turnos => {
      console.log("Turnos recibidos del backend:", turnos);
      this.turnosDisponibles = turnos;
      this.reservaForm.patchValue({ turno: '' }); // limpia 

      if (turnos.length === 0) {
        this.mensaje = '❌ Esta sucursal no tiene turnos disponibles';
      } else {
        this.mensaje = ''; // limpia mensaje si hay turnos
      }
    });
  }
  }

  // cuando cambia la fecha  se carga los turnos
  cargarTurnos() {
    const sucursalId = this.reservaForm.value.sucursal;
    const fecha = this.reservaForm.value.fecha;
    console.log(fecha + 'saber fecha');

    if (sucursalId && fecha) {
      this.servicioService.obtenerTurnosDisponibles(sucursalId, fecha).subscribe(turnos => {
        this.turnosDisponibles = turnos;
        this.mensaje = turnos.length === 0 ? '❌ No hay turnos disponibles en esa fecha' : '';
      });
    }
  }

  reservar() {
    console.log("➡️ Se ejecutó reservar()", this.reservaForm.value);
    const clienteId = this.authService.obtenerIdUsuario2(); // el ID del cliente logueado
    const servicioId = this.servicio.id;
    console.log(clienteId+"saberl el id del cliente")
    // if (this.reservaForm.invalid) return;

    // const clienteId = this.tokenService.getToken();

    const reserva = {
      cliente: clienteId,
      servicio: servicioId,
      turno: parseInt(this.reservaForm.value.turno, 10),   
      sucursal: parseInt(this.reservaForm.value.sucursal, 10),

    };
    console.log(this.reservaForm);
    this.servicioService.crearReserva(reserva).subscribe(
      res => {
        this.mensaje = '✅ Reserva creada con éxito';
        setTimeout(() => this.router.navigate(['/servicios']), 2000);
        console.log(reserva);
      },
      err => {
        this.mensaje = '❌ Error al crear la reserva';
      }
    );
  }

}
