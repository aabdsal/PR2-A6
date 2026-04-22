import threading
from modulos_python.entorno import preparar_entorno
RDK, project_dir = preparar_entorno()

from modulos_python import pick, place, bending, soldar, sensor
from modulos_python import mover_cintas as mc
from robodk import robolink

def hilo_cinta_larga():
    RDK_Local = robolink.Robolink()
    mc.mover_cinta_larga(RDK_Local)

def hilo_cinta_ancha():
    RDK_Local = robolink.Robolink()
    mc.mover_cinta_ancha(RDK_Local)

def hilo_yaskawa():
    RDK_Local = robolink.Robolink()
    ultima = None
    while True:
        ca = int(RDK_Local.getParam("SensorCA") or 0)
        cl = int(RDK_Local.getParam("SensorCL") or 0)      

        if ca and not cl:
            pick.pick_plancha_ancha()
            bending.bending_plancha_ancha()
            ultima = "ancha"

        elif cl and not ca:
            pick.pick_plancha_larga()
            bending.bending_plancha_larga()
            ultima = "larga"

        elif ca and cl:
            if ultima == "ancha":
                pick.pick_plancha_larga()
                bending.bending_plancha_larga()
                ultima = "larga"
            else:
                pick.pick_plancha_ancha()
                bending.bending_plancha_ancha()
                ultima = "ancha"

def hilo_place_main():
    place.place_cinta_main()

def hilo_place_mesa():
    place.place_plancha_mesa()

def hilo_place_soldado():
    place.place_plancha_soldada()

def hilo_soldador():
    soldar.soldar_ini()

def hilo_sensorCA():
    sensor.detectar_objeto("planxaAncha", "SensorCA")

def hilo_sensorCL():
    sensor.detectar_objeto("Botella", "SensorCL")

def hilo_sensorCC():
    sensor.detectar_objeto("planxCuadro", "SensorCC")

threads = [
    threading.Thread(target=hilo_cinta_larga),
    threading.Thread(target=hilo_cinta_ancha),
    threading.Thread(target=hilo_yaskawa),
    threading.Thread(target=hilo_place_main),
    threading.Thread(target=hilo_place_mesa),
    threading.Thread(target=hilo_place_soldado),
    threading.Thread(target=hilo_soldador),
    threading.Thread(target=hilo_sensorCA),
    threading.Thread(target=hilo_sensorCL),
    threading.Thread(target=hilo_sensorCC),
]

for t in threads:
    t.start()
    t.daemon = True