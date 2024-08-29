let dataTable;
let dataTableIsInitilized=false;

const initDataTable=async() => {
    if(dataTableIsInitilized){
        dataTable.destroy();
    }
    dataTable=$("#Ausencias").DataTable({
        language: {
            lengthMenu: 'Mostrar _MENU_ ausencias por página',
            zeroRecords: 'No hay ausenciass guardadas',
            info: 'Mostrando de _START_ a _END_ de _TOTAL_ ausencias',
            infoEmpty: 'No hay ausencias',
            InfoFiltered: '(filtrado de _MAX_ ausencias totales)',
            search: 'Buscar:',
            LoadingRecords: 'Cargando...',
            paginate: {
                first: 'Primero',
                last: 'Ultimo',
                next: 'Siguiente',
                previous: 'Anterior'
            }
        },
    });
    dataTableIsInitilized=true;
}

window.addEventListener("load", async() => {
    await initDataTable();
});

(function () {
    const btnEliminacion = document.querySelectorAll(".btnEliminacion");
    btnEliminacion.forEach(btn => {
        btn.addEventListener("click", (e) => {
            const recipient = btn.getAttribute('data-bs-whatever');
            var partes = recipient.split('|');

            const requestUser = partes[1];
            const nombre = partes[0];
            const autorizado = (partes[2] === 'True');
            if (nombre === requestUser || autorizado) {
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

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('ausenciaModal').addEventListener('show.bs.modal', function (event) {
        var button = event.relatedTarget;
        const recipient = button.getAttribute('data-bs-whatever');
        var partes = recipient.split('|');
        
        var absenceId = partes[0];
        const nombre = partes[1];
        const requestUser = partes[2];
        const autorizado = (partes[3] === 'True');
        

        if (absenceId !== 'new') {
            // Comprueba si el usuario tiene permisos para editar el registro
            if (nombre !== requestUser && !autorizado ) { // String(requestUser) !== 'superusuario') {
                // El usuario no tiene permisos para editar el registro
                alert("No tienes permiso para editar este registro.");
                event.preventDefault();
                return;
            }
        }
        
        var modal = this;
        var hiddenInput = modal.querySelector('input[name="id"]');
        hiddenInput.value = absenceId;

        obtenerDatosYPermisos(absenceId);
    });
});

function obtenerDatosYPermisos(absenceId) {
    $.ajax({
        url: `/asistencias/obtenerAusencia/${absenceId}`,
        method: 'GET',
        success: function (data) {
            // Limpiar campos y recargar modal
            $('#ausenciaForm')[0].reset();
            $('#archivo_actual').empty();
            $('#archivo').closest('.mb-3').show();

            if (absenceId === 'new') {
                // Lógica para un nuevo registro: limpiar campos
                $('#ausenciaModal input[name="fecha_inicio"]').val('');
                $('#ausenciaModal input[name="fecha_fin"]').val('');
                $('#ausenciaModal input[name="cantidad_dias"]').val('');
                $('#ausenciaModal textarea[name="motivo"]').val('');
            } else {
                // Lógica para edición: poblar campos con datos
                $('#ausenciaModal input[name="fecha_inicio"]').val(data.fecha_inicio);
                $('#ausenciaModal input[name="fecha_fin"]').val(data.fecha_fin);
                $('#ausenciaModal input[name="cantidad_dias"]').val(data.cantidad_dias);
                $('#ausenciaModal textarea[name="motivo"]').val(data.motivo);

                // Manejo de los archivos existentes
                if (data.archivo_existe) {
                    $('#archivo_actual').append(`
                        <button type="button" class="btn btn-outline-primary btn-sm archivo-btn">
                            ${data.archivo.split('/').pop()} 
                            <span class="btn-close" aria-hidden="true"></span>
                        </button>
                    `);
                    $('#archivo').closest('.mb-3').hide(); 
                } 
            }
            // Asignar eventos al botón de eliminación de archivo
            $('.archivo-btn .btn-close').on('click', function() {
                $(this).closest('.archivo-btn').remove();  // Remover el archivo del DOM
                $('#archivo').closest('.mb-3').show();  // Mostrar el input para cargar un nuevo archivo
                agregarArchivoEliminado(data.archivo);  // Guardar el archivo en el select oculto
            });

            // Manejo de permisos
            let usuarioSelect = $('#usuarioSelect');
            let usuarioInput = $('#usuarioInput'); 
            usuarioSelect.empty(); 
            usuarioInput.val('');

            if (data.autorizado) {
                usuarioSelect.show();
                usuarioInput.hide();

                usuarioSelect.append('<option value="">Seleccione un usuario</option>');

                if (data.usuarios) {
                    data.usuarios.forEach(function(user) {
                        usuarioSelect.append(`<option value="${user.id}">${user.username}</option>`);
                    });
                }

                if (absenceId === 'new') {
                    usuarioSelect.val(data.usuario);
                }
            } else {
                usuarioSelect.hide();
                usuarioInput.show();
                usuarioInput.val(data.usuario);
            }

        },
        error: function (xhr, status, error) {
            console.error("Error al obtener los datos: ", error);
        }
    });
}

// El siguiente script maneja el autocompletado de la fecha de fin y la cantidad de días
document.addEventListener('DOMContentLoaded', function() {
    const fechaInicio = document.getElementById('fecha_inicio');
    const fechaFin = document.getElementById('fecha_fin');
    const cantidadDias = document.getElementById('cantidad_dias');

    fechaInicio.addEventListener('change', function() {
        if (cantidadDias.value) {
            let startDate = new Date(fechaInicio.value);
            startDate.setDate(startDate.getDate() + parseInt(cantidadDias.value) - 1);
            fechaFin.value = startDate.toISOString().split('T')[0];
        }
    });

    cantidadDias.addEventListener('input', function() {
        if (fechaInicio.value) {
            let startDate = new Date(fechaInicio.value);
            startDate.setDate(startDate.getDate() + parseInt(cantidadDias.value) - 1);
            fechaFin.value = startDate.toISOString().split('T')[0];
        }
    });

    fechaFin.addEventListener('change', function() {
        if (fechaInicio.value && fechaFin.value) {
            let startDate = new Date(fechaInicio.value);
            let endDate = new Date(fechaFin.value);
            let days = Math.round((endDate - startDate) / (1000 * 60 * 60 * 24)) + 1;
            cantidadDias.value = days;
        }
    });
});

// Manejar la carga dinámica de archivos
document.getElementById('archivo').addEventListener('change', function(event) {
    const archivoInput = event.target;
    const archivo = archivoInput.files[0];
    if (archivo) {
        const archivosCargadosDiv = document.getElementById('archivos_cargados');

        const archivoBtn = document.createElement('button');
        archivoBtn.type = 'button';
        archivoBtn.classList.add('btn', 'btn-outline-primary', 'btn-sm', 'me-2', 'archivo-btn');
        archivoBtn.innerHTML = archivo.name + ' ' + '   <span class="btn-close" aria-hidden="true"></span>';

        archivosCargadosDiv.appendChild(archivoBtn);

        archivoBtn.querySelector('.btn-close').addEventListener('click', function() {
            archivoBtn.remove();
            archivoInput.value = '';  // Limpiar el input de archivos
            agregarArchivoEliminado(archivo.name);
        });

        // Remover el input si ya se ha cargado un archivo
        archivoInput.style.display = 'none';
    }
});

function agregarArchivoEliminado(nombreArchivo) {
    const archivosEliminadosSelect = document.getElementById('archivos_eliminados');
    
    // Crear una nueva opción en el select para el archivo eliminado
    const opcionArchivoEliminado = document.createElement('option');
    opcionArchivoEliminado.value = nombreArchivo;
    opcionArchivoEliminado.text = nombreArchivo;
    opcionArchivoEliminado.selected = true;

    archivosEliminadosSelect.appendChild(opcionArchivoEliminado);

    // Mostrar el input de nuevo para que el usuario pueda cargar otro archivo
    document.getElementById('archivo').style.display = 'block';
}

