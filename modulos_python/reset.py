from robodk import robolink
from robodk import robomath
from modulos_python import var, giro, simulation


def reset_objetos():
    RDK = robolink.Robolink()
    
    lista_objetos = RDK.ItemList(robolink.ITEM_TYPE_OBJECT, True)

    for idx in lista_objetos:
        nombre_objeto = idx if isinstance(idx, str) else idx.Name()
        simulation.reemplazar_pos_objeto(nombre_objeto)

def reset_cinta(nombre_cinta : str):
    RDK = robolink.Robolink()

    item_cinta = RDK.Item(nombre_cinta, robolink.ITEM_TYPE_ROBOT)
    item_cinta.setJoints(robomath.Mat([[0]]))

simulation.mostrar_objeto("planxaLarga")
simulation.mostrar_objeto("planxaAncha")

simulation.ocultar_objeto("planchaLarga2")
simulation.ocultar_objeto("planchaAncha2")
simulation.ocultar_objeto("planchaAcabada")

var.var_resets()
giro.giro_ini_mesa()