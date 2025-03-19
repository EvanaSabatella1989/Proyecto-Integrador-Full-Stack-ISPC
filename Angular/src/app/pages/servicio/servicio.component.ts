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
  // Formularios reactivos y variables
  servicioForm!: FormGroup;
  servicio: any = {}; // información del servicio seleccionado
  sucursales: any[] = []; // Lista de sucursales
  mensaje: string = ''; // Mensaje para mostrar al usuario
  horariosDisponibles: any[] = [];

  constructor(
    private miservicio: ServicioService,
    private activatedRouter: ActivatedRoute,
    private router: Router,
    private fb: FormBuilder,
    private tokenService: TokenService,
    private http: HttpClient,
   
  ) { 
    
  }

  ngOnInit(): void {
    this.inicializarFormulario();
    this.cargarServicio();
    this.cargarSucursales();
   
  
  }

  // cargar detalles del servicio seleccionado
  cargarServicio() {
    const id = this.activatedRouter.snapshot.params['id'];
    this.miservicio.obtenerServicio(id).subscribe(
      data => {
        this.servicio = data;
        // Rellenar el formulario con el nombre y ID del servicio
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

  // inicializar formulario reactivo
  inicializarFormulario() {
    this.servicioForm = this.fb.group({
      nombre_cliente: ['', [Validators.required, Validators.minLength(2)]],
      correo_cliente: ['', [Validators.required, Validators.email]],
      sucursal: ['', Validators.required], // Sucursal seleccionada
      fecha_sucursal: ['', Validators.required], // Fecha de la reserva
      hora_sucursal: ['', Validators.required], // Horario disponible para la fecha y sucursal
      servicio: ['', Validators.required], // Nombre del servicio
      servicioId: ['', Validators.required] // ID del servicio
      
    });

    
   
  }
  

  // obtener lista de sucursales disponibles
  cargarSucursales() {
    this.miservicio.obtenerSucursales().subscribe(
      (data: any[]) => {
        this.sucursales = data;
        console.log('Sucursales:', data);  
      },
      error => {
        console.error('Error al cargar sucursales', error);
      }
    );
  }

// metodo que se ejecuta cuando se cambia la sucursal
  alCambiarSucursal() {
    const sucursalId = this.servicioForm.get('sucursal')?.value;
    if (sucursalId) {
      this.miservicio.obtenerHorariosDisponibles(sucursalId).subscribe(
        (horarios) => {
          if (horarios.length === 0) {
            this.mensaje = '❌ No hay disponibilidad de reservas para esta sucursal en este momento.';
            this.horariosDisponibles = []; // Limpiar los horarios disponibles
          } else {
            this.horariosDisponibles = horarios;
            this.mensaje = ''; // Limpiar mensaje de error si hay horarios
          }
        },
        (error) => {
          console.error('Error al obtener horarios', error);
          this.mensaje = 'Hubo un error al obtener la disponibilidad de horarios.';
        }
      );
    }
  }
  
// Método que se ejecuta cuando se selecciona una fecha y hora
alCambiarFecha(event: any) {
  // Buscar el horario seleccionado por su ID
  const horarioSeleccionado = this.horariosDisponibles.find(horario => horario.id === parseInt(event.target.value));

  if (horarioSeleccionado) {
    // Actualizar el valor de hora_sucursal y fecha_sucursal
    this.servicioForm.patchValue({
      hora_sucursal: horarioSeleccionado.id,
      fecha_sucursal: horarioSeleccionado.id // Aquí ponemos el ID de la fecha seleccionada
    });

    console.log('Hora seleccionada:', horarioSeleccionado.hora); // Verificar que la hora se asigna correctamente
  }
}



  // 🟢 7. Método para reservar turno
  reservarTurno() {
    console.log("Formulario enviado:", this.servicioForm.value); // Para ver los valores que se envían
  
    // Verificar si el formulario es inválido
    if (this.servicioForm.invalid) {
      console.log("El formulario es inválido");
      return;
    }
  
    // Verificar si el usuario está logueado
    if (!this.tokenService.isValidToken()) {
      alert('Debes iniciar sesión antes de continuar');
      this.router.navigate(['/login']);
      return;
    }
  
    // Datos de la reserva (se enviará solo el ID del horario)
    const reservaData = {
      nombre_cliente: this.servicioForm.value.nombre_cliente,
      correo_cliente: this.servicioForm.value.correo_cliente,
      hora_sucursal: this.servicioForm.value.hora_sucursal, // Aquí solo se manda el ID del horario
      fecha_sucursal:this.servicioForm.value.fecha_sucursal,
      servicio: this.servicioForm.value.servicioId,
      sucursal: this.servicioForm.value.sucursal
    };
  
    console.log("Datos de reserva enviados:", reservaData); // Verificamos los datos que se enviarán
  
    // Enviar la reserva al backend
    this.http.post('http://127.0.0.1:8000/api/reserva/', reservaData).subscribe(
      response => {
        console.log("Reserva exitosa:", response); // Verificamos si la respuesta es correcta
        this.mensaje = '✅ Reserva realizada con éxito';
        setTimeout(() => {
          this.router.navigate(['servicios/']); // Redirigir después de la reserva exitosa
        }, 3000);
      },
      error => {
        console.error('Error al realizar la reserva', error);
        this.mensaje = '❌ Hubo un error, por favor intenta nuevamente';
      }
    );
  }
  
}
