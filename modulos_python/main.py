import threading
import traceback

from modulos_python.entorno import preparar_entorno
preparar_entorno()

from modulos_python import bending, sensor, var, soldar
from modulos_python import mover_cintas as mc
from modulos_python import pick_place as pp
from robodk import robolink
from robodk import robomath

def getIniPose():
    RDK = robolink.Robolink()
    lista_ini_objetos = RDK.ItemList(robolink.ITEM_TYPE_OBJECT)

    for idx in lista_ini_objetos:
        if isinstance(idx, str):
            idx = RDK.Item(idx) 
        
        var.registrar_info_objeto_json(idx.Name(), str(idx.Pose()), str(idx.Parent().Name()))

#getIniPose()
robomath.pause(0.5)

def _thread_excepthook(args):
    RDK = robolink.Robolink()

    RDK.ShowMessage(f"[ThreadError] {args.thread.name}: {args.exc_type.__name__}: {args.exc_value}")
    traceback.print_exception(args.exc_type, args.exc_value, args.exc_traceback)

threading.excepthook = _thread_excepthook

def hilo_cinta_larga():
    #while True:
    mc.mover_cinta_larga()

def hilo_cinta_ancha():
    #while True:
    mc.mover_cinta_ancha()

def hilo_cinta_tapa():
    #while True:        
    mc.mover_cinta_tapa()

def hilo_yaskawa():
    cola_ancha = var.objetos_pendientes["SensorCA"]
    cola_larga = var.objetos_pendientes["SensorCL"]
    
    while True:
        # Esta es una forma más simple y segura de alternar
        # Espera a que haya una plancha larga disponible
        nombre_larga = cola_larga.get() 
        pp.pick_plancha_larga(nombre_larga)
        bending.bending_plancha_larga(nombre_larga)
        pp.place_cinta_main()
        var.alternancia.put("larga") # Informa de que la siguiente es una larga

        # Espera a que haya una plancha ancha disponible
        nombre_ancha = cola_ancha.get()
        pp.pick_plancha_ancha(nombre_ancha)
        bending.bending_plancha_ancha(nombre_ancha)
        pp.place_cinta_main()
        var.alternancia.put("ancha") # Informa de que la siguiente es una ancha


def hilo_cinta_main():
    RDK = robolink.Robolink()
    while True:
        mc.mover_cinta_main(RDK)

# me falta revisar si me fa falta robolink, mirarme lo de duplicar objectes e implementar logica: 
# cintas -> bending -> cinta main -> mesa giratoria -> soldar -> tapa -> mesa -> cuadro -> cinta main 2 -> etiqueta -> salida
def hilo_place_mesa():
    cola_main = var.objetos_pendientes["SensorCC"]
    while True:
        pp.place_plancha_mesa(cola_main.get())

def hilo_place_tapa():
    while True:
        pp.place_tapa_en_mesa()

def hilo_place_cuadro_acabado():
    while True:
        pp.place_cuadro_acabada()

def hilo_soldador():
    while True:
        soldar.soldar_ini()

def hilo_cinta_etiquetado():
    while True:
        mc.mover_cinta_cuadro_acabada()

def hilo_sensorCA():
    sensor.detectar_objeto("SensorCA", "FramePlanchaAncha")

def hilo_sensorCL():
    sensor.detectar_objeto("SensorCL", "FramePlanchaLarga")

def hilo_sensorCC():
    sensor.detectar_objeto("SensorCC", "FramePlanchaMain")

def hilo_sensorTapa():
    sensor.detectar_objeto("SensorTapa", "FrameTapa")

def hilo_sensorEtiqueta():
    sensor.detectar_objeto("SensorEtiqueta", "FrameCuadroAcabada")

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
    threading.Thread(target=hilo_sensorEtiqueta, name="sensor_etiqueta")
]

for t in threads:
    t.start()
    