"""Este archivo de Python es clave para la simulación en RoboDK.

Incluye métodos para ocultar/mostrar objetos, reemplazar posiciones,
adjuntar o soltar objetos, simular esperas digitales, establecer
salidas digitales y duplicar objetos."""

from robodk import robolink, robomath    
from typing import Optional
from modulos_python import variables as var
from threading import Lock
from pathlib import Path
from PIL import Image
import uuid

_copy_lock = Lock()

RDK = robolink.Robolink()

def ocultar_objeto(object_name: str):
    """Este método oculta el objeto que se le pasa por parámetro"""

    obj = RDK.Item(object_name, robolink.ITEM_TYPE_OBJECT)

    if not obj.Valid():
        raise Exception(RDK.ShowMessage("El nombre del objeto no existe"))

    obj.setVisible(False)

def mostrar_objeto(object_name: str):
    """Este método muestra el objeto que se le pasa por parámetro"""

    obj = RDK.Item(object_name, robolink.ITEM_TYPE_OBJECT)

    if not obj.Valid():
        raise Exception(RDK.ShowMessage("El nombre del objeto no existe"))

    obj.setVisible(True)

def reemplazar_pos_objeto(object_name, parent: str,  pose : robomath.Mat):
    """Reemplaza la posición de un objeto respecto a su frame padre.

    Actualmente no se usa en el flujo principal y podría quedar obsoleta
    con el uso de objetos plantilla."""

    item = RDK.Item(object_name, robolink.ITEM_TYPE_OBJECT)
    if not item.Valid():
        raise Exception(RDK.ShowMessage("El nombre del objeto no existe"))

    parent_frame = RDK.Item(parent, robolink.ITEM_TYPE_TARGET)

    if not parent_frame.Valid():
        raise Exception(RDK.ShowMessage("No hay nada en objeto_parent"))

    item.setParentStatic(parent_frame)

    item.setPoseAbs(pose)

def adjuntar_objeto(tool_name: robolink.Item, object_name: Optional[str] = None):
    """Adjunta un objeto al TCP de la herramienta.

    Si se indica un nombre, se adjunta ese objeto. Si no, se usa AttachClosest."""

    if object_name is not None:
        attached = RDK.Item(object_name, robolink.ITEM_TYPE_OBJECT)
        if not attached.Valid():
            raise Exception("No se ha adjuntado ningun objeto")

        attached.setParentStatic(tool_name)
    else:
        attached = tool_name.AttachClosest()

    var.objetos_tcp[tool_name.Name()] = attached

def soltar_objeto(tool_name: str, frame_name: robolink.Item):
    """Suelta el objeto adjuntado en la herramienta dentro de un frame.

    Usa un diccionario para asegurar qué objeto está adjuntado a cada TCP."""

    if tool_name not in var.objetos_tcp:
        raise Exception("O la herramienta no existe o no se la ha asignado ningun objeto")

    obj = var.objetos_tcp.get(tool_name)
    if obj is not None and obj.Valid():
        obj.setParentStatic(frame_name)

    tool = RDK.Item(tool_name, robolink.ITEM_TYPE_TOOL)
    if tool.Valid():
        tool.DetachAll(frame_name)

    var.objetos_tcp.pop(tool_name, None)

def waitDI(param_name : str, valor : int):
    """Este método simula una espera digital mediante 
    un bucle con condicion de si un parametro esta a 0 o a 1,
    se realiza una pausa para que no vaya tan petado."""

    while int(RDK.getParam(param_name) or 0) != valor:
        robomath.pause(0.01)

def setDO(param_name: str, valor: int):
    """Guarda el parámetro en JSON y establece el valor en la estación."""

    var.registrar_parametro_json(param_name)
    RDK.setParam(param_name, str(valor))

def duplicar_objeto(plantilla_name: str, frame_name: str):
    """Crea un duplicado de un objeto plantilla dentro de un frame.

    También contabiliza el número de duplicados para información persistente."""

    plantilla_item = RDK.Item(plantilla_name, robolink.ITEM_TYPE_OBJECT)
    frame_item = RDK.Item(frame_name, robolink.ITEM_TYPE_FRAME)

    if not plantilla_item.Valid():
        raise RuntimeError(f"El objeto plantilla '{plantilla_name}' no existe. Revisa los nombres.")

    if not frame_item.Valid():
        raise RuntimeError(f"El frame de destino '{frame_name}' no existe. Revisa los nombres.")

    with _copy_lock:
        plantilla_item.Copy()
        
        pasted = RDK.Paste(frame_item)

        duplicado: Optional[robolink.Item] = None
        if isinstance(pasted, list):
            if len(pasted) == 0:
                raise Exception("No se pudo pegar el objeto duplicado.")
            duplicado = pasted[0]
        else:
            duplicado = pasted

        if duplicado is None or not duplicado.Valid():
            raise Exception("No se pudo crear el duplicado del objeto.")

        duplicado.setPoseAbs(plantilla_item.PoseAbs())
        #duplicado.setParentStatic(frame_item)
        duplicado.setVisible(True)

        param_name = "numero_" + plantilla_name.replace("plantilla_", "")
        
        if RDK.getParam(param_name) is None:
            RDK.setParam(param_name, '0')

        count = int(RDK.getParam(param_name)) + 1
        RDK.setParam(param_name, str(count))
        
        nombre_base = param_name.replace("numero_", "")
        duplicado.setName(f"{nombre_base}_{count}")
        
        return duplicado

def crear_pegatina_obj(RDK : robolink.Robolink, ruta_png, frame_name, px_to_m, nombre_base="label"):

    assets_dir = Path(__file__).resolve().parents[1] / "modulos_python" / "labels"
    assets_dir.mkdir(parents=True, exist_ok=True)

    base = f"{nombre_base}_{uuid.uuid4().hex}"
    obj_path = assets_dir / f"{base}.obj"
    mtl_path = assets_dir / f"{base}.mtl"

    # Leer dimensiones de la imagen
    with Image.open(ruta_png) as img:
        width_px, height_px = img.size

    w = width_px * px_to_m
    h = height_px * px_to_m
    
    obj_path.write_text(
        "mtllib {mtl}\n"
        f"v {-w/2} {-h/2} 0\n"
        f"v {w/2} {-h/2} 0\n"
        f"v {w/2} {h/2} 0\n"
        f"v {-w/2} {h/2} 0\n"
        "vt 0 0\nvt 1 0\nvt 1 1\nvt 0 1\n"
        "usemtl mat0\n"
        "f 1/1 2/2 3/3 4/4\n".format(mtl=mtl_path.name),
        encoding="utf-8"
    )

    mtl_path.write_text(
        "newmtl mat0\n"
        "Kd 1.000 1.000 1.000\n"
        "d 1.0\n"
        f"map_Kd {Path(ruta_png).as_posix()}\n"
        f"map_d {Path(ruta_png).as_posix()}\n",
        encoding="utf-8"
    )

    frame = RDK.Item(frame_name, robolink.ITEM_TYPE_FRAME)
    pegatina = RDK.AddFile(str(obj_path), frame)
    return pegatina