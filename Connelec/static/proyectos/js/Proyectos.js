let dataTable;
let dataTableIsInitilized=false;

const initDataTable=async() => {
    if(dataTableIsInitilized){
        dataTable.destroy();
    }
    dataTable=$("#Proyectos").DataTable({
        language: {
            lengthMenu: 'Mostrar _MENU_ proyectos por página',
            zeroRecords: 'No hay proyectos registrados',
            info: 'Mostrando de _START_ a _END_ de _TOTAL_ proyectos',
            infoEmpty: 'No hay proyectos',
            InfoFiltered: '(filtrado de _MAX_ proyectos totales)',
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
});


const editarProyectoModal = document.getElementById('editarProyectoModal')
editarProyectoModal.addEventListener('show.bs.modal', async event => {
  //botón que lanza el modal
  const button = event.relatedTarget
  //obtengo el código del producto y su nombre para mostrarlo en el modal
  const recipient = button.getAttribute('data-bs-whatever')
  var partes = recipient.split('`');

  const nombre = partes[0];
  const n_expediente= partes[1];

  $("#nombre").val(nombre);
  $("#n_expediente").val(n_expediente);
  
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
  });
  
});