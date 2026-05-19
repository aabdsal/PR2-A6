"""Este módulo ayuda al reseteo de la estación.

Establece parámetros a 0, devuelve las cintas a su 
posición original y elimina objetos."""

from robodk import robolink, robomath
from modulos_python import simulation as sim, variables as var
import json

def reset_cinta(mecanismos : list[str]):
    """Devuelve la cinta a la posición 0 y valida que exista el mecanismo."""
    RDK = robolink.Robolink()

    for nombre_cinta in mecanismos:
        item_cinta = RDK.Item(nombre_cinta, robolink.ITEM_TYPE_ROBOT)
        if not item_cinta.Valid():
            raise RuntimeError(RDK.ShowMessage(f"Cinta: {nombre_cinta} no existe, revisa nombres"))
        
        if item_cinta.Name() == var.mesa_giratoria:
            target_ini_mesa = RDK.Item("Inici", robolink.ITEM_TYPE_TARGET)
    
            if not target_ini_mesa.Valid():
                raise RuntimeError("Target de esquina inválido. Revisa nombres")
            
            item_cinta.MoveJ(target_ini_mesa)
            continue
        item_cinta.setJoints(robomath.Mat([[0]]))

def reset_param():
    """Carga los parámetros del JSON persistente y los reinicia a 0."""

    if not var.JSON_PARAM_PATH.exists():
        return
    with var.JSON_PARAM_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    parametros = data.get("parametros", []) if isinstance(data, dict) else data
    for nombre in parametros:
        sim.setDO(str(nombre), 0)

def eliminar_duplicados(frame_name : str):
    RDK = robolink.Robolink()
    
    frame = RDK.Item(frame_name, robolink.ITEM_TYPE_FRAME)
    if not frame.Valid():
            raise RuntimeError(RDK.ShowMessage(f"Frame: {frame_name} no existe, revisa nombres"))

    lista_objetos = frame.Childs()
    
    if not lista_objetos:
        return

    for idx in lista_objetos:
        idx.Delete()
    
eliminar_duplicados("FramePlanchaAncha")
eliminar_duplicados("FramePlanchaLarga")
eliminar_duplicados("FramePlanchaMain")
eliminar_duplicados("FrameTapa")
eliminar_duplicados("FrameEtiqueta")
eliminar_duplicados("Engranaje")

reset_param()
reset_cinta(var.mecanismos)
