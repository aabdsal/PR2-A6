import os
import sys
from robodk import robolink   

def preparar_entorno():
    RDK = robolink.Robolink()
    rdk_file_param = RDK.getParam(robolink.FILE_OPENSTATION)

    if not rdk_file_param:    
        raise Exception("Guarda y vuelve a abrir la estación .rdk antes de ejecutar el script")

    if isinstance(rdk_file_param, bytes):
        rdk_file = rdk_file_param.decode("utf-8", errors="replace")
    else:
        rdk_file = str(rdk_file_param)

    project_dir = os.path.dirname(os.path.abspath(rdk_file))

    if project_dir not in sys.path:
        sys.path.insert(0, project_dir)
    