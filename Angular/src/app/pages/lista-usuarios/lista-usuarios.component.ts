import { Component } from '@angular/core';
import { Cliente } from 'src/app/models/cliente';
import { AuthService } from 'src/app/service/auth.service';
import { ClienteService } from 'src/app/service/cliente.service';
declare var bootstrap: any;
@Component({
  selector: 'app-lista-usuarios',
  templateUrl: './lista-usuarios.component.html',
  styleUrls: ['./lista-usuarios.component.css']
})
export class ListaUsuariosComponent {

  clientes: Cliente[] = [];
  // para el modal
  clienteActual: Cliente | null = null;
  email?: string = '';
  first_name?: string = '';
  last_name?: string = '';
  password?: string = '';
  direccion?: string = '';
  num_telefono?: string = '';

  constructor(private clienteService: ClienteService, private authService: AuthService) { }

  ngOnInit(): void {
    this.cargarClientes();
  }

  cargarClientes() {
    this.clienteService.getClientes().subscribe(data => {
      this.clientes = data;
    });
  }


  eliminarCliente(id: number) {
    this.clienteService.deleteCliente(id).subscribe(() => {
      this.cargarClientes();
    });
  }

  abrirModal(cliente?: Cliente) {
    if (cliente) {

      // editar cliente
      this.clienteActual = cliente;
      this.email = cliente.email;
      this.first_name = cliente.first_name;
      this.last_name = cliente.last_name;
      this.direccion = cliente.direccion;
      this.num_telefono = cliente.num_telefono;
      this.password = ''; 
    } else {

      // crear cliente/usuario nuevo
      this.clienteActual = null;
      this.email = '';
        this.first_name = '';
      this.last_name = '';
      this.password = '';
      this.direccion = '';
      this.num_telefono = '';
    }

    // abrir modal
    const modalEl = document.getElementById('modalCliente');
    const modal = new bootstrap.Modal(modalEl!);
    modal.show();
  }

  guardarCliente() {
    if (this.clienteActual) {
      // actualizar usuario
      const updatedCliente: Cliente = {
        ...this.clienteActual,
        direccion: this.direccion,
        num_telefono: this.num_telefono
      };
      this.clienteService.updateCliente(this.clienteActual.id!, updatedCliente).subscribe({
        next: () => {
          this.cargarClientes();
          this.cerrarModal();
        },
        error: (err) => console.error(err)
      });
    } else {

      // crear usuario 
      this.authService.register(
        this.first_name!,
        this.last_name!,
        this.email!,
        this.password!
      ).subscribe({
        next: () => {
          this.cargarClientes();
          this.cerrarModal();
        },
        error: (err) => console.error(err)
      });
    }
  }
  // editarCliente(id: number, cliente: Cliente) {
  //   this.clienteService.updateCliente(id, cliente).subscribe({
  //     next: () => {
  //       console.log("Cliente actualizado correctamente");
  //       this.cargarClientes();
  //     },
  //     error: (err) => {
  //       console.error("Error al actualizar cliente:", err);
  //       
  //       alert("Ocurrió un error al actualizar el cliente");
  //     }
  //   });
  // }

  cerrarModal() {
    const modalEl = document.getElementById('modalCliente');
    const modal = bootstrap.Modal.getInstance(modalEl!);
    modal?.hide();
  }
}
