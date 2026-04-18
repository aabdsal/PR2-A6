from robodk import robolink    # RoboDK API
from robodk import robomath    # Robot toolbox
RDK = robolink.Robolink()

import mover_cintas as mc
import var

mc.mover_cinta_ancha_atras()
mc.mover_cinta_larga_atras()
mc.mover_cinta_main_atras()
var.var_resets()
