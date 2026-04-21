from modulos_python.entorno import preparar_entorno

RDK, project_dir = preparar_entorno()

from modulos_python import pick, place, bending, soldar, var
from modulos_python import mover_cintas as mc

"""
    Sustituir todos los var. 
    por setDO y 
    los if var. :
    por waitDI

    Ensenyarme a usar thread/tasks 
    en python para ponerlo en 
    las respectivas funciones
"""
for idx in range(2):
    if idx == 0:
        # ejecutar cinta larga, convertirlo a thread
        mc.mover_cinta_larga()
        # thread pick
        pick.pick_plancha_larga()
        # thread bending
        bending.bending_plancha_larga()
    elif idx == 1:
        # ejecutar cinta ancha, convertirlo a thread
        mc.mover_cinta_ancha()
        # thread pick
        pick.pick_plancha_ancha()
        # thread bending
        bending.bending_plancha_ancha()
    
    # thread place
    place.place_cinta_main()
    # ejecutar cinta_cuadro_avanza

    var.elegir += 1
    
    mc.mover_cinta_main()
    var.sensor_cuadro = False
    # ejecutar plancha_en_mesa
    place.place_plancha_mesa()
    var.en_mesa = False

# ejecutar soldar
soldar.soldar_ini()

place.place_plancha_soldada()
mc.mover_cinta_cuadro_acabada()
