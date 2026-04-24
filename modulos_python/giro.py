from robodk import robolink
from modulos_python import simulation as sim
from modulos_python import var

def giro_plancha(i : int):

    RDK = robolink.Robolink()
    mesa = RDK.Item("ABB IRBP A250 D1000")

    if i > 3:
        return
    
    esquina = "Esquina" + str(i)
    target_esquina = RDK.Item(esquina, robolink.ITEM_TYPE_TARGET)
    mesa.MoveJ(target_esquina)

def giro_mesa():
    RDK = robolink.Robolink()
    mesa = RDK.Item("ABB IRBP A250 D1000")

    target_giro = RDK.Item("Giro90", robolink.ITEM_TYPE_TARGET)
    mesa.MoveJ(target_giro)

def giro_ini_mesa():
    RDK = robolink.Robolink()
    mesa = RDK.Item("ABB IRBP A250 D1000")
    
    target_ini = RDK.Item("Inici", robolink.ITEM_TYPE_TARGET)
    mesa.MoveJ(target_ini)

def giro_final_plancha_soldada():
    RDK = robolink.Robolink()
    mesa = RDK.Item("ABB IRBP A250 D1000")
    
    target_final = RDK.Item("Final", robolink.ITEM_TYPE_TARGET)
    mesa.MoveJ(target_final)
    sim.mostrar_objeto("planchaAcabada")
    sim.ocultar_objeto("planchaLarga2")
    sim.ocultar_objeto("planchaAncha2")
    #var.plancha_acabada = True
