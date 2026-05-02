"""Este modulo ayuda a la parte de reseteo de la estación, 
ya que establece todos los parámetros a 0 y devuelve las cintas a su posición original.


También se hace uso de simulaciones de ocultar/mostrar objeto, pero es porque aún no 
se ha implementado de forma consistente la duplicación de objetos.
Se prevee que se implemente en el futuro un método para eliminar todos los duplicados
generados en tiempo de ejecución y se deje solo las plantillas, aún está por decidir 
si se implemetara en este módulo o en el módulo de simulación.
"""

from robodk import robolink
from robodk import robomath
from modulos_python import variables
import json

from modulos_python import simulation

def reset_cinta(nombre_cinta : str):
    """Devuelve la posición de la cinta al 0 comprobando que el nombre de la cinta existe y correponde a un mecanismo tipo robot"""
    RDK = robolink.Robolink()

    item_cinta = RDK.Item(nombre_cinta, robolink.ITEM_TYPE_ROBOT)
    if not item_cinta.Valid():
        raise RuntimeError(RDK.ShowMessage(f"Cinta: {nombre_cinta} no existe, revisa nombres"))
    
    item_cinta.setJoints(robomath.Mat([[0]]))

def reset_param():
    """Esta funcion hace uso de la información persistente en el archivo parametro.json 
    al cargar todos los nombres de los parametros que se han usado en la simulación y los establece a 0.
    
    Es muy útil por que así no necesitamos saber los nombres especificos de todos 
    los parametros que se van usando a lo largo de la simulación."""

    if not variables.JSON_PARAM_PATH.exists():
        return
    with variables.JSON_PARAM_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    parametros = data.get("parametros", []) if isinstance(data, dict) else data
    for nombre in parametros:
        simulation.setDO(str(nombre), 0)

def reset_objetos():
    """Función que supuestamente reemplazara la posición de un objeto, aunque sinceramente voy a deprecarla, 
    ya que voy a usar el metodo de duplicar eliminar objetos -- Ali Abdelhamid"""

    if not variables.JSON_PARAM_PATH.exists():
        return
    with variables.JSON_PARAM_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    info_objetos = data.get("info_objetos", {}) if isinstance(data, dict) else data
    for nombre in info_objetos:
        simulation.reemplazar_pos_objeto(nombre[0], nombre[1], nombre[2])

# llamadas a las funciones de reset
reset_param()
# esto se podria simplificar pasandole como parametro una lsita con los nombres de todas las cintas, luego se implementa
reset_cinta(variables.cinta_larga)
reset_cinta(variables.cinta_ancha)
reset_cinta(variables.cinta_main)
reset_cinta(variables.cinta_tapa)
reset_cinta(variables.mesa_giratoria)


# Esto tambien debo de quitarlo
simulation.mostrar_objeto("planchaLarga")
simulation.mostrar_objeto("planchaAncha")
simulation.mostrar_objeto("tapaCuadro")

simulation.ocultar_objeto("planchaLarga2")
simulation.ocultar_objeto("planchaAncha2")
simulation.ocultar_objeto("planchaSoldada")
simulation.ocultar_objeto("cuadroConTapa")
