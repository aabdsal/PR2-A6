"""Este script de python forma parte de la carpeta modulos_python, 
y es importante para el correcto funcionamiento de la estación.

Primeramente, se guardan todos los nombres de robots, herramientas, 
sistemas de referencia, cintas y plantillas de objetos que se 
consideran que van a ser usados en la estación.

Seguidamente, se hace uso de diccionarios (tablas hash) para guardar 
distinta información necesaria tanto para cuando acabe el programa 
como en tiempo de ejecuccion.

Se hace uso tambíen de tabla hash con colas para guardar los objetos que 
pasan por los determinados sensores que hay en toda la estación.

También se implementa una cola para decidir los movimientos del 
robot paletizado al coger una plancha ya prensada.

Finalmente, se implementan métodos y funciones para guardar información 
persistente en JSON sobre los parámetros de la estación,
que son importantes para poder hacer el reset en python."""

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
    """Función que devuelve el par clave: parametros valor : [] 
    en caso de que no el archivo no lo tenga creado"""

    return {
        "parametros": [],
    }

def _cargar_json():
    """Función que abre el archivo parametros.json, 
    comprueba si esta vacia, si no, devuelve una lista
    con los parámetros del archivo, esta función fue hecho con IA"""

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
    """Este método guarda nuevos parámetros detectados
    en tiempo de ejecución en la ruta del archivo JSON_PARAM_PATH"""

    JSON_PARAM_PATH.parent.mkdir(parents=True, exist_ok=True)
    with JSON_PARAM_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def registrar_parametro_json(valor: str):
    """Este método es el que se encarga de cargar y actualizar la lista del 
    archivo json mediante las funciones internas al script _cargar_json y _guardar_json"""
    
    clave = "parametros"
    data = _cargar_json()

    if clave not in data:
        data[clave] = []

    if valor not in data[clave]:
        data[clave].append(valor)
        _guardar_json(data)