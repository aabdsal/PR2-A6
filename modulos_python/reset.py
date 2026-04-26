from robodk import robolink
from robodk import robomath
from modulos_python import simulation, var
import json

def reset_cinta(nombre_cinta : str):
    RDK = robolink.Robolink()

    item_cinta = RDK.Item(nombre_cinta, robolink.ITEM_TYPE_ROBOT)
    if not item_cinta.Valid():
        raise RuntimeError(RDK.ShowMessage(f"Cinta: {nombre_cinta} no existe, revisa nombres"))
    
    item_cinta.setJoints(robomath.Mat([[0]]))

def reset_param():
    if not var.JSON_PARAM_PATH.exists():
        return
    with var.JSON_PARAM_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    parametros = data.get("parametros", []) if isinstance(data, dict) else data
    for nombre in parametros:
        simulation.setDO(str(nombre), 0)

def reset_objetos():
    if not var.JSON_PARAM_PATH.exists():
        return
    with var.JSON_PARAM_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    info_objetos = data.get("info_objetos", {}) if isinstance(data, dict) else data
    for nombre in info_objetos:
        simulation.reemplazar_pos_objeto(nombre[0], nombre[1], nombre[2])

def borrar_duplicados():
    pass

reset_param()
reset_objetos()

reset_cinta("CintaLargoIni")
reset_cinta("CintaAnchoIni")
reset_cinta("CintaCuadroIni")
reset_cinta("CintaTapaInit")
reset_cinta("ABB Mesa Giratoria")

simulation.mostrar_objeto("planxaLarga")
simulation.mostrar_objeto("planxaAncha")

simulation.ocultar_objeto("planchaLarga2")
simulation.ocultar_objeto("planchaAncha2")
simulation.ocultar_objeto("planchaAcabada")
