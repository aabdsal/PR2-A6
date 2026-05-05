"""Este módulo es el que implementa todos los movimientos de los robots que se usan en la estación."""

from robodk import robolink
from robodk import robomath
from modulos_python import variables as var
from modulos_python import simulation as sim
from modulos_python import giro

#  = pose local, posicion y orientacion respecto al frame de referencia
# .PoseAbs() = pose global, posicion y orientacion respecto al mundo, es decir, la estacion

def _pick_plancha(prepick_str, pick_str, obj_name : str):
    """Hace el pick desde las cintas iniciales para plancha larga o ancha."""

    RDK = robolink.Robolink()
    
    sistRefBending = RDK.Item(var.frame_bending, robolink.ITEM_TYPE_FRAME)
    sistRefPick = RDK.Item(var.frame_pick, robolink.ITEM_TYPE_FRAME)
    r = RDK.Item("Yaskawa MH24 Prensado", robolink.ITEM_TYPE_ROBOT)

    toolR = RDK.Item(var.tool_yaskawa, robolink.ITEM_TYPE_TOOL)
    
    r.setFrame(sistRefBending)
    r.setTool(toolR)
    
    home = RDK.Item("Home", robolink.ITEM_TYPE_TARGET)
    r.MoveJ(home)
    r.setFrame(sistRefPick)

    prepick = RDK.Item(prepick_str, robolink.ITEM_TYPE_TARGET)
    pick = RDK.Item(pick_str, robolink.ITEM_TYPE_TARGET)

    r.MoveL(prepick)
    r.Pause(1000)
    r.MoveL(pick)

    sim.adjuntar_objeto(toolR, obj_name)
    
    r.Pause(1000)
    r.MoveL(prepick)

    r.Pause(1000)

def pick_plancha_larga(obj_name : str):
    """Ejecuta el pick de una plancha larga usando los targets correctos."""

    _pick_plancha("PrePickLargo", "PickLargo", obj_name)

def pick_plancha_ancha(obj_name : str):
    """Ejecuta el pick de una plancha ancha usando los targets correctos."""

    _pick_plancha("PrePickAncho", "PickAncho", obj_name)
    
def place_cinta_main():
    """Lleva la plancha prensada a la cinta principal y notifica el estado.

    Se activa cuando el prensado termina y envía una salida digital
    indicando que la pieza ya está lista para avanzar."""
    
    sim.waitDI("BendingHecho", 1)
    sim.setDO("BendingHecho", 0)

    RDK = robolink.Robolink()

    r = RDK.Item(var.robot_yaskawa, robolink.ITEM_TYPE_ROBOT)
    sistRefPlace = RDK.Item(var.frame_place, robolink.ITEM_TYPE_FRAME)
    sistRefCinta = RDK.Item(var.frame_cinta_main, robolink.ITEM_TYPE_FRAME)
    toolR = RDK.Item(var.tool_yaskawa, robolink.ITEM_TYPE_TOOL)

    if not r.Valid() :
        raise RuntimeError("El nombre del robot no existe, revisa nombres")
    
    if not sistRefPlace.Valid() :
        raise RuntimeError("El nombre del frame  place no existe, revisa nombres")
    
    if not sistRefCinta.Valid() :
        raise RuntimeError("El nombre del frame cinta no existe, revisa nombres")
    
    if not toolR.Valid() :
        raise RuntimeError("El nombre de la herramienta no existe, revisa nombres")
    
    r.setFrame(sistRefPlace)
    r.setTool(toolR)

    preplace = RDK.Item("PrePlace", robolink.ITEM_TYPE_TARGET)
    place = RDK.Item("Place", robolink.ITEM_TYPE_TARGET)
    
    r.MoveJ(preplace)
    robomath.pause(0.5)
    r.MoveL(place)

    sim.soltar_objeto(var.tool_yaskawa, sistRefCinta)
    
    r.MoveL(preplace)   
    robomath.pause(0.5)

    sistRefBending = RDK.Item(var.frame_bending, robolink.ITEM_TYPE_FRAME)
    r.setFrame(sistRefBending)

    home = RDK.Item("Home", robolink.ITEM_TYPE_TARGET)
    r.MoveJ(home)
    
    sim.setDO("enCintaMain", 1)

