import psycopg
from modulos_python import variables as var
from datetime import datetime

curr = None
conn = None

def conectar():
    """Realiza la conexion con la base de datos que hay en postgresSQL"""
    global curr, conn
    try:  
        conn = psycopg.connect(
            dbname="gdi2026",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        curr = conn.cursor()

        curr.execute("SET search_path TO proyecto;")

    except Exception as error:
        print("Error al conectar a la base de datos:")
        print(error)
        exit()

def _buscar_pedido_pendiente(cursor):
    """Busca el pedido más urgente con unidades por fabricar."""
    sql = "SELECT id_pedido, cantidad_sol, cantidad_fab FROM pedido WHERE cantidad_fab < cantidad_sol ORDER BY fecha_lim ASC"
    cursor.execute(sql)
    return cursor.fetchone()

def _registrar_producto(conexion, cursor, id_pedido, t_ini, t_fin):
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

def actualizar_unidad():
    """Actualiza la tabla de bbds"""    
    if var.tiempo_ini.empty() or var.tiempo_fini.empty():
        return

    t_ini = var.tiempo_ini.get_nowait()
    t_fini = var.tiempo_fini.get_nowait()
    
    pedido = _buscar_pedido_pendiente(curr)
    if pedido is not None:
        _registrar_producto(conn, curr, pedido[0], t_ini, t_fini)

   