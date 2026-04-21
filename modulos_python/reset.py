from robodk import robolink    # RoboDK API
from robodk import robomath    # Robot toolbox
RDK = robolink.Robolink()

from modulos_python import var, giro
from modulos_python import mover_cintas as mc
from modulos_python import simulation as sim

estado_inicial_objetos = {}  # clave: nombre objeto

mc.mover_cinta_ancha_atras()
mc.mover_cinta_larga_atras()
mc.mover_cinta_main_atras()

sim.simulation_reemplazar_pos_objeto("planxaLarga")
sim.simulation_reemplazar_pos_objeto("planchaLarga1")
sim.simulation_reemplazar_pos_objeto("planchaLarga2")
sim.simulation_reemplazar_pos_objeto("planchaAncha")
sim.simulation_reemplazar_pos_objeto("planchaAncha1")
sim.simulation_reemplazar_pos_objeto("planchaAncha2")
sim.simulation_reemplazar_pos_objeto("planchaAcabada")

sim.simulation_mostrar_objeto("planxaLarga")
sim.simulation_mostrar_objeto("planxaAncha")

sim.simulation_mostrar_objeto("planchaLarga2")
sim.simulation_mostrar_objeto("planchaAncha2")
sim.simulation_mostrar_objeto("planchaAcabada")

var.var_resets()
giro.giro_ini_mesa()