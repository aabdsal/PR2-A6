from robodk import robolink
from robodk import robomath
from modulos_python import simulation
import time

def _mover_cinta(cinta_name: str, target_name: str, RDK : robolink.Robolink | None = None, stop_param: str | None = None):

    if RDK is None:
        RDK = robolink.Robolink()
    
    cinta = RDK.Item(cinta_name, robolink.ITEM_TYPE_ROBOT)
    
    if not cinta.Valid():
        raise RuntimeError("El nombre de la cinta no existe")

    target_cinta = RDK.Item(target_name, robolink.ITEM_TYPE_TARGET)

    if not target_cinta.Valid():
        raise RuntimeError("El nombre del target no existe, revisa nombres")

    tiempo_prev = time.perf_counter()
    velocidad = 100.0

    while stop_param is not None and int(RDK.getParam(stop_param) or 0) != 1:
        tiempo_actual = time.perf_counter()
        diferencia = tiempo_actual - tiempo_prev
        incremento = velocidad * diferencia

        cinta.setJoints(cinta.Joints() + robomath.Mat([[incremento]]))
        
        tiempo_prev = tiempo_actual
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
    _mover_cinta("CintaAnchoIni", "T_CintaAnchaFin", stop_param="SensorCA")

def mover_cinta_larga():
    _mover_cinta("CintaLargoIni", "T_CintaLargaFin", stop_param="SensorCL")

def mover_cinta_main(RDK : robolink.Robolink):
    simulation.waitDI("enCintaMain", 1)
    simulation.setDO("enCintaMain", 0)
    
    _mover_cinta("CintaCuadroIni", "T_CintaCuadroFin", RDK, stop_param="SensorCC")

def mover_cinta_cuadro_acabada():
    simulation.waitDI("EnCinta", 1)
    simulation.setDO("EnCinta", 0)
        
    _mover_cinta("CintaCuadroFini", "CintaCuadroSoldadoFin")
    simulation.ocultar_objeto("planchaAcabada")
