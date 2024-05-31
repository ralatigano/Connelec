let dataTable;
let dataTableIsInitilized=false;

const initDataTable=async() => {
    if(dataTableIsInitilized){
        dataTable.destroy();
    }
    dataTable=$("#Tareas").DataTable({
        language: {
            lengthMenu: 'Mostrar _MENU_ tareas por página',
            zeroRecords: 'No hay tareas registrados',
            info: 'Mostrando de _START_ a _END_ de _TOTAL_ tareas',
            infoEmpty: 'No hay tareas',
            InfoFiltered: '(filtrado de _MAX_ tareas totales)',
            search: 'Buscar:',
            LoadingRecords: 'Cargando...',
            paginate: {
                first: 'Primero',
                last: 'Ultimo',
                next: 'Siguiente',
                previous: 'Anterior'
            }
        },
        columnDefs: [ { targets: 6, type: 'date' } ],
        order: [[ 6, "desc" ]]
    });
    dataTableIsInitilized=true;
}

window.addEventListener("load", async() => {
    await initDataTable();
});

const editarTareaModal = document.getElementById('editarTareaModal')
editarTareaModal.addEventListener('show.bs.modal', async event => {
  //botón que lanza el modal
  const button = event.relatedTarget
  //obtengo el código del producto y su nombre para mostrarlo en el modal
  const recipient = button.getAttribute('data-bs-whatever')
  console.log(recipient);
  var partes = recipient.split('`');

  const nombre = partes[0];
  const descrip= partes[1];
  const encargado = partes[2];
  const estado = partes[3];
  const f_entrega = partes[4];
  const proyecto = partes[5];

  //cambio el texto del título del modal
  const modalTitle = editarTareaModal.querySelector('.modal-title')
  modalTitle.textContent = `Editar Tarea: ${nombre}`

  $("#nombre").val(nombre);
  $("#descrip").val(descrip);
  $("#estado").val(estado);
  $("#fecha_entrega").val(f_entrega);
  
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
  });
  
});

async function showEditarTareaModal(button){
    try{
        var response = await fetch(`/tareas/infoEditarTarea`);
        var data = await response.json();
        
        var cardContentUsus = `
            <option value="Ninguno">Ninguno</option>
            ${data.Usus.map(usu => `<option value="${usu.username}">${usu.username}</option>`).join('')}
        
        `;
        var modalBodyEncargado = document.getElementById('encargado');
        modalBodyEncargado.innerHTML = cardContentUsus;
        
        var cardContentProys = `
            <option value="Ninguno">Ninguno</option>
            ${data.Proys.map(proy => `<option value="${proy.nombre}">${proy.nombre}</option>`).join('')}
        
        `;
        var modalBodyProys = document.getElementById('proyecto');
        modalBodyProys.innerHTML = cardContentProys;
        
        
        var modal = new bootstrap.Modal(document.getElementById(editarTareaModal));
        modal.show();

    } catch(error){
        console.log('Error:', error);
    }
}