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
        }
    });
    dataTableIsInitilized=true;
}

window.addEventListener("load", async() => {
    await initDataTable();
    //document.getElementById("nav_item_clientes").style.fontWeight = "bold";
});