def place_plancha_mesa():
    """Hace un pick and place desde la cinta principal a la mesa giratoria.

    También comunica si ya hay una plancha en la mesa o si ya están las dos
    para pasar a la siguiente fase."""

    #sim.waitDI("SensorCC", 1)   
    RDK = robolink.Robolink()
    
    r = RDK.Item(var.robot_abb_p, robolink.ITEM_TYPE_ROBOT)
    frame_cinta = RDK.Item(var.frame_paletizado_cinta_mesa, robolink.ITEM_TYPE_FRAME)
    frame_paletizado = RDK.Item(var.frame_paletizado, robolink.ITEM_TYPE_FRAME)
    frame_mesa = RDK.Item(var.frame_mesa_giratoria, robolink.ITEM_TYPE_FRAME)
    toolR = RDK.Item(var.tool_abb_p, robolink.ITEM_TYPE_TOOL)

    if not r.Valid() :
        raise RuntimeError("El nombre del robot no existe, revisa nombres")
    
    if not frame_paletizado.Valid() :
        raise RuntimeError("El nombre del frame no existe, revisa nombres")
    
    if not toolR.Valid() :
        raise RuntimeError("El nombre de la herramienta no existe, revisa nombres")
    
    ini = RDK.Item("Inicio", robolink.ITEM_TYPE_TARGET)
    prepick_cinta = RDK.Item("PrePickMain", robolink.ITEM_TYPE_TARGET)

    giro180 = RDK.Item("Giro180_P", robolink.ITEM_TYPE_TARGET)
    pick_larga = RDK.Item("PickMainLarga", robolink.ITEM_TYPE_TARGET)
    pick_ancha = RDK.Item("PickMainAncha", robolink.ITEM_TYPE_TARGET)
    post_pick = RDK.Item("PostPick", robolink.ITEM_TYPE_TARGET)
    preplace_main = RDK.Item("PrePlaceMain", robolink.ITEM_TYPE_TARGET)
    place_main = RDK.Item("PlaceMain", robolink.ITEM_TYPE_TARGET)

    objeto_cola_main = var.objetos_pendientes["SensorCC"].get()

    r.setFrame(frame_paletizado)
    r.setTool(toolR)
    RDK.ShowMessage("antes de moverse a ini", False)
    r.MoveJ(ini)

    r.setFrame(frame_cinta)
    RDK.ShowMessage("antes de moverse a prepick cinta", False)
    r.MoveL(prepick_cinta)
    robomath.pause(0.5)
    elem = var.alternancia.get()
    
    if elem == "larga":
        r.MoveL(pick_larga)
    elif elem == "ancha":
        r.MoveL(pick_ancha)
    
    count = 0
    robomath.pause(0.5)
    sim.adjuntar_objeto(toolR, objeto_cola_main)
    
    r.MoveL(prepick_cinta)
    robomath.pause(0.5)
    r.MoveL(post_pick)
    robomath.pause(0.5)
    r.MoveJ(giro180)
    robomath.pause(0.5)
    r.MoveJ(preplace_main)
    robomath.pause(0.5)
    r.MoveL(place_main)

    sim.setDO("EnMesa", 1)

    if count == 1:
        sim.setDO("LasDos", 1)
        count = 0
    
    robomath.pause(0.5)
    
    sim.soltar_objeto(var.tool_abb_p, frame_mesa)
    
    r.MoveL(preplace_main)

    if count == 0:
        giro.giro_mesa()
        count = 1

    r.MoveJ(ini)
    robomath.pause(0.5)
    
