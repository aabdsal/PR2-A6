"""Este módulo implementa la soldadura simulada del cuadro eléctrico."""

from robodk import robolink
RDK = robolink.Robolink()

from modulos_python import simulation as sim, variables as var, giro, mqtt
from typing import Optional
import json

ACTION_RESET = -1
ACTION_OFF = 0
ACTION_ON = 1

DEFAULT_COLOR = "black"

def _ensure_simulation_mode():
    """Valida que la estación esté en modo simulación."""
    if RDK.RunMode() != robolink.RUNMODE_SIMULATE:
        raise RuntimeError("La soldadura simulada solo se puede ejecutar en RUNMODE_SIMULATE")

def _resolve_spray_id(tool_name: str, action: int) -> int:
    """Resuelve un spray_id válido a partir de la herramienta y la acción."""
    info, data = RDK.Spray_GetStats()
    n_sprays_raw = data.size(1)
    if isinstance(n_sprays_raw, tuple):
        n_sprays = n_sprays_raw[1]
    else:
        n_sprays = n_sprays_raw

    spray_id = -1

    if n_sprays > 0 and tool_name is not None:
        spray_id_raw = RDK.getParam(tool_name)
        try:
            spray_id = int(spray_id_raw) if spray_id_raw is not None else -1
        except (TypeError, ValueError):
            spray_id = -1

        if spray_id < 0 or action == ACTION_ON or spray_id >= n_sprays:
            spray_id = -1
        else:
            print("Spray gun statistics:")
            print(info)
            print(data.tr())

    return spray_id


def _apply_spray_action(action: int, object_name: Optional[str] = None, tool_name: str = var.tool_abb_s, color: str = DEFAULT_COLOR) -> int:
    """Aplica una acción de soldadura y devuelve el spray_id asociado."""
    _ensure_simulation_mode()
    spray_id = _resolve_spray_id(tool_name, action)

    if action == ACTION_OFF:
        RDK.Spray_SetState(robolink.SPRAY_OFF, spray_id)
        return spray_id

    if action == ACTION_RESET:
        RDK.Spray_Clear(spray_id)
        return spray_id

    if action == ACTION_ON:
        if spray_id < 0:
            if not isinstance(object_name, str):
                raise ValueError("Se requiere un nombre de objeto válido para iniciar la soldadura.")

            tool = RDK.Item(tool_name, robolink.ITEM_TYPE_TOOL)
            obj = RDK.Item(object_name, robolink.ITEM_TYPE_OBJECT)

            if not tool.Valid():
                raise ValueError(f"La herramienta de soldadura '{tool_name}' no es válida o no se proporcionó.")
            
            # El objeto puede ser opcional para Spray_Add, pero en nuestro caso es necesario
            if not obj.Valid():
                raise ValueError(f"El objeto a soldar '{object_name}' no es válido o no se proporcionó.")

            options_command = (
                "NO_PROJECT PARTICLE=SPHERE(2,8,1,1,1) STEP=1x0 RAND=0 COLOR="
                + str(color).lower().strip()
            )
            spray_id = int(RDK.Spray_Add(tool, obj, options_command))

        RDK.Spray_SetState(robolink.SPRAY_ON, spray_id)
        return spray_id

    raise ValueError("Accion de soldadura no valida: " + str(action))


def iniciar(tool_name: str = var.tool_abb_s, color: str = DEFAULT_COLOR):
    """Ejecuta la secuencia de soldadura con giros y trazas simuladas."""
    
    r = RDK.Item(var.robot_abb_s, robolink.ITEM_TYPE_ROBOT)
    toolR = RDK.Item(var.tool_abb_s, robolink.ITEM_TYPE_TOOL)
    frame_weld = RDK.Item(var.frame_welding, robolink.ITEM_TYPE_FRAME)

    frame_mesa = RDK.Item(var.frame_mesa_giratoria, robolink.ITEM_TYPE_FRAME)

    sim.waitDI("LasDos", 1)
    sim.setDO("LasDos", 0)
    sim.setDO("mesaOcupada", 1)

    piezas_en_mesa = [item for item in frame_mesa.Childs() if item.Type() == robolink.ITEM_TYPE_OBJECT]
    
    r.setFrame(frame_weld)
    r.setTool(toolR)

    ini = RDK.Item("Inicio_Soldador", robolink.ITEM_TYPE_TARGET)
    prePIS = RDK.Item("prePIS", robolink.ITEM_TYPE_TARGET)
    targetPIS = RDK.Item("PIS", robolink.ITEM_TYPE_TARGET)
    targetPFS = RDK.Item("PFS", robolink.ITEM_TYPE_TARGET)
    postPFS = RDK.Item("postPFS", robolink.ITEM_TYPE_TARGET)

    #r.MoveJ(ini)
    for i in range(4):
        giro.giro_plancha(i)    
        r.MoveJ(prePIS)
        r.MoveL(targetPIS)
        r.Pause(500)
        r.setFrame(frame_mesa)
        
        mensaje = json.dumps({
        "estado_led": "welding",
        })
        mqtt.enviar_message(mqtt.led_topic, mensaje)

        _apply_spray_action(
            action=ACTION_ON,
            object_name=piezas_en_mesa[0].Name(),
            tool_name=tool_name,
            color=color,
        )
        
        r.setFrame(frame_weld)
        r.MoveL(targetPFS)
        soldar_stop(tool_name)
        r.MoveL(postPFS)

    giro.giro_final_plancha_soldada()

    r.MoveJ(ini)

    sim.setDO("planchaSoldada", 1)
    sim.setDO("mesaOcupada", 0)

    piezas_en_mesa = [item for item in frame_mesa.Childs() if item.Type() == robolink.ITEM_TYPE_OBJECT]
    
    RDK.Render(False)
    for pieza in piezas_en_mesa:
       pieza.setVisible(False)
       pieza.Delete()

    nuevo_objeto = sim.duplicar_objeto(var.plantilla["soldada"], frame_mesa.Name())
    RDK.Render(True)
    
    var.cola_soldadas.put(nuevo_objeto.Name())

def soldar_stop(tool_name: str = var.tool_abb_s, clear_trace: bool = True):
    """Detiene la soldadura y opcionalmente limpia la traza."""
    spray_id = _apply_spray_action(action=ACTION_OFF, tool_name=tool_name)
    if clear_trace:
        _apply_spray_action(action=ACTION_RESET, tool_name=tool_name)
    return spray_id

