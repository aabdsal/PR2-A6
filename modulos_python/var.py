from robodk import robolink
from robodk import robomath
from pathlib import Path
import json
import queue
from typing import Any

JSON_PARAM_PATH = Path(__file__).resolve().parents[1] / "bbdd" / "parametros.json"

robot_yaskawa = "Yaskawa MH24 Prensado"
tool_yaskawa = "EPick Bend"

robot_abb_p = "ABB Paletizado"
tool_abb_p = "EPick Gripper"

robot_abb_s = "ABB Soldador"
tool_abb_s = "Welding Gun"

cinta_larga = "CintaLargoIni"
cinta_ancha = "CintaAnchoIni"
cinta_main = "CintaCuadroIni"
cinta_etiqueta = "CintaCuadroFini"
cinta_tapa = "CintaTapaInit"

mesa_giratoria = ""

frame_pick = "Pick"
frame_place = "Place"
frame_bending = "Bending"
frame_cinta_main = "FramePlanchaMain"
frame_cinta_etiqueta = "CuadroAcabada"
frame_welding = "RobotSoldador"
frame_mesa_giratoria = "MesaGiratoria"
frame_paletizado_mesa = "RobotPaletizado"

objetos_tcp: dict[str, robolink.Item] = {}
objeto_pose: dict[str, robomath.Mat] = {}
objeto_parentIni: dict[str, str] = {}

objetos_pendientes: dict[str, queue.Queue[robolink.Item]] = {
    "SensorCA" : queue.Queue(),
    "SensorCL" : queue.Queue(),
    "SensorCC" : queue.Queue(),
}

alternancia : queue.Queue[str] = queue.Queue()


def _estructura_json_vacia(): 
    return {
        "parametros": [],
        "info_objetos":{}
    }


def _cargar_json():
    if not JSON_PARAM_PATH.exists():
        return _estructura_json_vacia()

    try:
        with JSON_PARAM_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            return {
                "parametros": [str(x) for x in data],
                "info_objetos" : {}
            }

        if not isinstance(data, dict):
            return _estructura_json_vacia()

        resultado = _estructura_json_vacia()
        for clave in resultado:
            valor: Any = data.get(clave, [])
            if isinstance(valor, list):
                resultado[clave] = [str(x) for x in valor]

        return resultado
    except Exception:
        return _estructura_json_vacia()

def _guardar_json(data: dict[str, list[str]]):
    JSON_PARAM_PATH.parent.mkdir(parents=True, exist_ok=True)
    with JSON_PARAM_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def registrar_parametro_json(valor: str):
    clave = "parametros"
    data = _cargar_json()

    if clave not in data:
        data[clave] = []

    if valor not in data[clave]:
        data[clave].append(valor)
        _guardar_json(data)

def registrar_info_objeto_json(nombre_objeto, pose, frame : str):
    clave = "info_objetos"
    data = _cargar_json()

    if nombre_objeto not in data[clave]:
        data[clave].append(nombre_objeto)

    if pose not in data[clave]:
        data[clave].append(pose)

    if frame not in data[clave]:
        data[clave].append(frame)

    _guardar_json(data)