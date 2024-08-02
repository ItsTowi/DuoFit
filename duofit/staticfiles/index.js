// Variable para almacenar la categoría seleccionada
let selectedCategory = '';

// Función para mostrar el modal y almacenar la categoría seleccionada
function submitForm(category) {
    // Guardar la categoría seleccionada en una variable global
    selectedCategory = category;

    // Mostrar el modal
    $('#descriptionModal').modal('show');
}

// Función para enviar el formulario con la categoría y la descripción
document.getElementById('confirmSubmit').addEventListener('click', function() {
    // Obtener el valor de la descripción
    const description = document.getElementById('descriptionInput').value;

    // Obtener el formulario
    const form = document.getElementById("logTrainingForm");

    // Eliminar los campos ocultos existentes, si los hay
    const existingCategoryInput = form.querySelector('input[name="selected_category"]');
    const existingDescriptionInput = form.querySelector('input[name="description"]');
    if (existingCategoryInput) existingCategoryInput.remove();
    if (existingDescriptionInput) existingDescriptionInput.remove();

    // Crear un nuevo campo oculto para la categoría
    const categoryInput = document.createElement("input");
    categoryInput.setAttribute("type", "hidden");
    categoryInput.setAttribute("name", "selected_category");
    categoryInput.setAttribute("value", selectedCategory);

    // Crear un nuevo campo oculto para la descripción
    const descriptionInput = document.createElement("input");
    descriptionInput.setAttribute("type", "hidden");
    descriptionInput.setAttribute("name", "description");
    descriptionInput.setAttribute("value", description);

    // Añadir los campos ocultos al formulario
    form.appendChild(categoryInput);
    form.appendChild(descriptionInput);

    // Enviar el formulario
    form.submit();
});