import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ServicioService } from 'src/app/service/servicio.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { TokenService } from 'src/app/service/token.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';


@Component({
  selector: 'app-servicio',
  templateUrl: './servicio.component.html',
  styleUrls: ['./servicio.component.css']
})
export class ServicioComponent implements OnInit {

  servicioForm: FormGroup;
  servicio: any = {}; // Aquí almacenas la información del servicio seleccionado
  idServicio: number =0;
  servicios: any = {};  // Listado de servicios
 

  nombre: string = '';
  email: string = '';
  descripcion: string = '';
  telefono: number = 0;
  fecha: string = new Date().toISOString().split('T')[0];

  constructor(
    private miservicio: ServicioService,
    private activatedRouter: ActivatedRoute,
    private router: Router,
    private fb: FormBuilder,
    private tokenService: TokenService,
    private http: HttpClient
  ) {

    // constante que trae los datos del servicio elegido
    const id = this.activatedRouter.snapshot.params['id'];
    let datos:any= {};
    this.miservicio.obtenerServicio(id).subscribe(
      data => {
        this.servicios=data;
        console.log(this.servicios);
        console.log("servicio cargado con exito");
        
      }, err => {
        alert("Error al cargar");
        this.router.navigate(['']);
      }
    )

    //  formulario reactivo 
    this.servicioForm = this.fb.group({
      nombre: ['', [Validators.required, Validators.minLength(2)]],
      email: ['', [Validators.required, Validators.email]],
      telefono: ['', [Validators.required, Validators.minLength(5)]],
      fecha: ['', [Validators.required]],
      descripcion: ['']
    });

  }
  
  
  ngOnInit(): void {
    // Obtén el id del servicio desde la URL
    // this.idServicio = this.activatedRouter.snapshot.params['id'];

    // // Carga los detalles del servicio seleccionado
    // this.miservicio.obtenerServicio(this.idServicio).subscribe(
    //   data => {
    //     this.servicio = data;
    //     this.servicioForm.patchValue({
    //       nombre: this.servicio.nombre  // Pre-llena el campo nombre con el nombre del servicio seleccionado
    //     });
    //     console.log(this.servicio);
    //   },
    //   err => {
    //     alert('Error al cargar el servicio');
    //     this.router.navigate(['']);
    //   }
    // );

    this.servicioForm = this.fb.group({
      nombre: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      telefono: ['', [Validators.required, Validators.pattern('^[0-9]{10}$')]],
      fecha: ['', Validators.required],
      descripcion: ['']
    });
  }

  // metodo para guardar los datos e enviar el correo
  reservarTurno() {
    if (this.servicioForm.invalid) {
      alert('Por favor, completa todos los campos');
      console.log(this.servicioForm.value);
      return;
    }
  
    // verifica si el usuario está logueado
    if (!this.tokenService.getToken()) {
      alert('Debes iniciar sesión antes de continuar');
      this.router.navigate(['/login']);
      return;
    }
  
    // convertir la fecha al mismo formato que back
    const fechaTurno = new Date(this.servicioForm.value.fecha);
    const fechaISO = fechaTurno.toISOString().slice(0, 16); 
  
    // extrae los valores del formulario servicioForm.
    const reservaData = {
      nombre: this.servicioForm.value.nombre,
      email: this.servicioForm.value.email,
      telefono: this.servicioForm.value.telefono,
      fecha: fechaISO, 
      descripcion: this.servicioForm.value.descripcion
    };
  
    // envía los datos al backend
    this.http.post('http://127.0.0.1:8000/api/reserva/', reservaData).subscribe(
      () => {
        alert('✅ Reserva realizada con éxito, muy pronto se pondran en contacto contigo!');
        this.router.navigate(['servicios/']);
      },
      error => {
        console.error('Error al reservar turno', error);
        alert('❌ Hubo un error al realizar la reserva, prueba cargando nuevamente los datos');
      }
    );
  }
  
}
