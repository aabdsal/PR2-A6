"""Este script forma parte de modulos_python y es clave para la estación.

Guarda los nombres de robots, herramientas, frames, cintas y plantillas
que se usan en la simulación. También mantiene estructuras en memoria
para colas de sensores, alternancia y parámetros persistentes en JSON."""

from robodk import robolink
from robodk import robomath
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
frame_cinta_etiqueta = "CuadroAcabada"

plantilla = {
    "plantilla_planchaAncha"
    "plantilla_planchaLarga"
    "plantilla_planchaAncha1"
    "plantilla_planchaAncha2"
    "plantilla_planchaLarga1"
    "plantilla_planchaLarga2"
    "plantilla_planchaSoldada"
    "plantilla_tapaCuadro"
    "plantilla_cuadroConTapa"
    "plantilla_cuadroEtiquetada"
}

objetos_tcp: dict[str, robolink.Item] = {}
tiempos_proceso = {}

objetos_pendientes: dict[str, queue.Queue[str]] = {
    "SensorCA" : queue.Queue(),
    "SensorCL" : queue.Queue(),
    "SensorCC" : queue.Queue(),
    "SensorTapa" : queue.Queue(),
    "SensorEtiqueta" : queue.Queue(),
}

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