def place_tapa_en_mesa():
    """Coloca la tapa sobre el cuadro ya soldado y notifica el estado."""

    sim.waitDI("planchaSoldada", 1)
    sim.setDO("planchaSoldada", 0)

    RDK = robolink.Robolink()

    r = RDK.Item(var.robot_abb_p, robolink.ITEM_TYPE_ROBOT)
    sistRefMesa = RDK.Item(var.frame_paletizado, robolink.ITEM_TYPE_FRAME)
    toolR = RDK.Item(var.tool_abb_p, robolink.ITEM_TYPE_TOOL)
    
    if not r.Valid():
        raise RuntimeError("El nombre del robot no existe, revisa nombres")
    
    if not sistRefMesa.Valid() :
        raise RuntimeError("El nombre del frame no existe, revisa nombres")
    
    if not toolR.Valid():
        raise RuntimeError("El nombre de la herramienta no existe, revisa nombres")
    
    r.setFrame(sistRefMesa)
    r.setTool(toolR)
    
    prepick_tapa = RDK.Item("PrePickTapa", robolink.ITEM_TYPE_TARGET)
    pick_tapa = RDK.Item("PickTapa", robolink.ITEM_TYPE_TARGET)
    preplace_tapa = RDK.Item("PrePickCuadro", robolink.ITEM_TYPE_TARGET)
    place_tapa = RDK.Item("PickCuadro", robolink.ITEM_TYPE_TARGET)
    ini = RDK.Item("Inicio", robolink.ITEM_TYPE_TARGET)

    objeto_tapa = var.objetos_pendientes["SensorTapa"].get()

    r.MoveJ(prepick_tapa)
    robomath.pause(0.5)
    r.MoveL(pick_tapa)

    sim.adjuntar_objeto(toolR, objeto_tapa)
    
    robomath.pause(0.5)
    r.MoveJ(prepick_tapa)
    robomath.pause(0.5)
    r.MoveJ(preplace_tapa)
    robomath.pause(0.5)
    r.MoveL(place_tapa)

    sim.soltar_objeto(var.tool_abb_p, sistRefMesa)
    
    robomath.pause(0.5)
    r.MoveJ(preplace_tapa)

    item_objeto_tapa = RDK.Item(objeto_tapa, robolink.ITEM_TYPE_OBJECT)

    objecto_soldada = var.cola_soldadas.get()
    item_soldada = RDK.Item(objecto_soldada, robolink.ITEM_TYPE_OBJECT)

    item_objeto_tapa.Delete()
    item_soldada.Delete()

    nuevo_objeto = sim.duplicar_objeto(var.plantilla["cuadroConTapa"], var.frame_mesa_giratoria)

    var.cola_cuadrosTapa.put(nuevo_objeto.Name())

    sim.setDO("tapaPuesta", 1)
    r.MoveJ(ini)

def place_cuadro_acabada():
    """Devuelve el cuadro con tapa a la cinta de etiquetado.

    Espera a la señal de tapa puesta y notifica cuando el cuadro está en la cinta."""

    sim.waitDI("tapaPuesta", 1)
    sim.setDO("tapaPuesta", 0)

    RDK = robolink.Robolink()

    r = RDK.Item(var.robot_abb_p, robolink.ITEM_TYPE_ROBOT)
    
    frame_mesa = RDK.Item(var.frame_paletizado, robolink.ITEM_TYPE_FRAME)
    frame_cinta = RDK.Item(var.frame_cinta_etiqueta, robolink.ITEM_TYPE_FRAME)

    toolR = RDK.Item(var.tool_abb_p, robolink.ITEM_TYPE_TOOL)
    
    if not r.Valid() :
        raise RuntimeError("El nombre del robot no existe, revisa nombres")
    
    if not frame_mesa.Valid() :
        raise RuntimeError("El nombre del frame mesa no existe, revisa nombres")
    
    if not frame_cinta.Valid() :
        raise RuntimeError("El nombre del frame cinta etiquta no existe, revisa nombres")
    
    if not toolR.Valid() :
        raise RuntimeError("El nombre de la herramienta no existe, revisa nombres")
    
    r.setFrame(frame_mesa)
    r.setTool(toolR)
    
    prepick_cuadro = RDK.Item("PrePickCuadro", robolink.ITEM_TYPE_TARGET)
    pick_cuadro = RDK.Item("PickCuadro", robolink.ITEM_TYPE_TARGET)
    preplace_cuadro = RDK.Item("PrePlaceCuadro", robolink.ITEM_TYPE_TARGET)
    place_cuadro = RDK.Item("PlaceCuadro", robolink.ITEM_TYPE_TARGET)
    ini = RDK.Item("Inicio", robolink.ITEM_TYPE_TARGET)

    r.MoveJ(prepick_cuadro)
    robomath.pause(0.5)
    r.MoveL(pick_cuadro)
    
    sim.adjuntar_objeto(toolR, var.cola_cuadrosTapa.get())
    
    robomath.pause(0.5)
    r.MoveJ(prepick_cuadro)
    robomath.pause(0.5)
    r.MoveJ(preplace_cuadro)
    robomath.pause(0.5)
    r.MoveL(place_cuadro)

    sim.soltar_objeto(var.tool_abb_p, frame_cinta)

    robomath.pause(0.5)
    r.MoveJ(preplace_cuadro)

    sim.setDO("EnCintaEtiquetar", 1)
    
    r.MoveJ(ini)
    