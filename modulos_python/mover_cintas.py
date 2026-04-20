from robodk import robolink    # RoboDK API
from robodk import robomath    # Robot toolbox
RDK = robolink.Robolink()

from modulos_python import simulation, var

def _mover_cinta(cinta_name: str, target_name: str):
    cinta = RDK.Item(cinta_name)
    if cinta.Valid():
        target_cinta = RDK.Item(target_name, robolink.ITEM_TYPE_TARGET)
        cinta.MoveJ(target_cinta)
    else: raise RuntimeError("El nombre de la cinta no existe")

# programa de robodk cinta ancha
def mover_cinta_ancha():
    _mover_cinta("CintaAnchoIni", "Cinta Ancha Fin")
    var.detecta_ancha = True

def mover_cinta_ancha_atras():
    _mover_cinta("CintaAnchoIni", "Cinta Ancha Ini")

# programa de robodk cinta larga
def mover_cinta_larga():
    _mover_cinta("CintaLargoIni", "Cinta Larga Fin")
    var.detecta_larga = True

def mover_cinta_larga_atras():
    _mover_cinta("CintaLargoIni", "Cinta Larga Ini")

# programas de robodk cinta cuadro avanza y cinta cuadro retrocede
def mover_cinta_main():
    _mover_cinta("CintaCuadroIni", "CintaCuadroFin")
    var.sensor_cuadro = True

def mover_cinta_main_atras():  
    if var.en_mesa:
        _mover_cinta("CintaCuadroIni", "CintaCuadroIni")

# programa de robodk cinta cuadro acabada
def mover_cinta_cuadro_acabada():

    if var.en_cinta:
        if not var.acabar:
            _mover_cinta("CintaCuadroFini", "CintaCuadroSoldadoFin")
            simulation.simulation_ocultar_objeto("planchaAcabada")
        else:
            _mover_cinta("CintaCuadroFini", "CintaCuadroSoldadoIni")
        var.acabar = True