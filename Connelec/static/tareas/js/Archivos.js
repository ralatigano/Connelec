let dataTable;
let dataTableIsInitilized=false;

const initDataTable=async() => {
    if(dataTableIsInitilized){
        dataTable.destroy();
    }
    dataTable=$("#Archivos").DataTable({
        language: {
            lengthMenu: 'Mostrar _MENU_ archivos por página',
            zeroRecords: 'No hay archivos registrados',
            info: 'Mostrando de _START_ a _END_ de _TOTAL_ archivos',
            infoEmpty: 'No hay tareas',
            InfoFiltered: '(filtrado de _MAX_ archivos totales)',
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