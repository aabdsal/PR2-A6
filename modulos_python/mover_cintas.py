from robodk import robolink
from robodk import robomath
from modulos_python import simulation

def _mover_cinta(cinta_name: str, target_name: str, RDK : robolink.Robolink | None = None):
    
    INCREMENTO_MM = 100

    if RDK is None:
        RDK = robolink.Robolink()
    
    cinta = RDK.Item(cinta_name, robolink.ITEM_TYPE_ROBOT)
    
    if not cinta.Valid():
        raise RuntimeError("El nombre de la cinta no existe")

    target_cinta = RDK.Item(target_name, robolink.ITEM_TYPE_TARGET)

    if not target_cinta.Valid():
        raise RuntimeError("El nombre del target no existe, revisa nombres")

    cinta.MoveJ(cinta.Joints() + robomath.Mat(INCREMENTO_MM))

"""
if cinta.Valid():
    cinta.MoveJ(cinta.Joints() + robomath.Mat(robomath.Mat(INCREMENTO_MM)))

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
    _mover_cinta("CintaAnchoIni", "T_CintaAnchaFin")

def mover_cinta_larga():
    _mover_cinta("CintaLargoIni", "T_CintaLargaFin")

def mover_cinta_main(RDK : robolink.Robolink):
    simulation.waitDI("enCintaMain", 1)
    simulation.setDO("enCintaMain", 0)
    
    _mover_cinta("CintaCuadroIni", "T_CintaCuadroFin", RDK)

def mover_cinta_cuadro_acabada():
    simulation.waitDI("EnCinta", 1)
    simulation.setDO("EnCinta", 0)
        
    _mover_cinta("CintaCuadroFini", "CintaCuadroSoldadoFin")
    simulation.ocultar_objeto("planchaAcabada")
