function submitForm(category) {
    // Agrega un campo oculto al formulario con el valor de la categoría
    var input = document.createElement("input");
    input.setAttribute("type", "hidden");
    input.setAttribute("name", "selected_category");
    input.setAttribute("value", category);
    document.getElementById("logTrainingForm").appendChild(input);

    // Envía el formulario
    document.getElementById("logTrainingForm").submit();
}