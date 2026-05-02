"""Este módulo ayuda al reseteo de la estación.

Establece parámetros a 0 y devuelve las cintas a su posición original.
Mientras no exista una duplicación consistente de objetos, se usan
ocultar/mostrar para mantener la simulación coherente.
"""

from robodk import robolink
from robodk import robomath
from modulos_python import variables
import json

from modulos_python import simulation

def reset_cinta(nombre_cinta : str):
    """Devuelve la cinta a la posición 0 y valida que exista el mecanismo."""
    RDK = robolink.Robolink()

    item_cinta = RDK.Item(nombre_cinta, robolink.ITEM_TYPE_ROBOT)
    if not item_cinta.Valid():
        raise RuntimeError(RDK.ShowMessage(f"Cinta: {nombre_cinta} no existe, revisa nombres"))
    
    item_cinta.setJoints(robomath.Mat([[0]]))

def reset_param():
    """Carga los parámetros del JSON persistente y los reinicia a 0."""

    if not variables.JSON_PARAM_PATH.exists():
        return
    with variables.JSON_PARAM_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    parametros = data.get("parametros", []) if isinstance(data, dict) else data
    for nombre in parametros:
        simulation.setDO(str(nombre), 0)

def reset_objetos():
    """Función obsoleta para reemplazar posiciones de objetos.

    Se mantiene temporalmente; se pretende sustituir por duplicado/eliminación.
    """

    if not variables.JSON_PARAM_PATH.exists():
        return
    with variables.JSON_PARAM_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    info_objetos = data.get("info_objetos", {}) if isinstance(data, dict) else data
    for nombre in info_objetos:
        simulation.reemplazar_pos_objeto(nombre[0], nombre[1], nombre[2])

# Llamadas a las funciones de reset
reset_param()
# TODO: Simplificar pasando una lista con los nombres de todas las cintas.
reset_cinta(variables.cinta_larga)
reset_cinta(variables.cinta_ancha)
reset_cinta(variables.cinta_main)
reset_cinta(variables.cinta_tapa)
reset_cinta(variables.mesa_giratoria)


# TODO: Revisar esta parte cuando la duplicación sea consistente.
simulation.mostrar_objeto("planchaLarga")
simulation.mostrar_objeto("planchaAncha")
simulation.mostrar_objeto("tapaCuadro")

simulation.ocultar_objeto("planchaLarga2")
simulation.ocultar_objeto("planchaAncha2")
simulation.ocultar_objeto("planchaSoldada")
simulation.ocultar_objeto("cuadroConTapa")
