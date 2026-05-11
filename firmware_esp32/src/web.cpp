#include "web.h"
#include <WebServer.h>
#include <ArduinoJson.h>
#include "comunicaciones.h"

// Instanciem el servidor al port 80 (HTTP)
WebServer server(80);

// HTML i JS integrat usant PROGMEM per a no gastar memòria RAM
const char htmlPage[] PROGMEM = R"=====(
<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interfície RoboDK</title>
    <style>
        :root {
            --glow: #00ffcc;
            --bg: #0b1021;
            --panel: #131a35;
        }
        body { 
            font-family: 'Courier New', Courier, monospace; 
            background-color: var(--bg); 
            color: #d1d5db; 
            margin: 0; 
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            background-color: var(--panel);
            padding: 30px 40px;
            border-radius: 12px;
            border: 1px solid #232d4b;
            box-shadow: 0 0 20px rgba(0, 255, 204, 0.15);
            width: 100%;
            max-width: 350px;
            text-align: left;
        }
        h2 {
            color: var(--glow);
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-top: 0;
            text-shadow: 0 0 10px rgba(0, 255, 204, 0.4);
            text-align: center;
            border-bottom: 1px solid #232d4b;
            padding-bottom: 15px;
        }
        label {
            display: block;
            margin-top: 20px;
            font-size: 13px;
            color: #8b949e;
            letter-spacing: 1px;
        }
        input[type="text"], input[type="number"], input[type="file"] { 
            width: 100%;
            box-sizing: border-box;
            margin-top: 8px; 
            padding: 12px; 
            font-size: 15px; 
            background-color: #050814;
            border: 1px solid #30363d;
            color: var(--glow);
            border-radius: 6px;
            outline: none;
            font-family: inherit;
        }
        input:focus {
            border-color: var(--glow);
            box-shadow: 0 0 8px rgba(0, 255, 204, 0.3);
        }
        input[type="file"] { padding: 8px; color: #8b949e; }
        
        button { 
            margin-top: 30px; 
            padding: 14px 20px; 
            font-size: 16px; 
            font-weight: bold;
            background-color: transparent;
            color: var(--glow);
            border: 2px solid var(--glow);
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.3s;
            text-transform: uppercase;
            width: 100%;
            font-family: inherit;
            letter-spacing: 1px;
        }
        button:hover {
            background-color: var(--glow);
            color: var(--bg);
            box-shadow: 0 0 15px var(--glow);
        }
        .status {
            text-align: center;
            margin-top: 15px;
            font-size: 12px;
            color: #8b949e;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>⚙️ Sistema RoboDK</h2>
        
        <label>▶ IDENTIFICADOR (màx 20 lletres):</label>
        <input type="text" id="texto" maxlength="20" placeholder="Escriu el teu nom...">

        <label>▶ CARREGAR TEXTURA (Imatge):</label>
        <input type="file" id="foto" accept="image/*">

        <label>▶ UNITATS A PROCESSAR (1 a 5):</label>
        <input type="number" id="caixes" min="1" max="5" value="1">

        <button onclick="enviarDades()" type="button" id="btn-enviar">INICIAR SEQÜÈNCIA</button>
        <div class="status" id="estat">Estat: Esperant instruccions...</div>

        <canvas id="canvas" style="display:none;"></canvas>
    </div>

    <script>
        function enviarDades() {
            const texto = document.getElementById('texto').value;
            const caixes = document.getElementById('caixes').value;
            const fitxer = document.getElementById('foto').files[0];
            const btn = document.getElementById('btn-enviar');
            const estat = document.getElementById('estat');

            if(!fitxer) { alert("⚠️ ERROR: Falta carregar la imatge (textura)."); return; }
            if(!texto) { alert("⚠️ ERROR: L'identificador no pot estar buit."); return; }

            estat.style.color = "#00ffcc";
            estat.innerHTML = "Estat: Processant informació...";
            btn.innerHTML = "ENVIANT...";
            btn.style.opacity = "0.5";

            const reader = new FileReader();
            reader.onload = function(event) {
                const img = new Image();
                img.onload = function() {
                    const canvas = document.getElementById('canvas');
                    const ctx = canvas.getContext('2d');
                    
                    canvas.width = 200; 
                    canvas.height = 200;
                    
                    ctx.drawImage(img, 0, 0, 200, 200);
                    
                    // Afegir fons negre semi-transparent arrere del text per a que es llitja millor
                    ctx.fillStyle = "rgba(0, 0, 0, 0.6)";
                    ctx.fillRect(0, 155, 200, 45);

                    ctx.font = "bold 20px 'Courier New', monospace";
                    ctx.fillStyle = "#00ffcc"; // text color verd cíber
                    ctx.textAlign = "center";
                    ctx.fillText(texto.toUpperCase(), 100, 185);

                    const pegatinaBase64 = canvas.toDataURL('image/jpeg', 0.6);

                    fetch('/guardar', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            id_usuari: texto.toUpperCase(),
                            imatge: pegatinaBase64,
                            numero_caixes: parseInt(caixes)
                        })
                    }).then(res => {
                        estat.innerHTML = "Estat: ✅ Dades enviades a l'ESP32!";
                        btn.innerHTML = "SEQÜÈNCIA COMPLETADA";
                        setTimeout(() => {
                            btn.innerHTML = "INICIAR SEQÜÈNCIA";
                            btn.style.opacity = "1";
                            estat.style.color = "#8b949e";
                            estat.innerHTML = "Estat: Esperant instruccions...";
                        }, 3000);
                    }).catch(err => {
                        estat.style.color = "red";
                        estat.innerHTML = "Estat: ❌ Error de connexió.";
                        btn.innerHTML = "INICIAR SEQÜÈNCIA";
                        btn.style.opacity = "1";
                    });
                }
                img.src = event.target.result;
            }
            reader.readAsDataURL(fitxer);
        }
    </script>
</body>
</html>
)=====";

void handleRoot() {
    server.send(200, "text/html", htmlPage);
}

void handleGuardar() {
    // Comprovem si s'han enviat dades en el body
    if (server.hasArg("plain") == false) {
        server.send(400, "text/plain", "Les dades no han arribat");
        return;
    }
    
    // Obtenim el JSON amb les dades Base64 i número de caixes
    String body = server.arg("plain");
    
    
    // Anem a decodificar un poc el JSON per separar la informació.
    // L'ESP32 té poca RAM per decodificar JSONs molt grans si la imatge
    // base64 és molt pesada, per això fem un pas directe del 'body' complet
    // o enviem el mateix body JSON a un topic.
    // Com a "body" ja vé empaquetat correctament formatat:
    // { "imatge": "data:image...", "numero_caixes": N, "id_usuari": "NOM" }
    
    // Publiquem directament tot el JSON pel topic de pegatines:
    // És a dir, la ESP actua com a simple "tub" envidador des del web fins al MQTT.
    enviarMensajePorTopic("giirob/pr2/erro/pegatina", body);
    // NOTA: Ací cridarem més endavant a la teua funció MQTT per publicar 'body'.
    
    server.send(200, "text/plain", "Dades processades per l'ESP32");
}

void initWebServer() {
    server.on("/", HTTP_GET, handleRoot);
    server.on("/guardar", HTTP_POST, handleGuardar);
    
    server.begin();
    Serial.println("Servidor Web iniciat. Ves a la IP de l'ESP32 en el navegador.");
}

void handleWebServer() {
    server.handleClient();
}
