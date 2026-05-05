import psycopg
from modulos_python import simulation as sim
from datetime import datetime
from robodk import robolink
from robodk import robomath

curr = None
conn = None
h_ini_sensor = None
h_fin_sensor = None
# Para evitar que una misma detección dispare el tiempo varias veces
s1_bloqueado = False
s2_bloqueado = False

def conectar():
    global curr, conn
    try:
        conn = psycopg.connect(
            dbname="gdi",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        curr = conn.cursor()

        curr.execute("SET search_path TO proyecto;")
        print("Conexión a PostgreSQL realizada correctamente")

    except Exception as error:
        print("Error al conectar a la base de datos:")
        print(error)
        exit()

def buscar_pedido_pendiente(cursor):
    """Busca el pedido más urgente con unidades por fabricar."""
    sql = "SELECT id_pedido, cantidad_sol, cantidad_fab FROM pedido WHERE cantidad_fab < cantidad_sol ORDER BY fecha_lim ASC"
    cursor.execute(sql)
    return cursor.fetchone()


def registrar_producto(conexion, cursor, id_pedido, t_ini, t_fin):
    """Realiza la inserción en la BD."""
    id_prod = f"PR-{datetime.now().strftime('%H%M%S')}"
    try:
        cursor.execute("INSERT INTO unidad (id_producto, id_pedido, distribuidor, fase_actual) VALUES (%s, %s, %s, %s)",
                       (id_prod, id_pedido, 'LINEA_ROBODK', 1))
        
        cursor.execute("INSERT INTO se_realiza_en (id_producto, id_estacion, zona, hora_ini, hora_fin) VALUES (%s, %s, %s, %s, %s)",
                       (id_prod, 'ES01', 'ZN01', t_ini, t_fin))

        cursor.execute("UPDATE pedido SET cantidad_fab = cantidad_fab + 1 WHERE id_pedido = %s", (id_pedido,))

        conexion.commit()
    except Exception as error:
        conexion.rollback()

def leer_fotocelulas_robodk():
    """Consulta el estado físico de los sensores en la estación de RoboDK."""
    
    global h_fin_sensor, h_ini_sensor, s1_bloqueado, s2_bloqueado

    RDK = robolink.Robolink()
    
    while True:
        if RDK.getParam("SensorCA") == '1': 
            if not s1_bloqueado:
                h_ini_sensor = datetime.now()
                s1_bloqueado = True
                RDK.ShowMessage(f"S1 (Entrada) activado: {h_ini_sensor.strftime('%H:%M:%S')}", False)
        else:
            s1_bloqueado = False

        if RDK.getParam("SensorEtiqueta") == '1':
            if not s2_bloqueado:
                h_fin_sensor = datetime.now()
                s2_bloqueado = True

                if h_ini_sensor is not None:
                    pedido = buscar_pedido_pendiente(curr)
                    if pedido is not None:
                        registrar_producto(conn, curr, pedido[0], h_ini_sensor, h_fin_sensor)
                        h_ini_sensor = None
                        h_fin_sensor = None
        else:
            s2_bloqueado = False
        
        robomath.pause(0.1)
