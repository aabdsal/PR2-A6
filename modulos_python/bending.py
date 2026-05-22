"""Este módulo implementa los movimientos necesarios
para el prensado de planchas largas y anchas.

Se apoya en la API de RoboDK, variables globales 
y simulaciones que representan acciones reales."""

from robodk import robolink, robomath   
from modulos_python import variables as var, simulation as sim

def _transicion_objeto(obj_from_plantilla, obj_to_plantilla: str, frame, tool: robolink.Item):
    """Intercambia el objeto que tiene el Yaskawa MH24 por el siguiente.

    Se apoya en objetos plantilla definidos en variables.py, ubicados en la
    posición absoluta donde el robot debe recogerlos. La lógica de duplicado
    y limpieza de objetos está pendiente y se mantiene comentada."""
    
    RDK = robolink.Robolink()

    sim.soltar_objeto(var.tool_yaskawa, frame)

    obj_from = RDK.Item(obj_from_plantilla)
    if not obj_from.Valid():
        raise RuntimeError("objeto no existe, revisa nombres")
    
    obj_to = RDK.Item(obj_to_plantilla)
    if not obj_to.Valid():
        raise RuntimeError("objeto no existe, revisa nombres")
    
    RDK.Render(False)
    sim.ocultar_objeto(obj_from.Name())
    obj_from.Delete()

    nuevo_objeto = sim.duplicar_objeto(obj_to_plantilla, frame.Name())
    RDK.Render(True)
    
    sim.adjuntar_objeto(tool, nuevo_objeto.Name())
    
    return nuevo_objeto.Name()

def _bending_generico(bend_1: str, bend_2: str, obj_0: str, obj_1: str, obj_2: str):
    """Ejecuta la secuencia de movimientos del Yaskawa MH24.

    Configura los items necesarios (robot, frame, herramienta y targets),
    realiza el intercambio de objetos y, al finalizar, activa la salida
    digital para permitir el place en la cinta."""

    RDK = robolink.Robolink()

    r = RDK.Item(var.robot_yaskawa, robolink.ITEM_TYPE_ROBOT)
    sistRefBend = RDK.Item("Bending", robolink.ITEM_TYPE_FRAME)
    toolR = RDK.Item(var.tool_yaskawa, robolink.ITEM_TYPE_TOOL)

    # principio
    home = RDK.Item("Home", robolink.ITEM_TYPE_TARGET)
    preplace1 = RDK.Item("PrePlace1", robolink.ITEM_TYPE_TARGET)
    place1 = RDK.Item("Place1", robolink.ITEM_TYPE_TARGET)
    bajaprensa1 = RDK.Item("BajaPrensa1", robolink.ITEM_TYPE_TARGET)

    # mid bending
    abreprensa1 = RDK.Item("AbrePrensa1", robolink.ITEM_TYPE_TARGET)
    preretract1 = RDK.Item("PreRetract1", robolink.ITEM_TYPE_TARGET)
    retract1 = RDK.Item("Retract1", robolink.ITEM_TYPE_TARGET)
    gir180 = RDK.Item("Gir180", robolink.ITEM_TYPE_TARGET)

    preplace2 = RDK.Item("PrePlace2", robolink.ITEM_TYPE_TARGET)
    place2 = RDK.Item("Place2", robolink.ITEM_TYPE_TARGET)
    bajaprensa2 = RDK.Item("BajaPrensa2", robolink.ITEM_TYPE_TARGET)

    abreprensa2 = RDK.Item("AbrePrensa2", robolink.ITEM_TYPE_TARGET)
    preretract2 = RDK.Item("PreRetract2", robolink.ITEM_TYPE_TARGET)
    retract2 = RDK.Item("Retract2", robolink.ITEM_TYPE_TARGET)
    r.setFrame(sistRefBend)
    r.setTool(toolR)

    r.MoveL(home)
    robomath.pause(0.5)
    r.MoveL(preplace1)
    robomath.pause(0.5)
    r.MoveL(place1)
    robomath.pause(0.5)
    r.MoveL(bajaprensa1)
    robomath.pause(0.5)

    bend1 = RDK.Item(bend_1, robolink.ITEM_TYPE_TARGET)
    r.MoveL(bend1)

    nombre1 = _transicion_objeto(obj_0, obj_1, sistRefBend, toolR)

    r.MoveL(abreprensa1)
    robomath.pause(0.5)
    r.MoveL(preretract1)
    robomath.pause(0.5)
    r.MoveL(retract1)
    robomath.pause(0.5)
    r.MoveJ(gir180)
    robomath.pause(0.5)

    r.MoveJ(preplace2)
    robomath.pause(0.5)
    r.MoveJ(place2)
    robomath.pause(0.5)
    r.MoveL(bajaprensa2)
    robomath.pause(0.5)

    bend2 = RDK.Item(bend_2, robolink.ITEM_TYPE_TARGET)
    r.MoveL(bend2)

    _transicion_objeto(nombre1, obj_2, sistRefBend, toolR)

    r.MoveL(abreprensa2)
    robomath.pause(0.5)
    r.MoveL(preretract2)
    robomath.pause(0.5)
    r.MoveL(retract2)
    robomath.pause(0.5)

    sim.setDO("BendingHecho", 1)

def bending_plancha_larga(obj_name : str):
    """Ejecuta el prensado de la plancha larga con los targets adecuados."""

    _bending_generico("BendLarga1", "BendLarga2", obj_name, var.plantilla["larga1"], var.plantilla["larga2"])

def bending_plancha_ancha(obj_name : str):
    """Ejecuta el prensado de la plancha ancha con los targets adecuados."""

    _bending_generico("BendAncha1", "BendAncha2", obj_name, var.plantilla["ancha1"], var.plantilla["ancha2"])
