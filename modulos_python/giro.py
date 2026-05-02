"""Este archivo realiza los giros necesarios de la mesa giratoria"""

from robodk import robolink
from modulos_python import simulation as sim
from modulos_python import variables


def giro_plancha(i : int):
    """Este método mueve la mesa giratoria hacia un movimiento predefinido 
    en la estación de robodk, la gracia es que como hay 4 movimientos 
    para los 4 lados de la estación, se han creado 4 targets llamados Esquina0,1,2,3.
    
    Entonces, al soldar se hace uso de este método para que el objeto se acerce al robot soldador y no alreves."""

    RDK = robolink.Robolink()
    mesa = RDK.Item(variables.mesa_giratoria, robolink.ITEM_TYPE_ROBOT)

    if not mesa.Valid():
        raise RuntimeError("nombre mesa inválido pepe")

    esquina = "Esquina" + str(i)
    target_esquina = RDK.Item(esquina, robolink.ITEM_TYPE_TARGET)
    
    if not target_esquina.Valid():
        raise RuntimeError("target esquina inválido pepe")
    
    mesa.MoveJ(target_esquina)

def giro_mesa():
    """Este metodo sirve para cuando estamos poniendo las dos planchas con forma de U encima de la mesa, 
    ya que el primer objeto que se ponga en la mesa debera de estar rotada 90 grados para que no afecte a la siguiente plancha."""

    RDK = robolink.Robolink()
    mesa = RDK.Item(variables.mesa_giratoria, robolink.ITEM_TYPE_ROBOT)

    target_giro = RDK.Item("Giro90", robolink.ITEM_TYPE_TARGET)
    mesa.MoveJ(target_giro)

# quitar lo de mostrar/ocultar objeto del frame de la mesa giratoria

"""
els noms pa ocultar mostrar han de pasarse per parametres o algo, soc moet, aell
"""
def giro_final_plancha_soldada():
    """Como su propio nombre indica, realiza el giro final del 
    cuadro soldado para preparla para ponerle la tapa. Para que
    se active la siguiente parte de código, se envia una salida
    digital en tiempo de ejecución con el nombre de planchaSoldada.
    """

    RDK = robolink.Robolink()
    mesa = RDK.Item(variables.mesa_giratoria, robolink.ITEM_TYPE_ROBOT)

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
