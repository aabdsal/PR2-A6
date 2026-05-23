# Guía para ejecutar la página web desde cualquier lugar con Cloudflare Tunnel

## Objetivos
Esta página web permite interactuar con la estación de RoboDK desde cualquier dispositivo, incluso fuera de tu red local, de forma segura y sencilla. Puedes:
- Seleccionar la pegatina deseada
- Especificar el número de planchas a procesar
- Controlar los procesos de la estación en tiempo real

## Funcionamiento
Gracias a Cloudflare Tunnel, tu ordenador actúa como servidor web accesible desde cualquier lugar mediante una URL pública segura (HTTPS), sin necesidad de abrir puertos ni configurar el router.

## Instrucciones paso a paso

### 1. Verificar que Python 3 está instalado
```bash
python3 --version
```
Si no tienes Python instalado, descárgalo desde https://www.python.org

### 2. Instalar dependencias necesarias
Desde la carpeta raíz del proyecto:
```bash
pip install flask flask-cors pillow
```

### 3. Iniciar el servidor Flask
Navega a la carpeta `web/` del proyecto y ejecuta:
```bash
python upload_server.py
```
Verás un mensaje como:
```
 * Running on http://127.0.0.1:5001
```

### 4. Instalar Cloudflare Tunnel (cloudflared)
Si no lo tienes instalado:
```bash
brew install cloudflared
```
O consulta instrucciones para tu sistema operativo en: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/

### 5. Exponer tu servidor Flask a Internet
Ejecuta en la terminal:
```bash
cloudflared tunnel --url http://localhost:5001
```
Obtendrás una URL pública del tipo:
```
https://xxxx.trycloudflare.com
```

### 6. Acceder desde cualquier dispositivo
Abre la URL pública de Cloudflare Tunnel en cualquier navegador, desde cualquier red o dispositivo. ¡Ya puedes usar la web y subir imágenes!

### 7. (Opcional) Crear un código QR para facilitar el acceso
1. Ve a https://www.the-qrcode-generator.com
2. Selecciona "URL"
3. Ingresa la URL pública de Cloudflare Tunnel
4. Descarga e imprime el código QR

## Requisitos mínimos
- Python 3.x
- Navegador web moderno en los dispositivos cliente
- Acceso a Internet en el ordenador servidor