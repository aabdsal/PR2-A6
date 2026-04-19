# PR2-A6 - Automatización del proceso de cuadros eléctricos

## 1) Resumen
Este proyecto desarrolla una celda automatizada para la fabricacion de cuadros electricos en entorno RoboDK.
La implementacion actual esta centrada en simulacion y en la traduccion funcional de la logica de proceso a Python.

## 2) Objetivo de la propuesta
El objetivo principal es automatizar de forma integral:
- Alimentacion de material.
- Pick-and-place robotizado.
- Plegado de chapa.
- Soldadura robotizada.
- Montaje y salida de pieza final con trazabilidad.

Adicionalmente, la propuesta contempla:
- Integracion con nodos ESP32.
- Mensajeria MQTT para coordinacion.
- Intercambio de estados y ordenes en JSON.

## 3) Estado actual del proyecto
### Hecho
- Traduccion principal de la logica de RoboDK a scripts Python.
- Flujo funcional de simulacion implementado por fases.
- Correcciones base de estabilidad y reutilizacion aplicadas.

### En progreso / pendiente
- Integracion de E/S para sincronizacion industrial (`waitDI` / `setDO`).
- Integracion de comunicaciones con ESP32 y MQTT.
- Integracion con base de datos para trazabilidad.
- Definicion de pruebas de regresion y validacion automatica.

## 4) Flujo funcional actual (alto nivel)
1. Alimentacion inicial de material.
2. Recogida de plancha.
3. Proceso de plegado.
4. Colocacion en etapa intermedia.
5. Preparacion y ejecucion de soldadura.
6. Transferencia de pieza acabada.

## 5) Requisitos
- RoboDK instalado y estacion de simulacion disponible.
- Python 3.9+ (compatible con el interprete integrado de RoboDK).
- Paquete Python `robodk` instalado en el entorno activo.
- Si se ejecuta con PySide2/shiboken2, usar `numpy<2` para evitar incompatibilidades binarias.

## 6) Preparacion del entorno
Desde la raiz del proyecto:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install robodk "numpy<2"
```

Comprobacion:

```bash
python -c "import robodk, sys; print(sys.executable); print(robodk.__file__)"
```

## 7) Ejecucion
- Ejecutar scripts desde RoboDK con la estacion abierta.
- Verificar estado de simulacion antes de lanzar secuencias criticas.

## 8) Roadmap tecnico
1. Anadir hilos en las fases que deban ejecutarse en paralelo.
2. Definir sincronizacion explicita entre hilos y entre estaciones de proceso.
3. Evitar condiciones de carrera con primitivas de concurrencia (locks, eventos, colas).
4. Sustituir flags de memoria por E/S de proceso (`setDO`, `waitDI`) en sincronizaciones criticas.
5. Introducir capa de I/O desacoplada para memoria, RoboDK y MQTT.
6. Conectar persistencia de ordenes y eventos para trazabilidad completa.
7. Definir pipeline de validacion (lint, type checking y smoke tests).

## 9) Nota de madurez
Version actual orientada a simulacion y estabilizacion funcional.
La siguiente fase se centra en robustez industrial, sincronizacion y observabilidad.
