import psycopg
import mqtt
from datetime import datetime
import time


# --- Variables Globales de Estado ---
conn = None
cur = None
var_mqtt = None
marca_tiempo_anterior = None 
h_ini_sensor = None
h_fin_sensor = None
# Para evitar que una misma detección dispare el tiempo varias veces
s1_bloqueado = False
s2_bloqueado = False

# --- Conexión a la BBDD  ---

def conectar_bd():
    try:
        conn = psycopg.connect(
            dbname="gdi",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()

        cur.execute("SET search_path TO proyecto;")
        print("Conexión a PostgreSQL realizada correctamente")

    except Exception as error:
        print("Error al conectar a la base de datos:")
        print(error)
        exit()


# --- Lógica de Base de Datos ---

def buscar_pedido_pendiente(cursor):
    """Busca el pedido más urgente con unidades por fabricar."""
    sql = "SELECT id_pedido, cantidad_sol, cantidad_fab FROM pedido WHERE cantidad_fab < cantidad_sol ORDER BY fecha_lim ASC LIMIT 1"
    cursor.execute(sql)
    return cursor.fetchone()


def registrar_producto(conexion, cursor, id_pedido, t_ini, t_fin):
    """Realiza la transacción de inserción en la BD."""
    id_prod = f"PR-{datetime.now().strftime('%H%M%S')}"
    try:
        # Inserciones siguiendo vuestro esquema
        cursor.execute("INSERT INTO unidad (id_producto, id_pedido, distribuidor, fase_actual) VALUES (%s, %s, %s, %s)",
                       (id_prod, id_pedido, 'LINEA_ROBODK', 1))
        
        cursor.execute("INSERT INTO se_realiza_en (id_producto, id_estacion, zona, hora_ini, hora_fin) VALUES (%s, %s, %s, %s, %s)",
                       (id_prod, 'ES01', 'ZN01', t_ini, t_fin))

        cursor.execute("UPDATE pedido SET cantidad_fab = cantidad_fab + 1 WHERE id_pedido = %s", (id_pedido,))

        conexion.commit()
        print(f"Producto {id_prod} guardado en Pedido {id_pedido}.")
    except Exception as error:
        print(f"Error al registrar: {error}")
        conexion.rollback()


# --- Lógica de Sensores RoboDK ---

def leer_fotocelulas_robodk():
    """Consulta el estado físico de los sensores en la estación de RoboDK."""
    global h_ini_sensor, h_fin_sensor, s1_bloqueado, s2_bloqueado
    
    # Usamos mqtt.RDK que ya está inicializado
    sensor1 = mqtt.RDK.Item('SensorCA')
    sensor2 = mqtt.RDK.Item('SensorEtiqueta')

    # Detección Fotocélula 1 (Entrada -> hora_ini)
    if sensor1.setParam('Sensor') == '1': 
        if not s1_bloqueado:
            h_ini_sensor = datetime.now()
            s1_bloqueado = True
            print(f"S1 (Entrada) activado: {h_ini_sensor.strftime('%H:%M:%S')}")
    else:
        s1_bloqueado = False

    # Detección Fotocélula 2 (Salida -> hora_fin)
    if sensor2.setParam('Sensor') == '1':
        if not s2_bloqueado:
            h_fin_sensor = datetime.now()
            s2_bloqueado = True
            print(f"S2 (Salida) activado: {h_fin_sensor.strftime('%H:%M:%S')}")
    else:
        s2_bloqueado = False


# ---  MQTT  ---2

def my_handle_message(mqttc, topic, payload):
    """Función que se ejecuta al recibir un mensaje MQTT."""
    global h_ini_sensor, h_fin_sensor, conn, cur
    
    # Si llega "on", significa producto terminado
    if topic == mqtt.hello_topic and payload == "on":
        if h_ini_sensor and h_fin_sensor:
            pedido = buscar_pedido_pendiente(cur)
            if pedido:
                registrar_producto(conn, cur, pedido[0], h_ini_sensor, h_fin_sensor)
            else:
                print("No hay pedidos pendientes.")
            
            # Reset de marcas de tiempo para la siguiente pieza
            h_ini_sensor, h_fin_sensor = None, None
        else:
            print("Error: Faltan tiempos de fotocélulas (S1 o S2 no detectados).")

# --- Ejecución Principal ---

if __name__ == "__main__":
    # Inicializar BD
    conn, cur = conectar_bd()
    
    # Configurar MQTT usando mqtt módulo
    mqtt.handle_message = my_handle_message
    mqtt.conectar()
    
    print("Sistema iniciado. Monitoreando fotocélulas en RoboDK...")

    try:
        while True:
            leer_fotocelulas_robodk() 
            time.sleep(0.1) 
            
    except KeyboardInterrupt:
        print("\nCerrando sistema...")
    finally:
        if cur: cur.close()
        if conn: conn.close()
        if mqtt.var_mqtt: mqtt.var_mqtt.loop_stop()