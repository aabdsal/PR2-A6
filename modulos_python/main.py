"""Archivo principal que ejecuta todas las acciones de los distintos módulos.

Se caracteriza por el uso de hilos para cada acción o conjunto de acciones
necesarias para la automatización de cuadros eléctricos.

El uso de hilos permite ejecutar instancias en paralelo, por ejemplo mover
cintas o coordinar robots simultáneamente."""

from modulos_python.entorno import preparar_entorno
preparar_entorno()

from modulos_python import bending, sensor, soldar, variables, mqtt, bbdd
from modulos_python import mover_cintas as mc
from modulos_python import pick_place as pp
from robodk import robolink
import threading

mqtt.conectar()
bbdd.conectar()

def _thread_excepthook(args):
    """Se hace uso de este método interno para imprimir por pantalla los errores que 
    surjan en tiempo de ejecución, es muy útil porque nos dice en que hilo ha fallado 
    y devuelve el mensaje que elevan las excepciones en las funciones internas al hilo."""

    RDK = robolink.Robolink()

    RDK.ShowMessage(f"[ThreadError] {args.thread.name}: {args.exc_type.__name__}: {args.exc_value}")

threading.excepthook = _thread_excepthook

# Los siguientes hilos mueven las cintas por donde llegan los objetos.
# TODO : falta sustituir esos while true de las cintas a que se vuelva a mover despues de que el robot mueva el objeto

def hilo_cinta_larga():
    """Hilo que mueve la cinta de planchas largas."""
    #while True:
    mc.mover_cinta_larga()

def hilo_cinta_ancha():
    """Hilo que mueve la cinta de planchas anchas."""
    #while True:
    mc.mover_cinta_ancha()

def hilo_cinta_tapa():
    """Hilo que mueve la cinta de tapas."""
    #while True:
    mc.mover_cinta_tapa()

def hilo_yaskawa():
    """Este hilo llama a la secuencia de movimientos pick->bending->place de un 
    tipo de planchas o otro. Para no depender de la salida digital que se genera
    el objeto, se implemento una cola para sensor donde se guarda el objeto una
    vez el sensor detecte que hay un objeto.
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

def hilo_cinta_main():
    """Hilo que mueve la cinta principal cuando hay pieza disponible."""
    RDK = robolink.Robolink()
    while True:
        mc.mover_cinta_main(RDK)

def hilo_place_mesa():
    """Hilo que coloca planchas en la mesa giratoria desde la cinta principal."""
    while True:
        pp.place_plancha_mesa()

def hilo_place_tapa():
    """Hilo que coloca la tapa sobre el cuadro soldado."""
    while True:
        pp.place_tapa_en_mesa()

def hilo_place_cuadro_acabado():
    """Hilo que coloca el cuadro acabado en la cinta de etiquetado."""
    while True:
        pp.place_cuadro_acabada()

def hilo_soldador():
    """Hilo que ejecuta la secuencia de soldadura."""
    while True:
        soldar.soldar_ini()

def hilo_cinta_etiquetado():
    """Hilo que mueve la cinta final de etiquetado."""
    while True:
        mc.mover_cinta_cuadro_acabada()

# Hilos de sensores para detectar objetos en cada cinta.
def hilo_sensorCA():
    """Hilo del sensor de planchas anchas."""
    sensor.detectar_objeto("SensorCA", "FramePlanchaAncha")

def hilo_sensorCL():
    """Hilo del sensor de planchas largas."""
    sensor.detectar_objeto("SensorCL", "FramePlanchaLarga")

def hilo_sensorCC():
    """Hilo del sensor de la cinta principal."""
    sensor.detectar_objeto("SensorCC", "FramePlanchaMain")

def hilo_sensorTapa():
    """Hilo del sensor de tapas."""
    sensor.detectar_objeto("SensorTapa", "FrameTapa")

def hilo_sensorEtiqueta():
    """Hilo del sensor de la cinta de etiquetado."""
    sensor.detectar_objeto("SensorEtiqueta", "FrameCuadroAcabada")

def hilo_bbdd():
    bbdd.leer_fotocelulas_robodk()

""" Lista para guardar todos los hilos que se van a ejecutar 
en la estación, el parametro name se usa darle cuando 
ocurra un error,que se imprima por mensaje el nombre del hilo."""
threads = [
    threading.Thread(target=hilo_cinta_larga, name="cinta_larga"),
    threading.Thread(target=hilo_cinta_ancha, name="cinta_ancha"),
    threading.Thread(target=hilo_cinta_tapa, name="cinta_tapa"),
    threading.Thread(target=hilo_yaskawa, name="yaskawa"),
    threading.Thread(target=hilo_cinta_main, name="cinta_main"),
    threading.Thread(target=hilo_place_mesa, name="place_mesa"),
    threading.Thread(target=hilo_place_cuadro_acabado, name="place_cuadro"),
    threading.Thread(target=hilo_place_tapa, name="place_tapa"),
    threading.Thread(target=hilo_cinta_etiquetado, name="cinta_etiquetado"),
    threading.Thread(target=hilo_soldador, name="soldador"),
    threading.Thread(target=hilo_sensorCA, name="sensor_ca"),
    threading.Thread(target=hilo_sensorCL, name="sensor_cl"),
    threading.Thread(target=hilo_sensorCC, name="sensor_cc"),
    threading.Thread(target=hilo_sensorTapa, name="sensor_tapa"),
    threading.Thread(target=hilo_sensorEtiqueta, name="sensor_etiqueta"),
    threading.Thread(target=hilo_bbdd, name="base_datos")
]

for t in threads:
    t.start()
    