let dataTable;
let dataTableIsInitilized=false;

const initDataTable=async() => {
    if(dataTableIsInitilized){
        dataTable.destroy();
    }
    dataTable=$("#tabla_registros").DataTable({
        language: {
            lengthMenu: 'Mostrar _MENU_ registros por página',
            zeroRecords: 'No hay registros guardados',
            info: 'Mostrando de _START_ a _END_ de _TOTAL_ registros',
            infoEmpty: 'No hay presupuestos',
            InfoFiltered: '(filtrado de _MAX_ registros totales)',
            search: 'Buscar:',
            LoadingRecords: 'Cargando...',
            paginate: {
                first: 'Primero',
                last: 'Ultimo',
                next: 'Siguiente',
                previous: 'Anterior'
            }
        },
        columnDefs: [ { targets: 3, type: 'date' } ],
        order: [[ 3, "desc" ]]
    });
    dataTableIsInitilized=true;
}

window.addEventListener("load", async() => {
    await initDataTable();
});

// (function () {
//     const btnEliminacion = document.querySelectorAll(".btnEliminacion");
//     btnEliminacion.forEach(btn=>{
//         btn.addEventListener("click", (e)=>{
//             const confirmacion = confirm("¿Está segur@ de que desea eliminar este elemento?");
//             if(!confirmacion){
//                 e.preventDefault();
//             }    
//         });
//     });
// })();

(function () {
    const btnEliminacion = document.querySelectorAll(".btnEliminacion");
    btnEliminacion.forEach(btn => {
        btn.addEventListener("click", (e) => {
            const recipient = btn.getAttribute('data-bs-whatever');
            var partes = recipient.split('`');

            const requestUser = partes[0];
            const nombre = partes[1];
            if (nombre === requestUser) {
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

// function mostrarValores(request) {
//     const recipient = document.querySelector('.btnEliminacion').getAttribute('data-bs-whatever');
//     var partes = recipient.split('`');

//     const requestUser = partes[0];
//     const nombre = partes[1];

//     const cartel = document.createElement('div');
//     cartel.classList.add('alert', 'alert-info');
//     cartel.textContent = `Dueño del registro: ${nombre}\nrequest.user.username: ${requestUser}`;

//     document.body.appendChild(cartel);
// }

// mostrarValores();

const editarRegistroModal = document.getElementById('editarRegistroModal')
editarRegistroModal.addEventListener('show.bs.modal', async event => {
  //botón que lanza el modal
  const button = event.relatedTarget
  //   {{r.id}}`{{r.nombre_completo}}`{{r.fecha}}`{{r.hora}}
  
  const recipient = button.getAttribute('data-bs-whatever')
  //console.log(recipient);
  var partes = recipient.split('`');

  const id = partes[0];
  const nombre = partes[1];
  const fecha = partes[2];
  const hora = partes[3];
  const tipo = partes[4];
  const requestUser = partes[5];
  const usuario = partes[6];
  
// Comprueba si el usuario tiene permisos para editar el registro
  if (usuario !== requestUser && String(requestUser) !== 'superusuario') {
    // El usuario no tiene permisos para editar el registro
    alert("No tienes permiso para editar este registro.");
    event.preventDefault();
    return;
  }
  
  //Muestra el modal si el usuario tiene permisos
  const modalTitle = editarRegistroModal.querySelector('.modal-title')
  modalTitle.textContent = `Editar registro de: ${nombre}`

  $("#id").val(id);
  $("#fecha").val(fecha);
  $("#hora").val(hora);
  $("#tipo").val(tipo);
  
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
  });
  
});


document.addEventListener('DOMContentLoaded', function() {
toggleFechaInputs(); // Llama a la función cuando se carga la página para configurar el texto correctamente
});

function toggleFechaInputs() {
    const toggle = document.getElementById('descargarTodo').checked;
    document.getElementById('fechaInputs').style.display = toggle ? 'block' : 'none';
    document.getElementById('toggleLabel').innerText = toggle ? 'Descargar registros entre fechas' : 'Descargar todos los registros';
}

function descargarAsistencias() {
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

    fetch('exportarRegistros', {
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
        a.download = `registros_${new Date().toISOString().slice(0,10)}.xlsx`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        }).catch(error => console.error('Error:', error));
}