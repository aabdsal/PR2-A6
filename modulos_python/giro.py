from robodk import robolink
from modulos_python import simulation as sim
from modulos_python import var

nombre_mesa : str = "ABB Mesa Giratoria"

def giro_plancha(i : int):

    RDK = robolink.Robolink()
    mesa = RDK.Item(nombre_mesa, robolink.ITEM_TYPE_ROBOT)

    if i > 3:
        return
    
    esquina = "Esquina" + str(i)
    target_esquina = RDK.Item(esquina, robolink.ITEM_TYPE_TARGET)
    mesa.MoveJ(target_esquina)

def giro_mesa():
    RDK = robolink.Robolink()
    mesa = RDK.Item(nombre_mesa, robolink.ITEM_TYPE_ROBOT)

    target_giro = RDK.Item("Giro90", robolink.ITEM_TYPE_TARGET)
    mesa.MoveJ(target_giro)

def giro_final_plancha_soldada():
    RDK = robolink.Robolink()
    mesa = RDK.Item(nombre_mesa, robolink.ITEM_TYPE_ROBOT)
    
    target_final = RDK.Item("Final", robolink.ITEM_TYPE_TARGET)
    mesa.MoveJ(target_final)
    sim.mostrar_objeto("planchaAcabada")
    sim.ocultar_objeto("planchaLarga2")
    sim.ocultar_objeto("planchaAncha2")
    #var.plancha_acabada = True
