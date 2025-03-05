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

  servicioForm!: FormGroup;
  servicio: any = {}; //información del servicio seleccionado
  servicios: any = {}; //listado de servicios
  sucursales: any[] = []; //sucursales disponibles
  nombre: string = '';
  email: string = '';
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
    //cargar los detalles del servicio elegido
    const id = this.activatedRouter.snapshot.params['id'];
    this.miservicio.obtenerServicio(id).subscribe(
      data => {
        this.servicios = data;
        //cargar el servicio seleccionado en el formulario
        this.servicioForm.patchValue({
          servicio: this.servicios.nombre, //enviamos el nombre solo para mostrarlo en el formulario
          servicioId: this.servicios.id //se manda el ID del servicio
        });
      },
      err => {
        alert('Error al cargar el servicio');
        this.router.navigate(['']);
      }
    );
  }

  ngOnInit(): void {
    //obtener las sucursales disponibles
    this.http.get('http://127.0.0.1:8000/api/sucursal/').subscribe(
      (data: any) => {
        this.sucursales = data;
      },
      error => {
        console.error('Error al cargar sucursales', error);
      }
    );

    //inicializar el formulario reactivo
    this.servicioForm = this.fb.group({
      nombre: ['', [Validators.required, Validators.minLength(2)]],
      email: ['', [Validators.required, Validators.email]],
      telefono: ['', [Validators.required, Validators.pattern('^[0-9]{10}$')]],
      fecha: ['', Validators.required],
      descripcion: [''],
      sucursal: ['', Validators.required],
      servicio: ['', Validators.required], //esto solo muestra el nombre
      servicioId: ['', Validators.required] //este campo contiene el ID que enviamos al backend
    });
  }

  // metodo para reservar turno
  reservarTurno() {
    if (this.servicioForm.invalid) {
      console.log(this.servicioForm.value);
      return;
    }

    //verificar si el token es valido (usuario logueado y token no expirado)
    if (!this.tokenService.isValidToken()) {
      alert('Debes iniciar sesión antes de continuar');
      this.router.navigate(['/login']); //redirige a login si no hay token válido
      return; //detiene el envío
    }

    //convertir la fecha al formato adecuado
    const fechaTurno = new Date(this.servicioForm.value.fecha);
    const fechaISO = fechaTurno.toISOString().slice(0, 16);

    //crear el objeto de reserva con los datos del formulario
    const reservaData = {
      nombre: this.servicioForm.value.nombre,
      email: this.servicioForm.value.email,
      telefono: this.servicioForm.value.telefono,
      fecha: fechaISO,
      descripcion: this.servicioForm.value.descripcion,
      servicio: this.servicioForm.value.servicioId, //enviamos el ID del servicio
      sucursal: this.servicioForm.value.sucursal
    };

    //enviar la reserva al backend
    this.http.post('http://127.0.0.1:8000/api/reserva/', reservaData).subscribe(
      () => {
        alert('✅ Reserva realizada con éxito');
        this.router.navigate(['servicios/']);
      },
      error => {
        console.error('Error al realizar la reserva', error);
        alert('❌ Hubo un error, por favor intenta nuevamente');
      }
    );
  }
}
