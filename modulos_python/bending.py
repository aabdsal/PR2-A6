"""Este módulo implementa los movimientos necesarios
para el prensado de planchas largas y anchas.

Se apoya en la API de RoboDK, variables globales 
y simulaciones que representan acciones reales."""

from robodk import robolink   
from modulos_python import variables
from modulos_python import simulation as sim

def _transicion_objeto(obj_from_plantilla, obj_to_plantilla: str, frame, tool: robolink.Item):
    """Intercambia el objeto que tiene el Yaskawa MH24 por el siguiente.

    Se apoya en objetos plantilla definidos en variables.py, ubicados en la
    posición absoluta donde el robot debe recogerlos. La lógica de duplicado
    y limpieza de objetos está pendiente y se mantiene comentada.
    """
    
    RDK = robolink.Robolink()

    sim.soltar_objeto(variables.tool_yaskawa, frame)

    obj_from = RDK.Item(obj_from_plantilla)
    if not obj_from.Valid():
        raise RuntimeError("objeto no existe, revisa nombres")
    
    obj_to = RDK.Item(obj_to_plantilla)
    if not obj_to.Valid():
        raise RuntimeError("objeto no existe, revisa nombres")
    
    sim.ocultar_objeto(obj_from.Name())
    obj_from.Delete()

    nuevo_objeto = sim.duplicar_objeto(obj_to_plantilla, frame.Name())

    variables.objetos_tcp[variables.tool_yaskawa] = sim.adjuntar_objeto(tool, nuevo_objeto.Name())
    
    return nuevo_objeto.Name()

def _bending_generico(bend_1: str, bend_2: str, obj_0: str, obj_1: str, obj_2: str):
    """Ejecuta la secuencia de movimientos del Yaskawa MH24.

    Configura los items necesarios (robot, frame, herramienta y targets),
    realiza el intercambio de objetos y, al finalizar, activa la salida
    digital para permitir el place en la cinta."""

    RDK = robolink.Robolink()

    r = RDK.Item(variables.robot_yaskawa, robolink.ITEM_TYPE_ROBOT)
    sistRefBend = RDK.Item("Bending", robolink.ITEM_TYPE_FRAME)
    toolR = RDK.Item(variables.tool_yaskawa, robolink.ITEM_TYPE_TOOL)

    # principio
    home = RDK.Item("Home", robolink.ITEM_TYPE_TARGET)
    place1 = RDK.Item("Place1", robolink.ITEM_TYPE_TARGET)
    bajaprensa1 = RDK.Item("BajaPrensa1", robolink.ITEM_TYPE_TARGET)

    # mid bending
    abreprensa1 = RDK.Item("AbrePrensa1", robolink.ITEM_TYPE_TARGET)
    retract1 = RDK.Item("Retract1", robolink.ITEM_TYPE_TARGET)
    gir180 = RDK.Item("Gir180", robolink.ITEM_TYPE_TARGET)

    place2 = RDK.Item("Place2", robolink.ITEM_TYPE_TARGET)
    bajaprensa2 = RDK.Item("BajaPrensa2", robolink.ITEM_TYPE_TARGET)

    abreprensa2 = RDK.Item("AbrePrensa2", robolink.ITEM_TYPE_TARGET)
    retract2 = RDK.Item("Retract2", robolink.ITEM_TYPE_TARGET)
    r.setFrame(sistRefBend)
    r.setTool(toolR)

    r.MoveL(home)
    r.MoveL(place1)
    r.MoveL(bajaprensa1)
    r.Pause(2000)

    bend1 = RDK.Item(bend_1, robolink.ITEM_TYPE_TARGET)
    r.MoveL(bend1)

    nombre1 = _transicion_objeto(obj_0, obj_1, sistRefBend, toolR)

    r.MoveL(abreprensa1)
    r.MoveL(retract1)
    r.Pause(2000)
    r.MoveJ(gir180)
    r.MoveJ(place2)
    r.MoveL(bajaprensa2)
    r.Pause(2000)

    bend2 = RDK.Item(bend_2, robolink.ITEM_TYPE_TARGET)
    r.MoveL(bend2)

    _transicion_objeto(nombre1, obj_2, sistRefBend, toolR)

    r.MoveL(abreprensa2)
    r.MoveL(retract2)

    sim.setDO("BendingHecho", 1)

def bending_plancha_larga(obj_name : str):
    """Ejecuta el prensado de la plancha larga con los targets adecuados.

    Nota: los objetos planchaLarga1 y planchaLarga2 no son consistentes en la
    estación, por lo que se deberán sustituir por objetos plantilla.
    """

    _bending_generico("Bend1", "Bend2", obj_name, variables.plantilla["larga1"], variables.plantilla["larga2"])

def bending_plancha_ancha(obj_name : str):
    """Ejecuta el prensado de la plancha ancha con los targets adecuados.

    Nota: también falta sustituir los dos últimos parámetros por plantillas.
    """

    _bending_generico("BendA1", "BendA2", obj_name, variables.plantilla["ancha1"], variables.plantilla["ancha2"])
