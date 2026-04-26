from robodk import robolink
from robodk import robomath
from modulos_python import simulation, var
import time

def _mover_cinta(cinta_name: str, stop_param: str, RDK : robolink.Robolink | None = None):

    if RDK is None:
        RDK = robolink.Robolink()
    
    cinta = RDK.Item(cinta_name, robolink.ITEM_TYPE_ROBOT)
    
    if not cinta.Valid():
        raise RuntimeError("El nombre de la cinta no existe")

    incremento = 20.0

    while stop_param is not None and int(RDK.getParam(stop_param) or 0) != 1:

        cinta.setJoints(cinta.Joints() + robomath.Mat([[incremento]]))
        
        robomath.pause(0.01)

"""
    botella.Copy()
    botellaCopia = RDK.Paste(sistRefCinta)
    nbotella = int(RDK.getParam('num_botellas'))
    nbotella = nbotella + 1
    count = str(nbotella)
    botellaCopia.setName('Botella' + count)
    botellaCopia.setPose(botella.Pose()*robomath.transl(-INCREMENTO_MM*nbotella, 0, 0))
    RDK.setParam('num_botellas', str(nbotella))
"""

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
