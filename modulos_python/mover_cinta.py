"""Este módulo contiene las funciones necesarias para
simular el movimiento de los objetos sobre las cintas."""

import threading
import json
from pathlib import Path
from robodk import robolink, robomath
from modulos_python import mqtt, bbdd, variables as var, simulation as sim

def _mover_cinta(cinta_name, param_sensor, frame_name: str, objeto_plantilla : str | None = None):
    """Mueve una cinta mientras el sensor no detecte ningún objeto."""

    RDK = robolink.Robolink()
    
    cinta = RDK.Item(cinta_name, robolink.ITEM_TYPE_ROBOT)
    if not cinta.Valid():
        raise RuntimeError("El nombre de la cinta no existe")

    incremento = 15.0
    espacio_objetos = 1000
    restante = var.cinta_restante[cinta_name]
    
    while param_sensor is not None and int(RDK.getParam(param_sensor) or 0) != 1:

        if int(RDK.getParam("parada_emergencia") or 0) == 0:
            cinta.setJoints(cinta.Joints() + robomath.Mat([[incremento]]))
            restante -= incremento
            if objeto_plantilla and restante <= 0:
                RDK.Render(False)
                sim.duplicar_objeto(objeto_plantilla, frame_name)
                RDK.Render(True)
                restante += espacio_objetos
            robomath.pause(0.01)

    var.cinta_restante[cinta_name] = restante

def mover_cinta_larga():
    """Método que mueve la cinta por donde pasan las planchas largas, 
    y el sensor encargado de notificar si hay objeto es el SensorCL"""
    
    _mover_cinta(var.cinta_larga, "SensorCL", "FramePlanchaLarga", var.plantilla["larga"])
    sim.setDO("yaskawa_larga", 0)

def mover_cinta_ancha():
    """Método que mueve la cinta por donde pasan las planchas anchas, 
    y el sensor encargado de notificar si hay objeto es el SensorCA"""
    
    _mover_cinta(var.cinta_ancha, "SensorCA", "FramePlanchaAncha", var.plantilla["ancha"])
    sim.setDO("yaskawa_ancha", 0)

def mover_cinta_tapa():
    """Método que mueve la cinta por donde pasan las tapas, 
    y el sensor encargado de notificar si hay objeto es el SensorTapa"""

    _mover_cinta(var.cinta_tapa, "SensorTapa","FrameTapa", var.plantilla["tapa"])
    sim.setDO("abb_tapa", 0)

def mover_cinta_main():
    """Método que mueve la cinta principal, donde van las planchasLargas2 
    y planchasAnchas2. El sensor encargado de notificar si hay objeto es el SensorCM.

    Implementa una espera digital que se activa cuando el yaskawa pone una plancha prensada en la cinta"""

    sim.waitDI("enCintaMain", 1)
    sim.setDO("enCintaMain", 0)
    
    _mover_cinta(var.cinta_main, "SensorCM", "FramePlanchaMain")

def mover_cinta_cuadro_acabada():
    """Mueve la cinta final donde salen los cuadros eléctricos hacia el túnel.

    Implementa una espera digital que se activa cuando el ABB paletizado
    pone el cuadro con tapa en la cinta."""

    sim.waitDI("EnCintaEtiquetar", 1)
        
    _mover_cinta(var.cinta_etiqueta, "SensorEtiqueta", "FrameEtiqueta")
    
    RDK = robolink.Robolink()

    cuadro_etiquetado = var.cola_cuadrosAcabados.get()
    cuadro_obj = RDK.Item(cuadro_etiquetado, robolink.ITEM_TYPE_OBJECT)

    if not cuadro_obj.Valid():
        raise RuntimeError("Nombre de cuadro no válido, revisa errores")
    
    robomath.pause(2.0)
    
    ruta_pentapanel = (Path(__file__).resolve().parents[1] / "web" / "images/pentapanel.png").as_posix()
    pentapanel = sim.crear_pegatina_obj(RDK, ruta_pentapanel, var.frame_cinta_etiqueta, 0.0003)

    if pentapanel.Valid():
        pentapanel.setParentStatic(cuadro_obj)
        pose_etiqueta = (robomath.transl(70, -160, 100) * robomath.rotx(robomath.pi) * robomath.rotz(robomath.pi))    
        pentapanel.setPose(pose_etiqueta)
        pentapanel.setName("pentapanel" + cuadro_obj.Name())
    
    if not var.cola_etiquetas.empty():

        ruta_rel = var.cola_etiquetas.get()
        ruta_abs = (Path(__file__).resolve().parents[1] / "web" / ruta_rel).as_posix()
        pegatina = sim.crear_pegatina_obj(RDK, ruta_abs, var.frame_cinta_etiqueta, 0.0001)

        if pegatina.Valid():
            pegatina.setParentStatic(cuadro_obj)
            pose_etiqueta = (robomath.transl(70, 130, 100))    
            pegatina.setPose(pose_etiqueta)
            pegatina.setName("pegatina" + cuadro_obj.Name())

        robomath.pause(3.0)

    _mover_cinta(var.cinta_etiqueta, "SensorFinalEtiqueta", "FrameEtiqueta")
    
    sim.setDO("EnCintaEtiquetar", 0)

    mensaje = json.dumps({
        "estado_led": "on",
    })
    mqtt.enviar_message(mqtt.led_topic, mensaje)

    robomath.pause(3.0)

    RDK.Render(False)
    cuadro_obj.setVisible(False)
    cuadro_obj.Delete()
    RDK.Render(True)

    threading.Thread(target=bbdd.actualizar_unidad).start()
