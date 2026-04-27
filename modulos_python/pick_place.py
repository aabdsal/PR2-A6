from robodk import robolink
from robodk import robomath
from modulos_python import simulation, var, giro

#  = pose local, posicion y orientacion respecto al frame de referencia
# .PoseAbs() = pose global, posicion y orientacion respecto al mundo, es decir, la estacion

def _pick_plancha(prepick_str, pick_str : str):
    
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

    var.objetos_tcp[var.tool_yaskawa] = simulation.adjuntar_objeto(toolR)
    
    r.Pause(1000)
    r.MoveL(prepick)

    r.Pause(1000)

def pick_plancha_larga():
    _pick_plancha("PrePickLargo", "PickLargo")

def pick_plancha_ancha():
    _pick_plancha("PrePickAncho", "PickAncho")
    
def place_cinta_main():
    
    simulation.waitDI("BendingHecho", 1)
    simulation.setDO("BendingHecho", 0)

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

    simulation.soltar_objeto(var.tool_yaskawa, sistRefCinta)
    
    r.MoveL(preplace)   
    robomath.pause(0.5)

    sistRefBending = RDK.Item(var.frame_bending, robolink.ITEM_TYPE_FRAME)
    r.setFrame(sistRefBending)

    home = RDK.Item("Home", robolink.ITEM_TYPE_TARGET)
    r.MoveJ(home)
    
    simulation.setDO("enCintaMain", 1)

# programa de roboDK plancha en mesa
def place_plancha_mesa():

    simulation.waitDI("SensorCC", 1)   
    RDK = robolink.Robolink()
    
    r = RDK.Item(var.robot_abb_p, robolink.ITEM_TYPE_ROBOT)
    sistRefMesa = RDK.Item(var.frame_paletizado_mesa, robolink.ITEM_TYPE_FRAME)
    toolR = RDK.Item(var.tool_abb_p, robolink.ITEM_TYPE_TOOL)

    if not r.Valid() :
        raise RuntimeError("El nombre del robot no existe, revisa nombres")
    
    if not sistRefMesa.Valid() :
        raise RuntimeError("El nombre del frame no existe, revisa nombres")
    
    if not toolR.Valid() :
        raise RuntimeError("El nombre de la herramienta no existe, revisa nombres")
    
    r.setFrame(sistRefMesa)
    r.setTool(toolR)

    ini = RDK.Item("Inicio", robolink.ITEM_TYPE_TARGET)
    prepick_cinta = RDK.Item("PrePickMain", robolink.ITEM_TYPE_TARGET)

    giro180 = RDK.Item("Giro180_P", robolink.ITEM_TYPE_TARGET)
    pick_larga = RDK.Item("PickMainLarga", robolink.ITEM_TYPE_TARGET)
    pick_ancha = RDK.Item("PickMainAncha", robolink.ITEM_TYPE_TARGET)
    post_pick = RDK.Item("PostPick", robolink.ITEM_TYPE_TARGET)
    preplace_main = RDK.Item("PrePlaceMain", robolink.ITEM_TYPE_TARGET)
    place_main = RDK.Item("PlaceMain", robolink.ITEM_TYPE_TARGET)

    r.MoveJ(ini)
    r.MoveL(prepick_cinta)
    robomath.pause(0.5)

    elem = var.alternancia.get()
    
    if elem == "larga":
        r.MoveL(pick_larga)
    elif elem == "ancha":
        r.MoveL(pick_ancha)
    
    robomath.pause(0.5)
    var.objetos_tcp[var.tool_abb_p] = simulation.adjuntar_objeto(toolR)
    
    r.MoveL(prepick_cinta)
    robomath.pause(0.5)
    r.MoveL(post_pick)
    robomath.pause(0.5)
    r.MoveJ(giro180)
    robomath.pause(0.5)
    r.MoveJ(preplace_main)
    robomath.pause(0.5)
    r.MoveL(place_main)

    simulation.setDO("EnMesa", 1)

    if elem == "ancha":
        simulation.setDO("LasDos", 1)
    
    robomath.pause(0.5)
    
    simulation.soltar_objeto(var.tool_abb_p, sistRefMesa)
    
    if elem == "larga":
        giro.giro_mesa()
    
    r.MoveL(preplace_main)

    r.MoveJ(ini)
    robomath.pause(0.5)

