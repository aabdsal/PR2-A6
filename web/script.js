const BROKER = "broker.emqx.io";
const PORT = 8083;
const TOPIC_WEB = "giirob/pr2/erro/pentapanel/pedido";

let client = new Paho.MQTT.Client(BROKER, PORT, "pentapanel_web_" + Math.random());
let selectedId = null;

client.connect({ onSuccess: () => console.log("PentaPanel Conectado") });

document.querySelectorAll('.sticker-option').forEach(opt => {
    opt.addEventListener('click', () => {
        document.querySelectorAll('.sticker-option').forEach(o => o.classList.remove('selected'));
        opt.classList.add('selected');
        selectedId = opt.getAttribute('data-id');
    });
});

document.getElementById('btnOrder').addEventListener('click', () => {
    const qty = document.getElementById('quantity').value;
    if(!selectedId) return alert("Selecciona un pictograma");

    const payload = JSON.stringify({
        sistema: "PENTAPANEL",
        comando: "START",
        sticker: selectedId,
        unidades: parseInt(qty),
        user_timestamp: Date.now()
    });

    const message = new Paho.MQTT.Message(payload);
    message.destinationName = TOPIC_WEB;
    client.send(message);
    
    alert(`¡Pedido enviado! Fabricando ${qty} cuadros PentaPanel.`);
});