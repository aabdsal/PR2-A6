from robodk import robolink
from modulos_python import simulation, var, giro

#  = pose local, posicion y orientacion respecto al frame de referencia
# .PoseAbs() = pose global, posicion y orientacion respecto al mundo, es decir, la estacion

def place_cinta_main():
    
    simulation.waitDI("BendingHecho", 1)
    simulation.setDO("BendingHecho", 0)

    RDK = robolink.Robolink()

    tool_yaskawa = "EPick Bend"
    r = RDK.Item("Yaskawa MH24", robolink.ITEM_TYPE_ROBOT)
    sistRefPlace = RDK.Item("Place", robolink.ITEM_TYPE_FRAME)
    sistRefCinta = RDK.Item("PlanchaCuadro", robolink.ITEM_TYPE_FRAME)
    toolR = RDK.Item(tool_yaskawa, robolink.ITEM_TYPE_TOOL)

    r.setFrame(sistRefPlace)
    r.setTool(toolR)

    preplace = RDK.Item("PrePlace", robolink.ITEM_TYPE_TARGET)
    place = RDK.Item("Place", robolink.ITEM_TYPE_TARGET)
    
    r.MoveJ(preplace)
    r.Pause(1000)
    r.MoveL(place)

    simulation.soltar_objeto(tool_yaskawa, sistRefCinta)
    
    r.MoveL(preplace)   
    r.Pause(1000)

    sistRefBending = RDK.Item("Bending", robolink.ITEM_TYPE_FRAME)
    r.setFrame(sistRefBending)
    home = RDK.Item("Home", robolink.ITEM_TYPE_TARGET)
    r.MoveJ(home)
    
    simulation.setDO("enCintaMain", 1)

# programa de roboDK plancha en mesa
"""
    cambiar el tipo de movimientos que hacia antes usando el aux
    mediante la cola de consumidores, productores
"""
def place_plancha_mesa():

    simulation.waitDI("SensorCC", 1)   
    RDK = robolink.Robolink()
    
    tool_paletizado = "EPick Gripper"
    r = RDK.Item("ABB IRB 1660-4/1.55 (paletizado)", robolink.ITEM_TYPE_ROBOT)
    sistRefMesa = RDK.Item("DesplazP1", robolink.ITEM_TYPE_FRAME)
    toolR = RDK.Item(tool_paletizado, robolink.ITEM_TYPE_TOOL)

    r.setFrame(sistRefMesa)
    r.setTool(toolR)

    ini = RDK.Item("Inicio", robolink.ITEM_TYPE_TARGET)
    prepick_cinta = RDK.Item("PrePickCinta", robolink.ITEM_TYPE_TARGET)

    pregiro = RDK.Item("PreGiro", robolink.ITEM_TYPE_TARGET)
    acomodado1 = RDK.Item("Acomodado1", robolink.ITEM_TYPE_TARGET)
    acomodado2 = RDK.Item("Acomodado2", robolink.ITEM_TYPE_TARGET)
    pick_cinta = RDK.Item("PickCinta", robolink.ITEM_TYPE_TARGET)
    pick_cinta2 = RDK.Item("PickCinta2", robolink.ITEM_TYPE_TARGET)
    preplace_larga = RDK.Item("PrePlaceLarga", robolink.ITEM_TYPE_TARGET)
    preplace_ancha = RDK.Item("PrePlaceAncha", robolink.ITEM_TYPE_TARGET)
    place_larga = RDK.Item("PlaceLarga", robolink.ITEM_TYPE_TARGET)
    place_ancha = RDK.Item("PlaceAncha", robolink.ITEM_TYPE_TARGET)

    r.MoveJ(ini)
    r.MoveJ(prepick_cinta)

    if var.aux == 0:
        r.MoveL(pick_cinta)
        r.Pause(2000)

        var.objetos_tcp[tool_paletizado] = simulation.adjuntar_objeto(toolR)
        
        r.MoveJ(prepick_cinta)
        r.MoveJ(preplace_larga)
        
        r.MoveJ(place_larga)

        simulation.setDO("EnMesa", 1)
        r.Pause(2000)
        
        simulation.soltar_objeto(tool_paletizado, sistRefMesa)
        
        giro.giro_mesa()
        r.MoveL(preplace_larga)
    
    elif var.aux == 1:
        r.Pause(2000)
        r.MoveJ(pick_cinta2)

        var.objetos_tcp[tool_paletizado] = simulation.adjuntar_objeto(toolR)
        r.Pause(2000)
        
        r.MoveJ(prepick_cinta)
        r.Pause(2000)
        
        r.MoveL(pregiro)
        r.MoveJ(acomodado1) 
        r.MoveJ(acomodado2)
        
        r.MoveL(preplace_ancha)
        r.Pause(2000)
        r.MoveL(place_ancha)
        r.Pause(2000)
        
        simulation.soltar_objeto(tool_paletizado, sistRefMesa)
        simulation.setDO("EnMesa", 1)
        simulation.setDO("LasDos", 1)
        
        r.MoveL(preplace_ancha)

    
    r.MoveJ(ini)
    r.Pause(2000)

# programa de roboDK place plancha soldada
def place_plancha_soldada():
    
    simulation.waitDI("planchaSoldada", 1)
    simulation.setDO("planchaSoldada", 0)

    RDK = robolink.Robolink()
    tool_paletizado = "EPick Gripper"
    r = RDK.Item("ABB IRB 1660-4/1.55 (paletizado)", robolink.ITEM_TYPE_ROBOT)
    sistRefMesa = RDK.Item("RobotPaletizado", robolink.ITEM_TYPE_FRAME)
    toolR = RDK.Item(tool_paletizado, robolink.ITEM_TYPE_TOOL)
    
    r.setFrame(sistRefMesa)
    r.setTool(toolR)
    
    prepick_cuadro = RDK.Item("PrePickCuadro", robolink.ITEM_TYPE_TARGET)
    pick_cuadro = RDK.Item("PickCuadro", robolink.ITEM_TYPE_TARGET)
    preplace_cuadro = RDK.Item("PrePlaceCuadro", robolink.ITEM_TYPE_TARGET)
    place_cuadro = RDK.Item("PlaceCuadro", robolink.ITEM_TYPE_TARGET)
    ini = RDK.Item("Inicio", robolink.ITEM_TYPE_TARGET)

    r.MoveJ(prepick_cuadro)
    r.Pause(1000)
    r.MoveL(pick_cuadro)
    var.objetos_tcp[tool_paletizado] = simulation.adjuntar_objeto(toolR)
    r.Pause(1000)
    r.MoveJ(prepick_cuadro)
    r.Pause(1000)
    r.MoveJ(preplace_cuadro)
    r.Pause(1000)
    r.MoveL(place_cuadro)
    simulation.soltar_objeto(tool_paletizado, sistRefMesa)
    r.Pause(2000)
    r.MoveJ(preplace_cuadro)
    simulation.setDO("EnCinta", 1)
    r.MoveJ(ini)
    
    