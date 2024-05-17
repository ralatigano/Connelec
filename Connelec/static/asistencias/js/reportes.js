let dataTable;
let dataTableIsInitilized=false;

const initDataTable=async() => {
    if(dataTableIsInitilized){
        dataTable.destroy();
    }
    dataTable=$("#tabla_reportes").DataTable({
        language: {
            lengthMenu: 'Mostrar _MENU_ reportes por página',
            zeroRecords: 'No hay reportes guardados',
            info: 'Mostrando de _START_ a _END_ de _TOTAL_ reportes',
            infoEmpty: 'No hay presupuestos',
            InfoFiltered: '(filtrado de _MAX_ reportes totales)',
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


const editarReporteModal = document.getElementById('editarReporteModal')
editarReporteModal.addEventListener('show.bs.modal', async event => {
  //botón que lanza el modal
  const button = event.relatedTarget
  //obtengo el código del producto y su nombre para mostrarlo en el modal
  const id = button.getAttribute('data-bs-whatever')

  //cambio el texto del título del modal
  //const modalTitle = editarTareaModal.querySelector('.modal-title')
  //modalTitle.textContent = `Editar Tarea: ${nombre}`

  $("#id").val(id);
  
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
  });
  
});

async function showEditarReporteModal(button){
    try{
        var response = await fetch(`/tareas/infoEditarTarea`);
        var data = await response.json();
        //console.log(data);
        
        var cardContentProys = `
            <option value="Ninguno">Ninguno</option>
            ${data.Proys.map(proy => `<option value="${proy.nombre}">${proy.nombre}</option>`).join('')}
        `;
        var modalBodyProys = document.getElementById('proyecto');
        modalBodyProys.innerHTML = cardContentProys;
        
        
        var modal = new bootstrap.Modal(document.getElementById(editarReporteModal));
        modal.show();

    } catch(error){
        console.log('Error:', error);
    }
}