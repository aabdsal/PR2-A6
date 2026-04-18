from robodk import robolink    # RoboDK API
from robodk import robomath    # Robot toolbox
RDK = robolink.Robolink()

import simulation
import var

sistRefBending = RDK.Item("Bending", robolink.ITEM_TYPE_FRAME)
home = RDK.Item("Home", robolink.ITEM_TYPE_TARGET)
sistRefPick = RDK.Item("Pick", robolink.ITEM_TYPE_FRAME)

def pick_plancha():
    robot = RDK.Item("Yaskawa MH24", robolink.ITEM_TYPE_ROBOT)
    toolR = RDK.Item("EPick Bend", robolink.ITEM_TYPE_TOOL)
    
    robot.setFrame(sistRefBending)
    robot.MoveJ(home.Pose())

    prepick: robolink.Item | None = None
    pick: robolink.Item | None = None

    robot.setFrame(sistRefPick)
    if var.detecta_larga:
        prepick = RDK.Item("PrePickLargo", robolink.ITEM_TYPE_TARGET)
        pick = RDK.Item("PickLargo", robolink.ITEM_TYPE_TARGET)
    elif var.detecta_ancha:
        prepick = RDK.Item("PrePickAncho", robolink.ITEM_TYPE_TARGET)
        pick = RDK.Item("PickAncho", robolink.ITEM_TYPE_TARGET)
    else:
        raise Exception("No se ha podido asignar target a prepick y pick")
    
    robot.MoveL(prepick.Pose())
    robot.Pause(1200)
    robot.MoveL(pick.Pose())
    simulation.simulation_adjuntar_objeto()
    robot.Pause(1200)
    robot.MoveL(prepick.Pose())   
    
    robot.Pause(500)
    