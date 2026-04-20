from robodk import robolink    # RoboDK API
from robodk import robomath    # Robot toolbox
RDK = robolink.Robolink()

from modulos_python import simulation as sim
from modulos_python import var

mesa = RDK.Item("ABB IRBP A250 D1000")

def giro_plancha(i : int):
    if i > 3:
        return
    
    esquina = "Esquina" + str(i)
    target_esquina = RDK.Item(esquina, robolink.ITEM_TYPE_TARGET)
    mesa.MoveJ(target_esquina)

def giro_mesa():
    target_giro = RDK.Item("Giro90", robolink.ITEM_TYPE_TARGET)
    mesa.MoveJ(target_giro)

def giro_ini_mesa():
    target_ini = RDK.Item("Inici", robolink.ITEM_TYPE_TARGET)
    mesa.MoveJ(target_ini)

def giro_final_plancha_soldada():
    target_final = RDK.Item("Final", robolink.ITEM_TYPE_TARGET)
    mesa.MoveJ(target_final)
    sim.simulation_mostrar_objeto("planchaAcabada")
    sim.simulation_ocultar_objeto("planchaLarga2")
    sim.simulation_ocultar_objeto("planchaAncha2")
    var.plancha_acabada = True
