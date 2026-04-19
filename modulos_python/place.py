from robodk import robolink    # RoboDK API
from robodk import robomath    # Robot toolbox
RDK = robolink.Robolink()

import simulation
import var
import giro

def place_cinta_main():
    
    r = RDK.Item("Yaskawa MH24", robolink.ITEM_TYPE_ROBOT)
    sistRefPlace = RDK.Item("Place", robolink.ITEM_TYPE_FRAME)
    toolR = RDK.Item("EPick Bend", robolink.ITEM_TYPE_TOOL)

    r.setFrame(sistRefPlace)
    r.setTool(toolR)

    preplace = RDK.Item("PrePlace", robolink.ITEM_TYPE_TARGET)
    place = RDK.Item("Place", robolink.ITEM_TYPE_TARGET)
    
    r.MoveL(preplace.Pose())
    r.Pause(1000)
    r.MoveL(place.Pose())
    simulation.simulation_soltar_objeto(toolR)
    r.MoveL(preplace.Pose())   
    r.Pause(1000)

    if var.elegir == 1:
        sistRefBending = RDK.Item("Bending", robolink.ITEM_TYPE_FRAME)
        r.setFrame(sistRefBending)
        home = RDK.Item("Home", robolink.ITEM_TYPE_TARGET)
        r.MoveJ(home.Pose())

# programa de roboDK plancha en mesa
def place_plancha_mesa():

    r = RDK.Item("ABB IRB 1660-4/1.55 (paletizado)",robolink.ITEM_TYPE_ROBOT)
    sistRefMesa = RDK.Item("DesplazP1", robolink.ITEM_TYPE_FRAME)
    toolR = RDK.Item("riQ EPick Vacuum Gripper", robolink.ITEM_TYPE_TOOL)

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

    r.MoveJ(ini.Pose())
    r.MoveJ(prepick_cinta.Pose())

    if var.aux == 0:
        r.MoveL(pick_cinta.Pose())
        r.Pause(2000)

        simulation.simulation_adjuntar_objeto(toolR)
        
        r.MoveJ(prepick_cinta.Pose())
        r.MoveJ(preplace_larga.Pose())
        
        r.MoveL(place_larga.Pose()) 
        var.en_mesa = True  
        r.Pause(2000)
        
        simulation.simulation_soltar_objeto(toolR)
        
        giro.giro_mesa()
        r.MoveL(preplace_larga.Pose())
    
    elif var.aux == 1:
        r.Pause(2000)
        r.MoveJ(pick_cinta2.Pose())

        simulation.simulation_adjuntar_objeto(toolR)
        r.Pause(2000)
        
        r.MoveJ(prepick_cinta.Pose())
        r.Pause(2000)
        
        r.MoveL(pregiro.Pose())
        r.MoveJ(acomodado1.Pose()) 
        r.MoveJ(acomodado2.Pose())
        
        r.MoveL(preplace_ancha.Pose())
        r.Pause(2000)
        r.MoveL(place_ancha.Pose())
        r.Pause(2000)
        
        simulation.simulation_soltar_objeto(toolR)
        var.en_mesa = True  
        var.las_dos = True  
        
        r.MoveL(preplace_ancha.Pose())
    
    var.aux = var.aux + 1
    r.MoveJ(ini.Pose())
    r.Pause(2000)

# programa de roboDK place plancha soldada
def place_plancha_soldada():

    r = RDK.Item("ABB IRB 1660-4/1.55 (paletizado)", robolink.ITEM_TYPE_ROBOT)
    sistRefMesa = RDK.Item("rPaletizado", robolink.ITEM_TYPE_FRAME)
    toolR = RDK.Item("riQ EPick Vacuum Gripper", robolink.ITEM_TYPE_TOOL)
    
    r.setFrame(sistRefMesa)
    r.setTool(toolR)
    
    prepick_cuadro = RDK.Item("PrePickCuadro", robolink.ITEM_TYPE_TARGET)
    pick_cuadro = RDK.Item("PickCuadro", robolink.ITEM_TYPE_TARGET)
    preplace_cuadro = RDK.Item("PrePlacecuadro", robolink.ITEM_TYPE_TARGET)
    place_cuadro = RDK.Item("Placecuadro", robolink.ITEM_TYPE_TARGET)
    ini = RDK.Item("Inicio", robolink.ITEM_TYPE_TARGET)

    if var.plancha_acabada:
        r.MoveJ(prepick_cuadro.Pose())
        r.Pause(1000)
        r.MoveL(pick_cuadro.Pose())
        simulation.simulation_adjuntar_objeto(toolR)
        r.Pause(1000)
        r.MoveJ(prepick_cuadro.Pose())
        r.Pause(1000)
        r.MoveJ(preplace_cuadro.Pose())
        r.Pause(1000)
        r.MoveL(place_cuadro.Pose())
        simulation.simulation_soltar_objeto(toolR)
        r.Pause(2000)
        r.MoveJ(preplace_cuadro.Pose())
        var.en_cinta = True
        r.MoveJ(ini.Pose())
    
    