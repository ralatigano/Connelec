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
        }
    });
    dataTableIsInitilized=true;
}

window.addEventListener("load", async() => {
    await initDataTable();
});