from robodk import robolink    # RoboDK API
from robodk import robomath    # Robot toolbox
RDK = robolink.Robolink()

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
