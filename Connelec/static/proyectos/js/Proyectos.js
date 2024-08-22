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

const editarProyectoModal = document.getElementById('editarProyectoModal')
editarProyectoModal.addEventListener('show.bs.modal', async event => {
  //botón que lanza el modal
  const button = event.relatedTarget

  const recipient = button.getAttribute('data-bs-whatever')
  var partes = recipient.split('`');

  //{{p.nombre}}`{{p.descripcion}}`{{p.cliente}}`{{p.n_expediente}}
  const nombre = partes[0];
  const descripcion = partes[1];
  //const cliente = partes[2];
  const n_expediente= partes[3];

  $("#nombre").val(nombre);
  $("#descripcion").val(descripcion);
  //$("#cliente").val(cliente);
  const valorNExpediente = n_expediente === 'None' ? 'Sin expediente' : n_expediente;
  $("#n_expediente").val(valorNExpediente);

  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
  });

});

async function showEditarProyectoModal(button){
    try{
        var response = await fetch(`/proyectos/infoEditarProyecto`);
        var data = await response.json();

        const recipient = button.getAttribute('data-bs-whatever')
        var partes = recipient.split('`');
        const cliente = partes[2];
        var clienteId = data.Cli.find(cli => cli.nombre === cliente)?.id;

        var cardContentCli = `
            <option value="${clienteId}">${cliente}</option>
            ${data.Cli.map(cli => `<option value="${cli.id}">${cli.nombre}</option>`).join('')}

        `;
        var modalBodyCli = document.getElementById('cliente');
        modalBodyCli.innerHTML = cardContentCli;

        var modal = new bootstrap.Modal(document.getElementById(editarProyectoModal));
        modal.show();

    } catch(error){
        console.log('Error:', error);
    }
}