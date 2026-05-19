const BROKER = "broker.emqx.io";
const PORT = 8083;
const TOPIC_WEB = "giirob/pr2/erro/pentapanel/pedido";

// CORRECCIÓN 1: Se añade '/upload' y detecta automáticamente la IP de tu ordenador
const UPLOAD_URL = `http://${window.location.hostname}:5001/upload`;

const STICKER_PATHS = {
    hazard_bolt: "images/electricidad.png",
    foot_bolt: "images/botas.png",
    gloves: "images/guantes.png",
    goggles: "images/gafas.png",
    prohibited: "images/prohibidoPasar.png",
};

let client = new Paho.MQTT.Client(BROKER, PORT, "pentapanel_web_" + Math.random());
let selectedId = null;

client.connect({ onSuccess: () => console.log("PentaPanel Conectado") });

document.querySelectorAll('.sticker-option').forEach(opt => {
    opt.addEventListener('click', () => {
        // CORRECCIÓN 2: Lógica para deseleccionar si ya estaba seleccionado
        if (opt.classList.contains('selected')) {
            opt.classList.remove('selected');
            selectedId = null; // Resetea la variable
        } else {
            // Si no estaba seleccionado, quita la selección de los demás y lo selecciona
            document.querySelectorAll('.sticker-option').forEach(o => o.classList.remove('selected'));
            opt.classList.add('selected');
            selectedId = opt.getAttribute('data-id');
        }
    });
});

async function uploadSticker(file) {
    const form = new FormData();
    form.append("file", file);

    const response = await fetch(UPLOAD_URL, {
        method: "POST",
        body: form,
    });

    if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.error || "Error al subir la imagen");
    }

    return response.json();
}

document.getElementById('btnOrder').addEventListener('click', async () => {
    const qty = parseInt(document.getElementById('quantity').value);
    const fileInput = document.getElementById('customSticker');

    let ruta = null;

    try {
        if (fileInput.files && fileInput.files.length > 0) {
            const resultado = await uploadSticker(fileInput.files[0]);
            ruta = resultado.ruta_relativa;
        } else if (selectedId && STICKER_PATHS[selectedId]) {
            ruta = STICKER_PATHS[selectedId];
        } else {
            return alert("Selecciona un pictograma o sube un PNG.");
        }

        const payload = JSON.stringify({
            ruta_png: ruta,
            unidades: qty,
        });

        const message = new Paho.MQTT.Message(payload);
        message.destinationName = TOPIC_WEB;
        client.send(message);

        alert(`¡Pedido enviado! Fabricando ${qty} cuadros PentaPanel.`);
    } catch (error) {
        alert(error.message || "Error al enviar el pedido");
    }
});