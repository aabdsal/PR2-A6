from robodk import robolink    # RoboDK API
from robodk import robomath    # Robot toolbox

from modulos_python import simulation, var

def _mover_cinta(cinta_name: str, target_name: str):
    RDK = robolink.Robolink()
    cinta = RDK.Item(cinta_name)
    
    if cinta.Valid():
        target_cinta = RDK.Item(target_name, robolink.ITEM_TYPE_TARGET)
        
        if not target_cinta.Valid():
            raise RuntimeError("El nombre del target no existe, revisa nombres")
        
        cinta.MoveJ(target_cinta)
    else: raise RuntimeError("El nombre de la cinta no existe")

# programa de robodk cinta ancha
def mover_cinta_ancha():
    _mover_cinta("CintaAnchoIni", "Cinta Ancha Fin")

def mover_cinta_ancha_atras():
    _mover_cinta("CintaAnchoIni", "Cinta Ancha Ini")

# programa de robodk cinta larga
def mover_cinta_larga():
    _mover_cinta("CintaLargoIni", "Cinta Larga Fin")

def mover_cinta_larga_atras():
    _mover_cinta("CintaLargoIni", "Cinta Larga Ini")

# programas de robodk cinta cuadro avanza y cinta cuadro retrocede
def mover_cinta_main():
    RDK = robolink.Robolink()
    cinta = RDK.Item("CintaCuadroIni")
    
    if cinta.Valid():
        simulation.waitDI("enCintaMain", 1)
        simulation.setDO("enCintaMain", str(0))
    
    _mover_cinta("CintaCuadroIni", "CintaCuadroFin")

def mover_cinta_main_atras():
    RDK = robolink.Robolink()
    cinta = RDK.Item("CintaCuadroIni")
    
    if cinta.Valid():
        simulation.waitDI("EnMesa", 1)
        simulation.setDO("EnMesa", str(0))

    _mover_cinta("CintaCuadroIni", "CintaCuadroIni")

# programa de robodk cinta cuadro acabada
def mover_cinta_cuadro_acabada():
    RDK = robolink.Robolink()
    cinta = RDK.Item("CintaCuadroFini")
    
    if cinta.Valid():
        simulation.waitDI("EnCinta", 1)
        simulation.setDO("EnCinta", str(0))
        
        if not var.acabar:
            _mover_cinta("CintaCuadroFini", "CintaCuadroSoldadoFin")
            simulation.simulation_ocultar_objeto("planchaAcabada")
        else:
            _mover_cinta("CintaCuadroFini", "CintaCuadroSoldadoIni")
        var.acabar = True