let dataTable;
let dataTableIsInitilized=false;

const initDataTable=async() => {
    if(dataTableIsInitilized){
        dataTable.destroy();
    }
    dataTable=$("#Entradas").DataTable({
        language: {
            lengthMenu: 'Mostrar _MENU_ entradas por página',
            zeroRecords: 'No hay entradas registrados',
            info: 'Mostrando de _START_ a _END_ de _TOTAL_ entradas',
            infoEmpty: 'No hay tareas',
            InfoFiltered: '(filtrado de _MAX_ entradas totales)',
            search: 'Buscar:',
            LoadingRecords: 'Cargando...',
            paginate: {
                first: 'Primero',
                last: 'Ultimo',
                next: 'Siguiente',
                previous: 'Anterior'
            }
        },
        columnDefs: [ { targets: 0, type: 'date' } ],
        order: [[ 0, "desc" ]]
    });
    dataTableIsInitilized=true;
}

window.addEventListener("load", async() => {
    await initDataTable();
});

(function () {
    const btnEliminacion = document.querySelectorAll(".btnEliminacion");
    btnEliminacion.forEach(btn=>{
        btn.addEventListener("click", (e)=>{
            const confirmacion = confirm("¿Está segur@ de que desea eliminar este elemento?");
            if(!confirmacion){
                e.preventDefault();
            }    
        });
    });
})();

const editarEntradaModal = document.getElementById('editarEntradaModal')
editarEntradaModal.addEventListener('show.bs.modal', async event => {
  //botón que lanza el modal
  const button = event.relatedTarget
  //obtengo el código del producto y su nombre para mostrarlo en el modal
  const recipient = button.getAttribute('data-bs-whatever')
  console.log(recipient);
  var partes = recipient.split('`');

  const id = partes[0];
  const proyecto = partes[1];
  const fecha = partes[2];
  const resumen = partes[3];
  
  //cambio el texto del título del modal
  const modalTitle = editarEntradaModal.querySelector('.modal-title')
  modalTitle.textContent = `Editar entrada del proyecto: ${proyecto}`

  $("#id").val(id);
  $("#fecha").val(fecha);
  $("#resumen").val(resumen);
  
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
  });
  
});