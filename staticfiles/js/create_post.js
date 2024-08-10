var count = 1;
function verificarArchivo(element_get) {
    const files_get = element_get.files;

    if (files_get.length > 0) {
        const div = document.getElementById('cont-media');
        const form = document.getElementsByTagName("form")[0];
        const inputs = div.querySelectorAll('input[type="file"]');
        const num = inputs.length + 1;

        const input_new = document.createElement('input');
        input_new.setAttribute('type', 'file');
        input_new.setAttribute('onchange', 'verificarArchivo(this)');
        input_new.setAttribute('name', 'media-' + num);
        input_new.setAttribute('id', 'media-' + num);

        const label = document.createElement('label');
        label.textContent = "Imagen " + num + ": ";

        const textarea = document.getElementById('descripcion');
        // Conseguimos la posicion donde se dejo el cursor
        const cursorPosition = textarea.selectionStart;

        const input_new_hide = document.createElement('input');
        input_new_hide.setAttribute('type', 'hidden')
        input_new_hide.setAttribute('id', 'position-' + count);
        input_new_hide.setAttribute('name', 'position-' + count);
        count = count + 1;
        input_new_hide.setAttribute('value', cursorPosition)

        input_new.setAttribute('type', 'file');

        const marker = `<!--img-${num}-->`;

        textarea.value = textarea.value.slice(0, cursorPosition) + marker + textarea.value.slice(cursorPosition);

        form.appendChild(input_new_hide);
        div.appendChild(label);
        div.appendChild(input_new);
    }
}

window.onload = function() {
    const inputInicial = document.createElement('input');
    inputInicial.setAttribute('type', 'file');
    inputInicial.setAttribute('onchange', 'verificarArchivo(this)');
    inputInicial.setAttribute('name', 'media-1');
    inputInicial.setAttribute('id', 'media-1');

    const label = document.createElement('label');
    label.textContent = "Imagen 1: ";

    const div = document.getElementById('cont-media');
    div.appendChild(label);
    div.appendChild(inputInicial);
};
