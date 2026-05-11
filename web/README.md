# Guía para ejecutar la página web localmente

## Objetivos
Esta página web permite interactuar con la estación de RoboDK desde múltiples dispositivos conectados a la misma red. Puedes:
- Seleccionar la pegatina deseada
- Especificar el número de planchas a procesar
- Controlar los procesos de la estación en tiempo real


## Funcionamiento
Esta solución es ideal para eventos como la feria de proyectos. Permite que múltiples usuarios se conecten desde sus dispositivos sin necesidad de configuración adicional. Tu ordenador actúa como servidor web, y cualquiera conectado a tu red WiFi puede acceder.

## Instrucciones paso a paso

### Encontrar la dirección IP de tu ordenador
La dirección IP es necesaria para que otros accedan a tu servidor.

**En macOS/Linux:**
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```
O ve directamente a Ajustes > Red > Wi-Fi > Detalles > Dirección IPv4

**En Windows:**
```cmd
ipconfig
```
Busca "Dirección IPv4" en la salida

**Ejemplo:** `192.168.1.132`

### Verificar que Python 3 está instalado
```bash
python3 --version
```
Si no tienes Python instalado, descárgalo desde https://www.python.org

### Inicia el servidor web
Navega a la carpeta `web/` del proyecto y ejecuta:

```bash
python3 -m http.server 8000
```

Verás un mensaje como:
```
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

El servidor estará disponible en `http://localhost:8000`

### Acceder desde otros dispositivos
Desde cualquier navegador en la misma red, abre:
```
http://TU_DIRECCIÓN_IP:8000
```

**Ejemplo práctico:**
```
http://192.168.1.132:8000
```

### Crear un código QR para facilitar el acceso
Para eventos donde otros deben conectarse rápidamente:
1. Ve a https://www.the-qrcode-generator.com
2. Selecciona "URL"
3. Ingresa: `http://TU_DIRECCIÓN_IP:8000`
4. Descarga e imprime el código QR

## Requisitos mínimos
- Python 3.x
- Conexión a red WiFi compartida
- Navegador web moderno en los dispositivos cliente

## Solución de problemas
**¿No se carga la página?**
- Verifica que el servidor sigue ejecutándose en Terminal
- Comprueba que la dirección IP es correcta (puede cambiar)
- Asegúrate de que el cliente y el host están en la misma red WiFi

**¿Los cambios no se ven?**
- Recarga la página (Ctrl+F5 o Cmd+Shift+R)
- Limpia la caché del navegador