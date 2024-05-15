let dataTable;
let dataTableIsInitilized=false;

const initDataTable=async() => {
    if(dataTableIsInitilized){
        dataTable.destroy();
    }
    dataTable=$("#Clientes").DataTable({
        language: {
            lengthMenu: 'Mostrar _MENU_ clientes por página',
            zeroRecords: 'No hay clientes registrados',
            info: 'Mostrando de _START_ a _END_ de _TOTAL_ clientes',
            infoEmpty: 'No hay clientes',
            InfoFiltered: '(filtrado de _MAX_ clientes totales)',
            search: 'Buscar:',
            LoadingRecords: 'Cargando...',
            paginate: {
                first: 'Primero',
                last: 'Ultimo',
                next: 'Siguiente',
                previous: 'Anterior'
            }
        }
    });
    dataTableIsInitilized=true;
}

window.addEventListener("load", async() => {
    await initDataTable();
    document.getElementById("nav_item_clientes").style.fontWeight = "bold";
});


const editarClienteModal = document.getElementById('editarClienteModal')
editarClienteModal.addEventListener('show.bs.modal', event => {
  //botón que lanza el modal
  const button = event.relatedTarget
  //obtengo el código del producto y su nombre para mostrarlo en el modal
  const recipient = button.getAttribute('data-bs-whatever')
  console.log(recipient);
  var partes = recipient.split('|');

  //{{c.nombre}}|{{c.razon_social}}|{{c.cuit}}|{{c.telefono}}|{{c.email}}|{{c.direccion}}|{{c.provincia}}
  const nombre = partes[0];
  const razon_social = partes[1];
  const cuit = partes[2];
  const telefono = partes[3];
  const email = partes[4];
  const direccion = partes[5];
  const provincia = partes[6];

  //cambio el texto del título del modal
  const modalTitle = editarClienteModal.querySelector('.modal-title')
  modalTitle.textContent = `Editar Cliente: ${nombre}`

  $("#id").val(id);
  $("#nombre").val(nombre);
  $("#razon_social").val(razon_social);
  $("#cuit").val(cuit);
  $("#telefono").val(telefono);
  $("#email").val(email);
  $("#direccion").val(direccion);
  $("#provincia").val(provincia);

  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
  });

});