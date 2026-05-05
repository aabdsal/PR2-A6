import psycopg
import paho.mqtt.client as mqtt # No sé si esta libreria es la correcta
from datetime import datetime

# --- Variables Globales ---
conn = None
cur = None
hora_inicio_proceso = None


# --- Conexión a la BBDD ---
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
    print("Conexión realizada correctamente")

except Exception as error:
    print("Error al conectar a la base de datos:")
    print(error)
    exit()


# --- Lógica de Base de Datos ---

def procesar_producto_terminado(h_ini, h_fin):
    """
    Busca el pedido actual, inserta el producto y actualiza el pedido.
    """
    global conn, cur
    
    try:
        # Buscar el pedido que toca rellenar
        sql_buscar = """SELECT id_pedido, cantidad_sol, cantidad_fab 
                        FROM pedido 
                        WHERE cantidad_fab < cantidad_sol 
                        ORDER BY fecha_lim ASC"""
        cur.execute(sql_buscar)
        pedido = cur.fetchone()
        
        if not pedido:
            print("No hay pedidos pendientes en la BD")
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
        print("Se ha producido un error durante la inserción:")
        print(error)
        if conn is not None:
            conn.rollback() # Deshacer si falla


# --- MQTT ---

def on_connect(client, userdata, flags, rc):
    print("Conectado a MQTT. Esperando mensajes...")
    client.subscribe("HELLO_TOPIC") # CAMBIAR TOPIC

def on_message(client, userdata, msg):
    global marca_tiempo_anterior
    payload = msg.payload.decode("utf-8").strip().lower()
    
    if payload == "on":
        # La hora de fin de este ciclo es AHORA mismo
        hora_fin_actual = datetime.now()
        
        # Guardamos en base de datos usando la marca anterior como inicio
        procesar_producto_terminado(marca_tiempo_anterior, hora_fin_actual)
        
        # Actualizamos la marca de tiempo para que la siguiente plancha empiece a contar desde este exacto momento.
        marca_tiempo_anterior = hora_fin_actual


# --- Ejecución y Cierre (Tratamiento de Errores) ---

try:
    # Registramos la hora en la que arranca la estación por primera vez
    marca_tiempo_anterior = datetime.now()
    print(f"Estación iniciada a las: {marca_tiempo_anterior.strftime('%H:%M:%S')}")

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    
    client.connect("localhost", 1883, 60)
    print("Pulsa Ctrl+C para detener el programa.")
    client.loop_forever()

except KeyboardInterrupt:
    print("\nPrograma terminado por el usuario.")
except Exception as e:
    print(f"Error con MQTT: {e}")
finally:
    print("Cerrando conexiones a la Base de Datos...")
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()
    print("Programa finalizado.")