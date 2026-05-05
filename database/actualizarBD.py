import psycopg
import paho.mqtt.client as mqtt
from datetime import datetime


# --- Variables y Configuración MQTT (de mqtt.py) ---
broker = "mqtt.dsic.upv.es"
port = 1883
user = "giirob"
passwd = "UPV2024"

# Topics definidos
hello_topic = "giirob/pr2_a6/devices/hello"
button_topic = "giirob/pr2_a6/devices/button"
emergency_stop_topic = "giirob/pr2_a6/devices/emergency_stop"

# --- Variables Globales de Estado ---
conn = None
cur = None
var_mqtt = None
marca_tiempo_anterior = None 

# --- Conexión a la BBDD  ---
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

def procesar_producto_terminado(h_ini, h_fin):
    """Busca el pedido actual, inserta el producto y actualiza el pedido."""
    global conn, cur
    try:
        # Buscar pedido pendiente
        sql_buscar = """SELECT id_pedido, cantidad_sol, cantidad_fab 
                        FROM pedido 
                        WHERE cantidad_fab < cantidad_sol 
                        ORDER BY fecha_lim ASC"""
        cur.execute(sql_buscar)
        pedido = cur.fetchone()
        
        if not pedido:
            print("No hay pedidos pendientes en la BD.")
            return
            
        id_pedido = pedido[0]
        cant_sol = pedido[1]
        cant_fab = pedido[2]

        id_nuevo_producto = f"PR-{datetime.now().strftime('%H%M%S')}"

        # Verificar que no existe
        sql_check = "SELECT 1 FROM unidad WHERE id_producto = %s"
        cur.execute(sql_check, (id_nuevo_producto,))
        if cur.fetchone():
            print(f"Error: Producto {id_nuevo_producto} ya existe")
            return

        # Insertar en tabla UNIDAD
        sql_unidad = """INSERT INTO unidad 
                        (id_producto, id_pedido, distribuidor, fase_actual) 
                        VALUES (%s, %s, %s, %s)"""
        cur.execute(sql_unidad, (id_nuevo_producto, id_pedido, 'LINEA_AUTO', 1))

        # Insertar en tabla SE_REALIZA_EN
        sql_tiempos = """INSERT INTO se_realiza_en 
                         (id_producto, id_estacion, zona, hora_ini, hora_fin) 
                         VALUES (%s, %s, %s, %s, %s)"""
        cur.execute(sql_tiempos, (id_nuevo_producto, 'ES01', 'ZN01', h_ini, h_fin))

        # Actualizar tabla PEDIDO
        sql_update = "UPDATE pedido SET cantidad_fab = cantidad_fab + 1 WHERE id_pedido = %s"
        cur.execute(sql_update, (id_pedido,))

        # Confirmar inserciones
        conn.commit()
        print(f"Registrado: Producto {id_nuevo_producto} asignado al pedido {id_pedido}")
        
        # Comprobar si se ha cerrado el pedido
        if (cant_fab + 1) >= cant_sol:
            print(f"¡PEDIDO {id_pedido} COMPLETADO!")

    except Exception as error:
        print(f"Error en la inserción: ")
        print(error)
        if conn is not None: 
            conn.rollback()

# ---  MQTT  ---

def recibir_menssage(mqttc, obj, msg):
    """Decodifica el mensaje y delega a handle_message"""
    payload = msg.payload.decode('utf-8').strip().lower()
    topic = msg.topic
    handle_message(mqttc, topic, payload)

def handle_message(mqttc, topic, payload):
    """Gestiona la lógica de 'on' para actualizar la BD"""
    global marca_tiempo_anterior
    
    # Si el LED se enciende, procesamos el ciclo transcurrido
    if topic == hello_topic and payload == "on":
        hora_fin_actual = datetime.now()
        
        # Guardar en BD usando la marca anterior como inicio
        procesar_producto_terminado(marca_tiempo_anterior, hora_fin_actual)
        
        # Actualizar la marca para el siguiente producto
        marca_tiempo_anterior = hora_fin_actual

def conectar():
    """Configura e inicia la conexión MQTT"""
    global var_mqtt

    var_mqtt = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    var_mqtt.on_message = recibir_menssage

    var_mqtt.username_pw_set(username=user, password=passwd)
    var_mqtt.connect(broker, port, 60)

    # Suscripciones topics
    var_mqtt.subscribe(hello_topic, 0)
    var_mqtt.subscribe(button_topic, 0)
    var_mqtt.subscribe(emergency_stop_topic, 0)

    print(f"Suscrito a topics en {broker}. Esperando mensajes...")
    var_mqtt.loop_start()

# --- Ejecución Principal ---

if __name__ == "__main__":
    try:
        # Marca de tiempo inicial al arrancar la estación
        marca_tiempo_anterior = datetime.now()
        print(f"Estación iniciada a las: {marca_tiempo_anterior.strftime('%H:%M:%S')}")

        conectar()

        # Mantener el script vivo para recibir mensajes
        while True:
            pass

    except KeyboardInterrupt:
        print("\nPrograma terminado por el usuario.")
    finally:
        print("Cerrando conexiones...")
        if cur is not None: cur.close()
        if conn is not None: conn.close()
        if var_mqtt is not None: var_mqtt.loop_stop()