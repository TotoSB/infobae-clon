function verificarArchivo(element_get) {
    const files_get = element_get.files;

    if (files_get.length > 0) {
        const div = document.getElementById('cont-media');
        const inputs = div.querySelectorAll('input[type="file"]');
        const num = inputs.length + 1;

        const input_new = document.createElement('input');
        input_new.setAttribute('type', 'file');
        input_new.setAttribute('onchange', 'verificarArchivo(this)');
        input_new.setAttribute('name', 'media-' + num);
        input_new.setAttribute('id', 'media-' + num);

        const label = document.createElement('label');
        label.textContent = "Imagen: "+num;
        div.appendChild(label)
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

    document.getElementById('cont-media').appendChild(label);
    document.getElementById('cont-media').appendChild(inputInicial);
};