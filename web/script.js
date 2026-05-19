const BROKER = "broker.emqx.io";
const PORT = 8083;
const TOPIC_WEB = "giirob/pr2/erro/pentapanel/pedido";

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

client.connect({ onSuccess: () => console.log("MQTT conectado") });

document.querySelectorAll('.sticker-option').forEach(opt => {
    opt.addEventListener('click', () => {
        if (opt.classList.contains('selected')) {
            opt.classList.remove('selected');
            selectedId = null;
        } else {
            document.querySelectorAll('.sticker-option').forEach(o => o.classList.remove('selected'));
            opt.classList.add('selected');
            selectedId = opt.getAttribute('data-id');
        }
    });
});

async function processImage(file) {
    return new Promise((resolve, reject) => {
        const img = new Image();
        const reader = new FileReader();

        reader.onload = e => img.src = e.target.result;

        img.onload = () => {
            const canvas = document.createElement("canvas");
            const ctx = canvas.getContext("2d");

            const MAX_WIDTH = 800;
            const scale = Math.min(1, MAX_WIDTH / img.width);

            canvas.width = img.width * scale;
            canvas.height = img.height * scale;

            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

            canvas.toBlob(blob => {
                if (!blob) return reject("Error procesando imagen");

                if (blob.size > 2 * 1024 * 1024) {
                    return reject("Imagen demasiado grande (>2MB)");
                }

                resolve(blob);
            }, "image/png");
        };

        reader.onerror = () => reject("Error leyendo archivo");
        reader.readAsDataURL(file);
    });
}

async function uploadSticker(file) {
    const processed = await processImage(file);

    const form = new FormData();
    form.append("file", processed, "custom.png");

    const response = await fetch(UPLOAD_URL, {
        method: "POST",
        body: form,
    });

    if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.error || "Error al subir");
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
            return alert("Selecciona un pictograma o sube una imagen");
        }

        const payload = JSON.stringify({
            ruta_png: ruta,
            unidades: qty,
        });

        if (client.isConnected()) {
            const message = new Paho.MQTT.Message(payload);
            message.destinationName = TOPIC_WEB;
            client.send(message);

            alert(`Pedido enviado (${qty})`);
        } else {
            alert("MQTT no conectado");
        }

    } catch (error) {
        alert(error.message);
    }
});