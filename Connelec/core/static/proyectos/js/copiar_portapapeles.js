// Función para manejar el clic del botón en la vista de proyectos
function handleButtonClick(button) {
    var info = button.getAttribute('data-info');

    if (info.includes('|')) {
        showModal(info);
    } else {
        copyTextToClipboard(info, button);
    }
}

// Función para copiar texto al portapapeles
function copyTextToClipboard(text, button) {
    // Copiar el texto al portapapeles
    navigator.clipboard.writeText(text).then(function() {
        // Mostrar el toast
        var toastElement = document.getElementById('toast');
        var bsToast = new bootstrap.Toast(toastElement);

        // Ajustar clase según el tema activo
        var theme = localStorage.getItem('theme') || 'light';
        if (theme === 'dark') {
            toastElement.classList.add('toast-dark');
            toastElement.classList.remove('toast-light');
        } else {
            toastElement.classList.add('toast-light');
            toastElement.classList.remove('toast-dark');
        }

        toastElement.classList.remove('d-none'); // Asegúrate de que el toast sea visible
        bsToast.show();
        
        // Ocultar el toast después de 3 segundos
        setTimeout(function() {
            bsToast.hide();
            toastElement.classList.add('d-none');
        }, 3000);
    }, function(err) {
        console.error('Error al copiar: ', err);
    });
}

// Función para mostrar el modal con la información dividida
function showModal(info) {
    var infoArray = info.split(' | ');
    var modalContent = document.querySelector('#copiarInfoModal .modal-body');
    const buttonClass = getButtonClass(); // Obtener la clase según el tema

    if (modalContent) {
        modalContent.innerHTML = ''; // Limpiar contenido previo

        infoArray.forEach(function(text, index) {
            var div = document.createElement('div');
            div.classList.add('mb-2'); // Añadir margen entre los renglones
            div.innerHTML = `
                <div class="d-flex justify-content-between">
                    <span>${text}</span>
                    <button type="button" class="btn ${buttonClass} btn-xs" data-bs-toggle="tooltip" data-bs-placement="top" data-bs-custom-class="custom-tooltip" data-bs-title="Copiar al portapapeles" onclick="copyTextToClipboard('${text}', this)"><i class="fa-solid fa-copy"></i></button>
                </div>
            `;
            modalContent.appendChild(div);
        });

        var modal = new bootstrap.Modal(document.getElementById('copiarInfoModal'));
        modal.show();
    } else {
        console.error("No se encontró ningún elemento con la clase 'modal-body' dentro del modal");
    }
}

// Función para determinar el tema y aplicar la clase correcta
function getButtonClass() {
    // Asume que el tema oscuro se marca con una clase 'dark-theme' en el body
    const theme = localStorage.getItem('theme');
    
    // Retorna la clase correspondiente según el tema
    return theme === 'dark' ? 'btn-outline-light' : 'btn-outline-dark';
}

