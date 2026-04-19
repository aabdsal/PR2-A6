from robodk import robolink    # RoboDK API
from robodk import robomath    # Robot toolbox
RDK = robolink.Robolink()

def giro_plancha(i : int):

    if i > 3:
        return
    
    mesa = RDK.Item("ABB IRBP A250 D1000")
    esquina = "Esquina" + str(i)
    target_esquina = RDK.Item(esquina, robolink.ITEM_TYPE_TARGET)
    mesa.MoveJ(target_esquina.Pose())

def giro_mesa():
    mesa = RDK.Item("ABB IRBP A250 D1000")
    target_giro = RDK.Item("Giro90", robolink.ITEM_TYPE_TARGET)
    mesa.MoveJ(target_giro.Pose())

def giro_ini_mesa():
    mesa = RDK.Item("ABB IRBP A250 D1000")
    target_ini = RDK.Item("Inici", robolink.ITEM_TYPE_TARGET)
    mesa.MoveJ(target_ini.Pose())