# programa de roboDK place plancha soldada
def place_cuadro_acabada():
    
    simulation.waitDI("tapaPuesta", 1)
    simulation.setDO("tapaPuesta", 0)

    RDK = robolink.Robolink()

    r = RDK.Item(var.robot_abb_p, robolink.ITEM_TYPE_ROBOT)
    sistRefMesa = RDK.Item(var.frame_cinta_etiqueta, robolink.ITEM_TYPE_FRAME)
    toolR = RDK.Item(var.tool_abb_p, robolink.ITEM_TYPE_TOOL)
    
    if not r.Valid() :
        raise RuntimeError("El nombre del robot no existe, revisa nombres")
    
    if not sistRefMesa.Valid() :
        raise RuntimeError("El nombre del frame no existe, revisa nombres")
    
    if not toolR.Valid() :
        raise RuntimeError("El nombre de la herramienta no existe, revisa nombres")
    
    r.setFrame(sistRefMesa)
    r.setTool(toolR)
    
    prepick_cuadro = RDK.Item("PrePickCuadro", robolink.ITEM_TYPE_TARGET)
    pick_cuadro = RDK.Item("PickCuadro", robolink.ITEM_TYPE_TARGET)
    preplace_cuadro = RDK.Item("PrePlaceCuadro", robolink.ITEM_TYPE_TARGET)
    place_cuadro = RDK.Item("PlaceCuadro", robolink.ITEM_TYPE_TARGET)
    ini = RDK.Item("Inicio", robolink.ITEM_TYPE_TARGET)

    r.MoveJ(prepick_cuadro)
    robomath.pause(0.5)
    r.MoveL(pick_cuadro)
    var.objetos_tcp[var.tool_abb_p] = simulation.adjuntar_objeto(toolR)
    robomath.pause(0.5)
    r.MoveJ(prepick_cuadro)
    robomath.pause(0.5)
    r.MoveJ(preplace_cuadro)
    robomath.pause(0.5)
    r.MoveL(place_cuadro)
    simulation.soltar_objeto(var.tool_abb_p, sistRefMesa)
    robomath.pause(0.5)
    r.MoveJ(preplace_cuadro)
    simulation.setDO("EnCinta", 1)
    r.MoveJ(ini)
    
def place_tapa_en_mesa():
   
    simulation.waitDI("planchaSoldada", 1)
    simulation.setDO("planchaSoldada", 0)

    RDK = robolink.Robolink()

    r = RDK.Item(var.robot_abb_p, robolink.ITEM_TYPE_ROBOT)
    sistRefMesa = RDK.Item(var.frame_paletizado, robolink.ITEM_TYPE_FRAME)
    toolR = RDK.Item(var.tool_abb_p, robolink.ITEM_TYPE_TOOL)
    
    if not r.Valid() :
        raise RuntimeError("El nombre del robot no existe, revisa nombres")
    
    if not sistRefMesa.Valid() :
        raise RuntimeError("El nombre del frame no existe, revisa nombres")
    
    if not toolR.Valid() :
        raise RuntimeError("El nombre de la herramienta no existe, revisa nombres")
    
    r.setFrame(sistRefMesa)
    r.setTool(toolR)
    
    prepick_tapa = RDK.Item("PrePicktapa", robolink.ITEM_TYPE_TARGET)
    pick_tapa = RDK.Item("Picktapa", robolink.ITEM_TYPE_TARGET)
    preplace_tapa = RDK.Item("PrePlacetapa", robolink.ITEM_TYPE_TARGET)
    place_tapa = RDK.Item("Placetapa", robolink.ITEM_TYPE_TARGET)
    ini = RDK.Item("Inicio", robolink.ITEM_TYPE_TARGET)

    r.MoveJ(prepick_tapa)
    robomath.pause(0.5)
    r.MoveL(pick_tapa)
    var.objetos_tcp[var.tool_abb_p] = simulation.adjuntar_objeto(toolR)
    robomath.pause(0.5)
    r.MoveJ(prepick_tapa)
    robomath.pause(0.5)
    r.MoveJ(preplace_tapa)
    robomath.pause(0.5)
    r.MoveL(place_tapa)
    simulation.soltar_objeto(var.tool_abb_p, sistRefMesa)
    robomath.pause(0.5)
    r.MoveJ(preplace_tapa)

    simulation.setDO("tapaPuesta", 1)
    r.MoveJ(ini)
    