import giro

from robodk import robolink    
from robodk import robomath    
RDK = robolink.Robolink()

ACTION_RESET = -1  
ACTION_OFF = 0 
ACTION_ON = 1 

Action = ACTION_ON
COLOR = 'green'
Tool_Name = 'Fronius MTB500i Welding Gun'  
Object_Name = 'planchaLarga2' 

def soldar_ini():    
    for i in range(4):
        # implementar codigo del programa robodk
        giro.giro_plancha()

    return

if RDK.RunMode() != RUNMODE_SIMULATE:
    quit()

import sys
if len(sys.argv) > 1:
    Action_str = sys.argv[1].strip().upper()
    if 'ON' in Action_str:
        Action = ACTION_ON
    elif 'OFF' in Action_str:
        Action = ACTION_OFF
    elif 'RESET' in Action_str:
        Action = ACTION_RESET
    else:
        Action = int(Action_str)

    if len(sys.argv) > 2:
        Tool_Name = sys.argv[2].strip()
        if Tool_Name == '':
            Tool_Name = None

        if len(sys.argv) > 3:
            COLOR = sys.argv[3].lower().strip()

print("Applying action: " + str(Action))
print("Using tool: " + str(Tool_Name))
print("Using color: " + COLOR)

info, data = RDK.Spray_GetStats()
n_sprays = data.size(1)
spray_id = -1
if n_sprays > 0 and Tool_Name is not None:
    spray_id = RDK.getParam(Tool_Name)
    if spray_id is None or Action == ACTION_ON or type(spray_id) == str or spray_id >= n_sprays:
        spray_id = -1

    print("Spray gun statistics:")
    print(info)
    print(data.tr())

if Action is None:
    print('Note: This macro can be called as ArcStart(1) or ArcStart(0) or ArcStart(-1)')
    entry = mbox('Turn gun ON or OFF', ('On', '1'), ('Off', '0'))
    if not entry:
        quit()
    Action = int(entry)

if Action == ACTION_OFF:
    RDK.Spray_SetState(SPRAY_OFF, spray_id)
    RDK.Spray_Clear(spray_id)
elif Action == ACTION_ON:
    if spray_id < 0:
        tool = 0  
        obj = 0  
        if Tool_Name is not None:
            tool = RDK.Item(Tool_Name, ITEM_TYPE_TOOL)

        if Object_Name is not None:
            obj = RDK.Item(Object_Name, ITEM_TYPE_OBJECT)
        options_command = "NO_PROJECT PARTICLE=SPHERE(2,8,1,1,1) STEP=1x0 RAND=0 COLOR=" + COLOR

        spray_id = RDK.Spray_Add(tool, obj, options_command)
    
    if Tool_Name is not None:
        RDK.setParam(Tool_Name, spray_id)

    RDK.Spray_SetState(SPRAY_ON, spray_id)

