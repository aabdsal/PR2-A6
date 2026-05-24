# PR2-A6 - Automatización del proceso de cuadros eléctricos

## Resumen
Este proyecto desarrolla una celda automatizada para la fabricación de cuadros eléctricos en entorno RoboDK.
La implementación actual esta centrada en simulación y en la traducción funcional de la lógica de proceso a Python.

<p align="center">
	<img src="image.png" width="500"/>
</p>

## Miembros
- Ali Abdelhamid
- Andreu García
- Manuel Martínez
- Roberto Noguera
- Ángela Sal

## Objetivo de la propuesta
- Alimentación de material a través de cintas.
- Pick-and-place robotizado.
- Plegado de planchas.
- Soldadura robotizada.
- Montaje del cuadro.
- Etiquetado del cuadro.
- Integración con nodos ESP32.
- Mensajeria MQTT para coordinación.
- Intercambio de estados y ordenes en JSON.

## Requisitos
- RoboDK instalado y estación de simulación disponible.
- Python 3.9+ (compatible con el intérprete integrado de RoboDK.)
- Paquete Python `robodk` instalado en el entorno activo.
- Paquetes `paho-mqtt` y `psycopg` instalados en el intérprete de RoboDK para conectarse a MQTT y a la Base de Datos SQL
- VS Code + PlatformIO para el firmware del ESP32.
- PostgreSQL y pgAdmin para la base de datos.

## Preparación del entorno
Desde la raíz del proyecto:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install robodk
brew install cloudflared
```

Para `paho-mqtt` y `psycopg` ` flask` `flask-cors` `pillow`, usa el intérprete que RoboDK tiene configurado (Tools > Options > Python):

```bash
<RUTA_PYTHON_ROBODK> -m pip install paho-mqtt psycopg  flask flask-cors pillow
```

## Web (Flask + Cloudflare Tunnel)
- Permite interactuar con la estación RoboDK desde cualquier dispositivo vía web.
- Para acceso remoto seguro, se recomienda usar Cloudflare Tunnel (`cloudflared`).
- La web se ejecuta desde la carpeta `web/` y se expone por defecto en el puerto 5001.
- Acceso remoto: https seguro mediante URL pública generada por Cloudflare Tunnel.
- Puedes generar un código QR con la URL pública en https://www.the-qrcode-generator.com para facilitar el acceso desde móviles.


## ESP32 (PlatformIO)
- Abrir la carpeta `firmware_esp32` en VS Code con PlatformIO instalado.
- Ajustar WiFi y MQTT en `firmware_esp32/include/config.h` (NET_SSID, NET_PASSWD, MQTT_SERVER_IP).
- Compilar, subir y monitorizar

## Base de datos (PostgreSQL + pgAdmin)
- Crear la base de datos `gdi2026` en pgAdmin y ejecutar los scripts `database/DDL_proyecto.sql` y `database/poblar_proyecto.sql`.
- Verificar los datos de conexión en `modulos_python/bbdd.py` (dbname, user, password, host, port).

## Ejecución
- Abrir RoboDK con licencia activa.
- Cargar los scripts `modulos_python/main.py` y `modulos_python/reset.py` en la estación para asegurarse de tener la versión más nueva dentro de ella.
- Ejecutar script main desde RoboDK con la estación abierta.
- Para la página web, ejecuta primero:

```bash
cd web
python upload_server.py
```
- Y ahora para iniciar la web
```bash
cloudflared tunnel --url http://localhost:5001
```
- Se generará una URL pública para acceder desde cualquier dispositivo.






