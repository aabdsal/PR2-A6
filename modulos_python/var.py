from robodk import robolink
from robodk import robomath
import queue

objetos_tcp: dict[str, robolink.Item] = {}

objeto_pose: dict[str, robomath.Mat] = {}

objetos_pendientes: dict[str, queue.Queue[robolink.Item]] = {
    "SensorCA" : queue.Queue(),
    "SensorCL" : queue.Queue(),
    "SensorCC" : queue.Queue(),
}

def var_resets():
    objetos_tcp.clear()
    objetos_pendientes.clear()
    objeto_pose.clear()
    