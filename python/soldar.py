from robodk import robolink
RDK = robolink.Robolink()

import giro

ACTION_RESET = -1
ACTION_OFF = 0
ACTION_ON = 1

DEFAULT_COLOR = "green"
DEFAULT_TOOL_NAME = "Fronius MTB500i Welding Gun"
DEFAULT_OBJECT_NAME = "planchaLarga2"


def _ensure_simulation_mode():
    if RDK.RunMode() != robolink.RUNMODE_SIMULATE:
        raise RuntimeError("La soldadura simulada solo se puede ejecutar en RUNMODE_SIMULATE")


def _resolve_spray_id(tool_name: str | None, action: int) -> int:
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


def _apply_spray_action(
    action: int,
    tool_name: str | None = DEFAULT_TOOL_NAME,
    object_name: str | None = DEFAULT_OBJECT_NAME,
    color: str = DEFAULT_COLOR,
) -> int:
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
            tool = RDK.Item("", robolink.ITEM_TYPE_TOOL)
            obj = RDK.Item("", robolink.ITEM_TYPE_OBJECT)
            if tool_name is not None:
                tool = RDK.Item(tool_name, robolink.ITEM_TYPE_TOOL)
            if object_name is not None:
                obj = RDK.Item(object_name, robolink.ITEM_TYPE_OBJECT)

            options_command = (
                "NO_PROJECT PARTICLE=SPHERE(2,8,1,1,1) STEP=1x0 RAND=0 COLOR="
                + str(color).lower().strip()
            )
            spray_id = int(RDK.Spray_Add(tool, obj, options_command))

        if tool_name is not None:
            RDK.setParam(tool_name, str(spray_id))

        RDK.Spray_SetState(robolink.SPRAY_ON, spray_id)
        return spray_id

    raise ValueError("Accion de soldadura no valida: " + str(action))


def soldar_ini(
    giros: int = 4,
    tool_name: str | None = DEFAULT_TOOL_NAME,
    object_name: str | None = DEFAULT_OBJECT_NAME,
    color: str = DEFAULT_COLOR,
) -> int:
    for i in range(giros):
        giro.giro_plancha(i)

    return _apply_spray_action(
        action=ACTION_ON,
        tool_name=tool_name,
        object_name=object_name,
        color=color,
    )


def soldar_stop(tool_name: str | None = DEFAULT_TOOL_NAME, clear_trace: bool = True):
    spray_id = _apply_spray_action(action=ACTION_OFF, tool_name=tool_name)
    if clear_trace:
        _apply_spray_action(action=ACTION_RESET, tool_name=tool_name)
    return spray_id


if __name__ == "__main__":
    import sys

    action = ACTION_ON
    color = DEFAULT_COLOR
    tool_name = DEFAULT_TOOL_NAME
    object_name = DEFAULT_OBJECT_NAME

    if len(sys.argv) > 1:
        action_str = sys.argv[1].strip().upper()
        if "ON" in action_str:
            action = ACTION_ON
        elif "OFF" in action_str:
            action = ACTION_OFF
        elif "RESET" in action_str:
            action = ACTION_RESET
        else:
            action = int(action_str)

    if len(sys.argv) > 2:
        tool_name = sys.argv[2].strip() or None

    if len(sys.argv) > 3:
        color = sys.argv[3].lower().strip()

    print("Applying action: " + str(action))
    print("Using tool: " + str(tool_name))
    print("Using color: " + str(color))

    _apply_spray_action(
        action=action,
        tool_name=tool_name,
        object_name=object_name,
        color=color,
    )
