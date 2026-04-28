from robodk import robolink
from robodk import robomath
from modulos_python import var

from modulos_python import simulation

def _mover_cinta(cinta_name: str, param_sensor: str, RDK : robolink.Robolink | None = None):

    if RDK is None:
        RDK = robolink.Robolink()
    
    cinta = RDK.Item(cinta_name, robolink.ITEM_TYPE_ROBOT)
    if not cinta.Valid():
        raise RuntimeError("El nombre de la cinta no existe")

    incremento = 15.0

    while param_sensor is not None and int(RDK.getParam(param_sensor) or 0) != 1:
        
        cinta.setJoints(cinta.Joints() + robomath.Mat([[incremento]]))
        

        robomath.pause(0.01)

def mover_cinta_ancha():
    _mover_cinta(var.cinta_ancha, "SensorCA")

def mover_cinta_larga():
    _mover_cinta(var.cinta_larga, "SensorCL")

def mover_cinta_tapa():
    _mover_cinta(var.cinta_tapa, "SensorTapa")

def mover_cinta_main(RDK : robolink.Robolink):
    simulation.waitDI("enCintaMain", 1)
    simulation.setDO("enCintaMain", 0)
    
    _mover_cinta(var.cinta_main, "SensorCC", RDK)

def mover_cinta_cuadro_acabada():
    simulation.waitDI("EnCinta", 1)
    simulation.setDO("EnCinta", 0)
        
    _mover_cinta(var.cinta_etiqueta, "SensorEtiqueta")
    simulation.ocultar_objeto("planchaAcabada")
