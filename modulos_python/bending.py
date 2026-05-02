"""Este módulo de python implementa los movimientos necesarios 
tanto para hacer el prensado las planchas largas como anchas.

Es posible gracias a la API de RoboDK, el uso de variables 
globales y simulaciones que representen acciones reales."""

from robodk import robolink   
from modulos_python import variables
from modulos_python import simulation

def _transicion_objeto(obj_from_plantilla, obj_to_plantilla: str, frame, tool: robolink.Item):
    """Esta función hace un intercambio entre el objeto 
    que tiene el Yaskawa MH24 y el siguiente objeto que debe adjuntar.

    Además, para poder tener una cantidad infinita (o las que pida el usuario) de objetos 
    se hace un duplicado del objeto que tiene que adjuntar el Yaskawa y se elimina el anterior, 
    para no crear basura durante el proceso. Se hace uso de objetos plantilla definidos en variables.py
    que estan en la posición absoluta del objeto que el robot va a adjuntar.

    La parte de duplicado aún no es definitiva, por eso está comentada."""
    
    RDK = robolink.Robolink()

    simulation.soltar_objeto(variables.tool_yaskawa, frame)

    obj_from = RDK.Item(obj_from_plantilla)
    if not obj_from.Valid():
        raise RuntimeError("objeto no existe, revisa nombres")
    
    obj_to = RDK.Item(obj_to_plantilla)
    if not obj_to.Valid():
        raise RuntimeError("objeto no existe, revisa nombres")
    
    simulation.ocultar_objeto(obj_from.Name())
    simulation.mostrar_objeto(obj_to.Name())
    #obj_from.Delete() # ¡Importante! Elimina el objeto viejo.

    #nuevo_objeto = simulation.duplicar_objeto(obj_to_plantilla, frame.Name())

    variables.objetos_tcp[variables.tool_yaskawa] = simulation.adjuntar_objeto(tool, obj_to_plantilla)
    
    #return nuevo_objeto.Name()

def _bending_generico(bend_1: str, bend_2: str, obj_0: str, obj_1: str, obj_2: str):
    """Este método realiza los movimientos del Yaskawa MH24 
    y el intercambio de objetos necesarios. 

    Primero que todo, se establece la conexión con la estación de 
    forma local mediante el robolink.Robolink() para evitar 
    problemas con los hilos y se guardan todos los targets, 
    frame, robot y tcp que se van a usar durante el movimiento.

    Finalmente, una vez finalizado el bending, se establece una 
    salida digital para proceder al place del objeto prensado a la cinta."""

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

    #nombre1 = 
    _transicion_objeto(obj_0, obj_1, sistRefBend, toolR)

    r.MoveL(abreprensa1)
    r.MoveL(retract1)
    r.Pause(2000)
    r.MoveJ(gir180)
    r.MoveJ(place2)
    r.MoveL(bajaprensa2)
    r.Pause(2000)

    bend2 = RDK.Item(bend_2, robolink.ITEM_TYPE_TARGET)
    r.MoveL(bend2)

    _transicion_objeto(obj_1, obj_2, sistRefBend, toolR)

    r.MoveL(abreprensa2)
    r.MoveL(retract2)

    simulation.setDO("BendingHecho", 1)

def bending_plancha_larga(obj_name : str):
    """Este método para por parámetro las targets 
    y objetos para hacer un prensado de la plancha larga.
    
    Falta sustituir los dos últimos parámetros por objetos plantilla, 
    ya que planchaLarga1 y planchaLarga2 no son consistentes en la 
    estación y se van moviendo provocando que no sea útil hacer una duplicación de ellas"""

    _bending_generico("Bend1", "Bend2", obj_name, "planchaLarga1", "planchaLarga2")

def bending_plancha_ancha(obj_name : str):
    """Este método hace lo mismo que el de arriba pero para 
    la plancha ancha, y tambien falta sustituir los dos últimos parametros"""

    _bending_generico("BendA1", "BendA2", obj_name, "planchaAncha1", "planchaAncha2")
