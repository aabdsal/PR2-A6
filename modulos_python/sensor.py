from robodk import robolink    # RoboDK API
from robodk import robomath    # Robot toolbox
from modulos_python import simulation
RDK = robolink.Robolink()

def detectar_objeto(item_name, nombre_sensor : str):
    sensor = RDK.Item(nombre_sensor)
    item = RDK.Item(item_name)

    if not sensor.Valid():
        raise Exception("El sensor que me has pasado no existe en tu estación, revisa nombres")
    
    if not item.Valid():
        raise Exception("El objeto que me has pasado no existe en tu estación, revisa nombres")
    
    #sensor.setDO(nombre_sensor, 0)
    
    estado_detectado = -1
    while True:
        detectado = 0
        
        if sensor.Collision(item):
            detectado = 1
        
        if detectado != estado_detectado:
            estado_detectado = detectado
            simulation.setDO(nombre_sensor, str(detectado))
        
        robomath.pause(0.01)
    
"""
waitDI y setDO son I/O de robot/programa (entradas y salidas digitales).
"""