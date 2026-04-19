import os
import sys

from robodk import robolink    # RoboDK API
from robodk import robomath    # Robot toolbox
RDK = robolink.Robolink()

# Ruta completa al .rdk abierto
rdk_file_param = RDK.getParam(robolink.FILE_OPENSTATION)

if not rdk_file_param:    
    raise Exception("Guarda y vuelve a abrir la estación .rdk antes de ejecutar el script")

if isinstance(rdk_file_param, bytes):
    rdk_file = rdk_file_param.decode("utf-8", errors="replace")
else:
    rdk_file = str(rdk_file_param)

# Carpeta del proyecto: .../PR2-A6
project_dir = os.path.dirname(os.path.abspath(rdk_file))

# Carpeta donde están tus módulos: .../PR2-A6/modulos_python
scripts_dir = os.path.join(project_dir, "modulos_python")
if not os.path.isdir(scripts_dir):    
    raise Exception(f"No existe la carpeta de scripts: {scripts_dir}")
if scripts_dir not in sys.path:    
    sys.path.insert(0, scripts_dir)

import pick
import place
import bending
import soldar
import var
import mover_cintas as mc

for idx in range(2):
    if var.elegir == 0:
        # ejecutar cinta larga, convertirlo a thread
        mc.mover_cinta_larga()
        # thread pick
        pick.pick_plancha()
        # thread bending
        bending.bending_plancha_larga()
    elif var.elegir == 1:
        # ejecutar cinta ancha, convertirlo a thread
        mc.mover_cinta_ancha()
        # thread pick
        pick.pick_plancha()
        # thread bending
        bending.bending_plancha_ancha()
    
    # thread place
    place.place_cinta_main()
    # ejecutar cinta_cuadro_avanza
    mc.mover_cinta_main()
    var.sensor_cuadro = False
    # ejecutar plancha_en_mesa
    place.place_plancha_mesa()
    var.en_mesa = False
    # ejecutar soldar
    soldar.soldar_ini()

mc.mover_cinta_cuadro_acabada()
