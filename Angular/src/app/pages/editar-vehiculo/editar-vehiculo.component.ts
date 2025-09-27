import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { VehiculoService } from 'src/app/service/vehiculo.service';

@Component({
  selector: 'app-editar-vehiculo',
  templateUrl: './editar-vehiculo.component.html',
  styleUrls: ['./editar-vehiculo.component.css']
})
export class EditarVehiculoComponent implements OnInit {
  vehiculoForm!: FormGroup;
  vehiculoId!: number;

  constructor(
    private fb: FormBuilder,
    private vehiculoService: VehiculoService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    // Tomar el id desde la URL
    this.vehiculoId = Number(this.route.snapshot.paramMap.get('id'));

    // Inicializar formulario
    this.vehiculoForm = this.fb.group({
      marca: ['', Validators.required],
      modelo: ['', Validators.required],
      categoria: ['', Validators.required],
      tipo: ['', Validators.required],
      anio_fabricacion: ['', [Validators.required, Validators.min(1900), Validators.max(new Date().getFullYear())]]
    });

    // Cargar datos del vehículo
    this.vehiculoService.getVehiculo(this.vehiculoId).subscribe({
      next: (data) => {
        this.vehiculoForm.patchValue(data);
      },
      error: (err) => {
        console.error('Error al obtener vehículo', err);
      }
    });
  }

  onSubmit(): void {
  if (this.vehiculoForm.valid) {
    // ✅ Si no se modificó nada, volver directo al perfil
    if (this.vehiculoForm.pristine) {
      this.router.navigate(['/perfil']);
      return;
    }

    // ✅ Si hubo cambios, actualizar y mostrar alerta
    this.vehiculoService.editarVehiculo(this.vehiculoId, this.vehiculoForm.value).subscribe({
      next: () => {
        alert('Vehículo actualizado correctamente');
        this.router.navigate(['/perfil']);
      },
      error: (err) => {
        console.error('Error al actualizar vehículo', err);
      }
    });
  }
}

}

