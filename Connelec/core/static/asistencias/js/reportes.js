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
        },
        columnDefs: [ { targets: 4, type: 'date' } ],
        order: [[ 4, "desc" ]]
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
  //{{r.id}}`{{r.informe}}`{{r.proyecto}}`{{fecha_num}}`{{r.hora}}`{{request.user}}`{{r.usuario}}
  const recipient = button.getAttribute('data-bs-whatever')
  console.log(recipient);
  var partes = recipient.split('`');

  const id = partes[0];
  const informe = partes[1];
  //const proyecto = partes[2];
  const fecha = partes[3];
  const hora = partes[4];
  const requestUser = partes[5];
  const usuario = partes[6];
  
// Comprueba si el usuario tiene permisos para editar el registro
  if (usuario !== requestUser && String(requestUser) !== 'superusuario') {
    // El usuario no tiene permisos para editar el registro
    alert("No tienes permiso para editar este registro.");
    event.preventDefault();
    return;
  }
  
  
  //cambio el texto del título del modal
  const modalTitle = editarReporteModal.querySelector('.modal-title')
  modalTitle.textContent = `Editar reporte del usuario: ${usuario}`

  $("#id").val(id);
  $("#informe").val(informe);
  $("#fecha").val(fecha);
  $("#hora").val(hora);

  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
  });
  
});

(function () {
    const btnEliminacion = document.querySelectorAll(".btnEliminacion");
    btnEliminacion.forEach(btn => {
        btn.addEventListener("click", (e) => {
            const recipient = btn.getAttribute('data-bs-whatever');
            var partes = recipient.split('`');
            const requestUser = partes[0];
            const nombre = partes[1];
            if (nombre === requestUser || String(requestUser) === 'superusuario') {
                const confirmacion = confirm("¿Está segur@ de que desea eliminar este elemento?");
                if(!confirmacion){
                    e.preventDefault();
                }
            } else {
                alert("No tienes permiso para eliminar este registro.");
                e.preventDefault();
            }
        });
    });
})();


async function showEditarReporteModal(button){
    try{
        var response = await fetch(`/tareas/infoEditarTarea`);
        var data = await response.json();
        
        const recipient = button.getAttribute('data-bs-whatever')
        var partes = recipient.split('`');
        const proyecto = partes[2]; 

        var cardContentProys = `
            <option value="${proyecto === 'None' ? 'Ninguno' : proyecto}">${proyecto === 'None' ? 'Ninguno' : proyecto}</option>
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

document.addEventListener('DOMContentLoaded', function() {
    toggleFechaInputs(); // Llama a la función cuando se carga la página para configurar el texto correctamente
    });
    
    function toggleFechaInputs() {
        const toggle = document.getElementById('descargarTodo').checked;
        document.getElementById('fechaInputs').style.display = toggle ? 'block' : 'none';
        document.getElementById('toggleLabel').innerText = toggle ? 'Descargar reportes entre fechas' : 'Descargar todos los reportes';
    }
    
    function descargarReportes() {
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const todos = document.getElementById('descargarTodo').checked ? 'false' : 'true';
        const fecha1 = document.getElementById('fecha1').value;
        const fecha2 = document.getElementById('fecha2').value;
    
        if (todos && (!fecha1 || !fecha2 || fecha1 > fecha2)) {
            alert('Por favor, selecciona fechas válidas.');
            return;
        }
    
        const form = new FormData();
        form.append('todos', todos);
        if (todos) {
            form.append('fecha1', fecha1);
            form.append('fecha2', fecha2);
        }
    
        fetch('exportarReportes', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            body: form
        }).then(response => response.blob())
            .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = `reportes_${new Date().toISOString().slice(0,10)}.xlsx`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            }).catch(error => console.error('Error:', error));
    }