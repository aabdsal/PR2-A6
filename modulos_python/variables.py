"""Este script forma parte de modulos_python y es clave para la estación.

Guarda los nombres de robots, herramientas, frames, cintas y plantillas
que se usan en la simulación. También mantiene estructuras en memoria
para colas de sensores, alternancia y parámetros persistentes en JSON."""

from robodk import robolink
from pathlib import Path
from typing import Any

import json
import queue

robot_yaskawa = "Yaskawa MH24 Prensado"
tool_yaskawa = "EPick Bend"

robot_abb_p = "ABB Paletizado"
tool_abb_p = "EPick Gripper"

robot_abb_s = "ABB Soldador"
tool_abb_s = "Welding Gun"

mecanismos = [
 "CintaLargoIni",
 "CintaAnchoIni",
 "CintaCuadroIni",
 "CintaCuadroFini",
 "CintaTapaInit",
 "Yaskawa Giratoria"
]

cinta_restante = {
    "CintaLargoIni": 1000.0,
    "CintaAnchoIni": 1000.0,
    "CintaTapaInit": 1000.0,
    "CintaCuadroIni": 1000.0,
    "CintaCuadroFini": 1000.0,
}

cinta_larga = "CintaLargoIni"
cinta_ancha = "CintaAnchoIni"
cinta_main = "CintaCuadroIni"
cinta_etiqueta = "CintaCuadroFini"
cinta_tapa = "CintaTapaInit"

mesa_giratoria = "Yaskawa Giratoria"

frame_pick = "Pick"
frame_place = "Place"
frame_bending = "Bending"
frame_cinta_main = "FramePlanchaMain"
frame_welding = "RobotSoldador"
frame_mesa_giratoria = "Engranaje"
frame_paletizado_cinta_mesa = "Cinta_Mesa"
frame_paletizado = "RobotPaletizado"
frame_cinta_etiqueta = "FrameEtiqueta"

plantilla: dict[str, str] = {
    "ancha": "plantilla_planchaAncha",
    "larga": "plantilla_planchaLarga",
    "ancha1": "plantilla_planchaAncha1",
    "ancha2": "plantilla_planchaAncha2",
    "larga1": "plantilla_planchaLarga1",
    "larga2": "plantilla_planchaLarga2",
    "soldada": "plantilla_planchaSoldada",
    "tapa": "plantilla_tapaCuadro",
    "cuadroConTapa": "plantilla_cuadroConTapa",
    "etiqueta": "plantilla_etiqueta",
}

objetos_tcp: dict[str, robolink.Item] = {}


objetos_pendientes: dict[str, queue.Queue[str]] = {
    "SensorCA" : queue.Queue(),
    "SensorCL" : queue.Queue(),
    "SensorCM" : queue.Queue(),
    "SensorTapa" : queue.Queue(),
    "SensorEtiqueta" : queue.Queue(),
}

cola_soldadas : queue.Queue[str] = queue.Queue()
cola_cuadrosTapa : queue.Queue[str] = queue.Queue()
cola_cuadrosAcabados : queue.Queue[str] = queue.Queue()
cola_etiquetas : queue.Queue[str] = queue.Queue()

tiempo_ini = queue.Queue()
tiempo_fini = queue.Queue()

soldadas : queue.Queue[str] = queue.Queue()
alternancia : queue.Queue[str] = queue.Queue()

JSON_PARAM_PATH = Path(__file__).resolve().parents[1] / "database" / "parametros.json"

def _estructura_json_vacia(): 
    """Devuelve la estructura base para el archivo de parámetros."""

    return {
        "parametros": [],
    }

def _cargar_json():
    """Abre parametros.json y devuelve la estructura normalizada."""

    if not JSON_PARAM_PATH.exists():
        return _estructura_json_vacia()

    try:
        with JSON_PARAM_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            return {
                "parametros": [str(x) for x in data],
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
    """Guarda parámetros detectados en tiempo de ejecución."""

    JSON_PARAM_PATH.parent.mkdir(parents=True, exist_ok=True)
    with JSON_PARAM_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def registrar_parametro_json(valor: str):
    """Carga y actualiza la lista de parámetros en el JSON."""
    
    clave = "parametros"
    data = _cargar_json()

    if clave not in data:
        data[clave] = []

    if valor not in data[clave]:
        data[clave].append(valor)
        _guardar_json(data)