"""Archivo principal que ejecuta todas las acciones de los distintos módulos.

Se caracteriza por el uso de hilos para cada acción o conjunto de acciones
necesarias para la automatización de cuadros eléctricos.

El uso de hilos permite ejecutar instancias en paralelo, por ejemplo mover
cintas o coordinar robots simultáneamente."""

from modulos_python.entorno import preparar_entorno
preparar_entorno()

from modulos_python import bending, sensor, soldar, variables, mqtt, bbdd
from modulos_python import mover_cinta as mc, pick_place as pp, simulation as sim

from robodk import robolink
import threading
import time

mqtt.conectar()
#bbdd.conectar()

sim.setDO("yaskawa_larga", 1)
sim.setDO("yaskawa_ancha", 1)
sim.setDO("abb_tapa", 1)

def _thread_excepthook(args):
    """Se hace uso de este método interno para imprimir por pantalla los errores que 
    surjan en tiempo de ejecución, es muy útil porque nos dice en que hilo ha fallado 
    y devuelve el mensaje que elevan las excepciones en las funciones internas al hilo."""

    RDK = robolink.Robolink()

    RDK.ShowMessage(f"[ThreadError] {args.thread.name}: {args.exc_type.__name__}: {args.exc_value}")

threading.excepthook = _thread_excepthook

# Los siguientes hilos mueven las cintas por donde llegan los objetos.
def hilo_cinta_larga():
    """Hilo que mueve la cinta de planchas largas."""
    while True:
        sim.waitDI("yaskawa_larga" , 1)
        mc.mover_cinta_larga()
        time.sleep(0.01)  

def hilo_cinta_ancha():
    """Hilo que mueve la cinta de planchas anchas."""
    while True:
        sim.waitDI("yaskawa_ancha" , 1)
        mc.mover_cinta_ancha()
        time.sleep(0.01)  

def hilo_cinta_tapa():
    """Hilo que mueve la cinta de tapas."""
    while True:
        sim.waitDI("abb_tapa" , 1)
        mc.mover_cinta_tapa()
        time.sleep(0.01)  
    
def hilo_cinta_main(): 
    """Hilo que mueve la cinta principal cuando hay pieza disponible."""
    while True:
        mc.mover_cinta_main()
        time.sleep(0.01)

def hilo_cinta_etiquetado():
    """Hilo que mueve la cinta final de etiquetado."""
    while True:
        mc.mover_cinta_cuadro_acabada()
        time.sleep(0.01)

# Los siguientes hilos llaman a funciones donde los robots realizan movimientos de pick & place, prensado y soldado
def hilo_yaskawa():
    """Este hilo llama a la secuencia de movimientos pick->bending->place 
    de un tipo de planchas o otro. Para no depender de la salida digital 
    que se genera el objeto, se implemento una cola para cada sensor donde
    se guarda el objeto una vez el sensor detecte que hay un objeto.
    Así la información es más persistente en tiempo de ejecución."""

    cola_ancha = variables.objetos_pendientes["SensorCA"]
    cola_larga = variables.objetos_pendientes["SensorCL"]
    
    while True:

        nombre_larga = cola_larga.get() 
        pp.pick_plancha_larga(nombre_larga)
        bending.bending_plancha_larga(nombre_larga)
        pp.place_cinta_main()
        variables.alternancia.put("larga") 

        nombre_ancha = cola_ancha.get() 
        pp.pick_plancha_ancha(nombre_ancha)
        bending.bending_plancha_ancha(nombre_ancha)
        pp.place_cinta_main()
        variables.alternancia.put("ancha") 

        time.sleep(0.01)

def hilo_abb_paletizado():
    """Hilo del abb paletizado que decide que tarea hace primero segun la logica de la automatización."""
    
    RDK = robolink.Robolink()

    while True:
        if RDK.getParam("tapaPuesta") == 1 and not variables.cola_cuadrosTapa.empty():
            pp.place_cuadro_acabada()
        elif RDK.getParam("planchaSoldada") == 1 and not variables.objetos_pendientes["SensorTapa"].empty():
            pp.place_tapa_en_mesa()
        elif RDK.getParam("mesaOcupada") == 0 and not variables.objetos_pendientes["SensorCM"].empty():
            pp.place_plancha_mesa()
        else:
            time.sleep(0.01)

def hilo_abb_soldador():
    """Hilo que ejecuta la secuencia de soldadura."""
    while True:
        soldar.iniciar()
        time.sleep(0.01)

# Hilos de sensores para detectar objetos en cada cinta.
def hilo_sensorCA():
    """Hilo del sensor de planchas anchas."""
    sensor.detectar_objeto("SensorCA", "FramePlanchaAncha")

def hilo_sensorCL():
    """Hilo del sensor de planchas largas."""
    sensor.detectar_objeto("SensorCL", "FramePlanchaLarga")

def hilo_sensorCM():
    """Hilo del sensor de la cinta principal."""
    sensor.detectar_objeto("SensorCM", "FramePlanchaMain")

def hilo_sensorTapa():
    """Hilo del sensor de tapas."""
    sensor.detectar_objeto("SensorTapa", "FrameTapa")

def hilo_sensorEtiqueta():
    """Hilo del sensor de la cinta de etiquetado."""
    sensor.detectar_objeto("SensorEtiqueta", "FrameEtiqueta")

def hilo_sensorFinalEtiqueta():
    """Hilo del sensor de la cinta de etiquetado."""
    sensor.detectar_objeto("SensorFinalEtiqueta", "FrameEtiqueta")

""" Lista para guardar todos los hilos que se van a ejecutar 
en la estación, el parametro name se usa darle cuando 
ocurra un error, que se imprima por mensaje el nombre del hilo."""
threads = [
    threading.Thread(target=hilo_cinta_larga, name="cinta_larga"),
    threading.Thread(target=hilo_cinta_ancha, name="cinta_ancha"),
    threading.Thread(target=hilo_cinta_main, name="cinta_main"),
    threading.Thread(target=hilo_cinta_tapa, name="cinta_tapa"),
    threading.Thread(target=hilo_cinta_etiquetado, name="cinta_etiquetado"),

    threading.Thread(target=hilo_yaskawa, name="yaskawa"),
    threading.Thread(target=hilo_abb_paletizado, name="paletizado"),
    threading.Thread(target=hilo_abb_soldador, name="soldador"),

    threading.Thread(target=hilo_sensorCA, name="sensor_ca"),
    threading.Thread(target=hilo_sensorCL, name="sensor_cl"),
    threading.Thread(target=hilo_sensorCM, name="sensor_cm"),
    threading.Thread(target=hilo_sensorTapa, name="sensor_tapa"),
    threading.Thread(target=hilo_sensorEtiqueta, name="sensor_etiqueta")
]

# Se inicializan todos los hilos a la vez
for t in threads:
    t.start()
