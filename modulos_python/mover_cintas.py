"""Este módulo contiene las funciones necesarias para
simular el movimiento de los objetos sobre las cintas.

Queda por decidir si el duplicado de objetos se implementa aquí o en otro sitio.
"""

from robodk import robolink
from robodk import robomath
from modulos_python import variables

from modulos_python import simulation

def _mover_cinta(cinta_name: str, param_sensor: str, RDK : robolink.Robolink | None = None):
    """Mueve una cinta mientras el sensor no detecte ningún objeto.

    Si no se recibe un Robolink, crea una conexión local para permitir
    mover varias cintas en paralelo.
    """

    if RDK is None:
        RDK = robolink.Robolink()
    
    cinta = RDK.Item(cinta_name, robolink.ITEM_TYPE_ROBOT)
    if not cinta.Valid():
        raise RuntimeError("El nombre de la cinta no existe")

    incremento = 15.0

    while param_sensor is not None and int(RDK.getParam(param_sensor) or 0) != 1:
        
        cinta.setJoints(cinta.Joints() + robomath.Mat([[incremento]]))
        
        robomath.pause(0.01)

def mover_cinta_ancha():
    """Método que mueve la cinta por donde pasan las planchas anchas, 
    y el sensor encargado de notificar si hay objeto es el SensorCA"""
    _mover_cinta(variables.cinta_ancha, "SensorCA")

def mover_cinta_larga():
    """Método que mueve la cinta por donde pasan las planchas largas, 
    y el sensor encargado de notificar si hay objeto es el SensorCL"""

    _mover_cinta(variables.cinta_larga, "SensorCL")

def mover_cinta_tapa():
    """Método que mueve la cinta por donde pasan las tapas, 
    y el sensor encargado de notificar si hay objeto es el SensorTapa"""

    _mover_cinta(variables.cinta_tapa, "SensorTapa")

def mover_cinta_main(RDK : robolink.Robolink):
    """Método que mueve la cinta principal, donde van las planchasLargas2 
    y planchasAnchas2. El sensor encargado de notificar si hay objeto es el SensorCC.

    Implementa una espera digital que se activa cuando el yaskawa pone una plancha prensada en la cinta"""

    simulation.waitDI("enCintaMain", 1)
    simulation.setDO("enCintaMain", 0)
    
    _mover_cinta(variables.cinta_main, "SensorCC", RDK)

def mover_cinta_cuadro_acabada():
    """Mueve la cinta final donde salen los cuadros eléctricos hacia el túnel.

    Implementa una espera digital que se activa cuando el ABB paletizado
    pone el cuadro con tapa en la cinta. Falta la lógica para detenerse
    2 segundos en el túnel de etiquetado.
    """

    simulation.waitDI("EnCintaEtiquetar", 1)
    simulation.setDO("EnCintaEtiquetar", 0)
        
    _mover_cinta(variables.cinta_etiqueta, "SensorEtiqueta")
    simulation.ocultar_objeto("cuadroConTapa") # sustituir por objeto que hay en la cola, falta implementación
    # tambien faltaria eliminar ese objeto para que no se guarde basura en la estació
