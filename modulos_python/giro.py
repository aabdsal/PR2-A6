from robodk import robolink
from modulos_python import simulation as sim
from modulos_python import var


def giro_plancha(i : int):

    RDK = robolink.Robolink()
    mesa = RDK.Item(var.mesa_giratoria, robolink.ITEM_TYPE_ROBOT)

    if not mesa.Valid():
        raise RuntimeError("nombre mesa inválido pepe")

    esquina = "Esquina" + str(i)
    target_esquina = RDK.Item(esquina, robolink.ITEM_TYPE_TARGET)
    
    if not target_esquina.Valid():
        raise RuntimeError("target esquina inválido pepe")
    
    mesa.MoveJ(target_esquina)

def giro_mesa():
    RDK = robolink.Robolink()
    mesa = RDK.Item(var.mesa_giratoria, robolink.ITEM_TYPE_ROBOT)

    target_giro = RDK.Item("Giro90", robolink.ITEM_TYPE_TARGET)
    mesa.MoveJ(target_giro)

# quitar lo de mostrar/ocultar objeto del frame de la mesa giratoria

"""
els noms pa ocultar mostrar han de pasarse per parametres o algo, soc moet, aell
"""
def giro_final_plancha_soldada():
    RDK = robolink.Robolink()
    mesa = RDK.Item(var.mesa_giratoria, robolink.ITEM_TYPE_ROBOT)

    if not mesa.Valid():
        raise RuntimeError("nombre mesa inválido pepe")
    
    target_final = RDK.Item("Final", robolink.ITEM_TYPE_TARGET)

    if not target_final.Valid():
        raise RuntimeError("target efinal inválido pepe")
    
    mesa.MoveJ(target_final)
    sim.mostrar_objeto("planchaSoldada")
    sim.ocultar_objeto("planchaLarga2")
    sim.ocultar_objeto("planchaAncha2")
    sim.setDO("planchaSoldada", 1)
