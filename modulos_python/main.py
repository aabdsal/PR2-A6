import threading
import traceback
from modulos_python.entorno import preparar_entorno

preparar_entorno()

from modulos_python import pick, place, bending, soldar, sensor, var
from modulos_python import mover_cintas as mc
from robodk import robolink
from robodk import robomath


def _thread_excepthook(args):
    RDK = robolink.Robolink()
    # Make uncaught thread failures explicit instead of failing silently.
    RDK.ShowMessage(f"[ThreadError] {args.thread.name}: {args.exc_type.__name__}: {args.exc_value}")
    traceback.print_exception(args.exc_type, args.exc_value, args.exc_traceback)

threading.excepthook = _thread_excepthook

def hilo_cinta_larga():
    mc.mover_cinta_larga()

def hilo_cinta_ancha():
    mc.mover_cinta_ancha()

def hilo_yaskawa():
    """ que piezas pendientes tengo en cola """
    
    RDK = robolink.Robolink()

    ultima = None
    
    cola_ancha = var.objetos_pendientes["SensorCA"]
    cola_larga = var.objetos_pendientes["SensorCL"]
    
    while True:
        
        if not cola_ancha.empty():
            obj1 = cola_ancha.get()
            pick.pick_plancha_ancha()
            
            if obj1 is not None:
                RDK.ShowMessage(f"objeto consumido: {obj1.Name()}", False)
            
            bending.bending_plancha_ancha()
            place.place_cinta_main()
            #ultima = "ancha"
        elif not cola_larga.empty():
            obj2 = cola_larga.get()
            pick.pick_plancha_larga()
            
            if obj2 is not None:
                RDK.ShowMessage(f"objeto consumido: {obj2.Name()}", False)
            
            bending.bending_plancha_larga()
            place.place_cinta_main()
            #ultima = "larga"

        else:
            RDK.ShowMessage(f"no esta haciendo nada el hilo_yaskawa", False)
            robomath.pause(0.01)

def hilo_cinta_main():
    RDK = robolink.Robolink()
    while True:
        mc.mover_cinta_main(RDK)

def hilo_place_mesa():
    while True:
        place.place_plancha_mesa()

def hilo_place_soldado():
    while True:
        place.place_plancha_soldada()

def hilo_soldador():
    while True:
        soldar.soldar_ini()

def hilo_sensorCA():
    sensor.detectar_objeto("SensorCA", "FramePlanchaAncha")

def hilo_sensorCL():
    sensor.detectar_objeto("SensorCL", "FramePlanchaLarga")

def hilo_sensorCC():
    sensor.detectar_objeto("SensorCC", "PlanchaCuadro")

def hilo_loggs():
    RDK = robolink.Robolink()
    
    cola_ancha = var.objetos_pendientes["SensorCA"]
    cola_larga = var.objetos_pendientes["SensorCL"]
    
    while True:
        RDK.ShowMessage(f"Objeto pendiente en ancha: {cola_ancha.qsize()} y larga: {cola_larga.qsize()}", False)
        robomath.pause(0.5)

def hilo_getIniPose():
    RDK = robolink.Robolink()
    lista_ini_objetos = RDK.ItemList(robolink.ITEM_TYPE_OBJECT)

    for idx in lista_ini_objetos:
        if isinstance(idx, str):
            idx = RDK.Item(idx) 
        
        var.objeto_pose[idx.Name()] = idx.Pose()

threads = [
    #threading.Thread(target=hilo_loggs, daemon= True),
    threading.Thread(target=hilo_cinta_larga, name="cinta_larga"),
    threading.Thread(target=hilo_cinta_ancha, name="cinta_ancha"),
    threading.Thread(target=hilo_yaskawa, name="yaskawa"),
    threading.Thread(target=hilo_cinta_main, name="cinta_main"),
    threading.Thread(target=hilo_place_mesa, name="place_mesa"),
    threading.Thread(target=hilo_place_soldado, name="place_soldado"),
    threading.Thread(target=hilo_soldador, name="soldador"),
    threading.Thread(target=hilo_sensorCA, name="sensor_ca"),
    threading.Thread(target=hilo_sensorCL, name="sensor_cl"),
    threading.Thread(target=hilo_sensorCC, name="sensor_cc")
]

for t in threads:
    t.start()
    