// Obtener referencias a los elementos DOM
let addContainer = document.getElementById('add-container');
let btnAddRegister = document.getElementById('btn-add-register');
let iconElement = btnAddRegister.querySelector('i');

if (addContainer && btnAddRegister && iconElement) {
    // Agregar un event listener al botón
    btnAddRegister.addEventListener('click', function() {
        // Alternar la visibilidad del div cambiando la clase d-none
        addContainer.classList.toggle('d-none');

        btnAddRegister.classList.toggle('btn-success')
        btnAddRegister.classList.toggle('btn-danger')

        iconElement.classList.toggle('fa-plus');
        iconElement.classList.toggle('fa-sort-up');

    });
}

// let deleteButtons = document.querySelectorAll('.delete');
// if (deleteButtons.length > 0) {
//     deleteButtons.forEach(function(button) {
//         button.addEventListener('click', function() {
//             let formId = button.getAttribute('data-form-id');
//             let newAction = button.getAttribute('data-action');

//             // Obtén el formulario
//             let form = document.getElementById(formId);

//             // Cambia la acción del formulario
//             form.action = newAction;

//             // Establece el método del formulario a 'POST' (puedes ajustarlo según tus necesidades)
//             form.method = 'POST';

//             // Envía el formulario
//             form.submit();
//         });
//     });
// }

// Escuchar el clic en el botón de eliminar
document.querySelectorAll('.delete').forEach(function(button) {
    button.addEventListener('click', function() {
        var deleteAction = button.getAttribute('data-action');

        // Mostrar el modal de confirmación
        var modal = new bootstrap.Modal(document.getElementById('confirmDeleteModal'));
        modal.show();

        // Cuando se hace clic en el botón de confirmación en el modal
        document.getElementById('confirmDeleteButton').addEventListener('click', function() {
            // Enviar la solicitud para eliminar la tarea
            fetch(deleteAction, {
                method: 'POST', // o 'POST' según tu ruta y método
            })
            .then(response => {
                if (response.ok) {
                    // Puedes realizar alguna acción adicional si la eliminación fue exitosa
                    console.log('Tarea eliminada exitosamente');
                    window.location.reload();
                } else {
                    console.error('Error al intentar eliminar la tarea');
                }
            })
            .catch(error => console.error('Error en la solicitud:', error))
            .finally(() => {
            // Ocultar el modal después de la acción
                modal.hide();
            });
        });
    });
});

