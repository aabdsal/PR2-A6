"""Este módulo realiza los giros necesarios de la mesa giratoria."""

from robodk import robolink
from modulos_python import simulation as sim
from modulos_python import variables


def giro_plancha(i : int):
    """Mueve la mesa giratoria a una esquina predefinida (Esquina0..Esquina3).

    Se usa durante la soldadura para acercar la pieza al robot soldador."""

    RDK = robolink.Robolink()
    mesa = RDK.Item(variables.mesa_giratoria, robolink.ITEM_TYPE_ROBOT)

    if not mesa.Valid():
        raise RuntimeError("Nombre de la mesa inválido. Revisa nombres")

    esquina = "Esquina" + str(i)
    target_esquina = RDK.Item(esquina, robolink.ITEM_TYPE_TARGET)
    
    if not target_esquina.Valid():
        raise RuntimeError("Target de esquina inválido. Revisa nombres")
    
    mesa.MoveJ(target_esquina)

def giro_mesa():
    """Gira la mesa 90 grados para orientar la primera plancha en la mesa."""

    RDK = robolink.Robolink()
    mesa = RDK.Item(variables.mesa_giratoria, robolink.ITEM_TYPE_ROBOT)

    target_giro = RDK.Item("Giro90", robolink.ITEM_TYPE_TARGET)
    mesa.MoveJ(target_giro)

# TODO: Parametrizar los nombres de objetos a ocultar/mostrar en la mesa giratoria.
def giro_final_plancha_soldada():
    """Realiza el giro final del cuadro soldado para preparar la tapa.

    Al finalizar, se activa la salida digital planchaSoldada.
    """

    RDK = robolink.Robolink()
    mesa = RDK.Item(variables.mesa_giratoria, robolink.ITEM_TYPE_ROBOT)

    if not mesa.Valid():
        raise RuntimeError("Nombre de la mesa inválido. Revisa nombres")
    
    target_final = RDK.Item("Final", robolink.ITEM_TYPE_TARGET)

    if not target_final.Valid():
        raise RuntimeError("Target final inválido. Revisa nombres")
    
    mesa.MoveJ(target_final)
    sim.mostrar_objeto("planchaSoldada")
    sim.ocultar_objeto("planchaLarga2")
    sim.ocultar_objeto("planchaAncha2")
    sim.setDO("planchaSoldada", 1)
