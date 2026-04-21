from robodk import robolink

detecta_larga = False
detecta_ancha = False
sensor_cuadro = False
en_mesa = False
plancha_acabada = False
en_cinta = False
acabar = False
aux = 0
las_dos = False
elegir = 0
objetos_tcp: dict[str, robolink.Item] = {}

def var_resets():
    global detecta_larga
    global detecta_ancha
    global sensor_cuadro
    global en_mesa
    global plancha_acabada
    global en_cinta
    global acabar
    global aux
    global las_dos
    global elegir
    global objetos_tcp

    detecta_larga = False
    detecta_ancha = False
    sensor_cuadro = False
    en_mesa = False
    plancha_acabada = False
    en_cinta = False
    acabar = False
    aux = 0
    las_dos = False
    elegir = 0
    objetos_tcp.clear()
    