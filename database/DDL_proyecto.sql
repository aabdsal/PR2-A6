CREATE SCHEMA proyecto;
SET search_path TO proyecto;

-- 1. Tabla Cliente
CREATE TABLE cliente (
    id_cliente      VARCHAR(10) PRIMARY KEY,
    nombre          VARCHAR(20) NOT NULL,
    cif             VARCHAR(10) UNIQUE NOT NULL,
    direccion       VARCHAR(20) NOT NULL,
    n_telefono      VARCHAR(20) NOT NULL
);

-- 2. Tabla Transporte
CREATE TABLE transporte (
    id_transporte      VARCHAR(10) PRIMARY KEY,
    companyia          VARCHAR(20) NOT NULL,
    direccion_destino  VARCHAR(20) NOT NULL,
    fecha_salida       DATE NOT NULL,
    n_telefono         VARCHAR(20) NOT NULL,
    estado_viaje       VARCHAR(20) NOT NULL
);

-- 3. Tabla Pedido
CREATE TABLE pedido (
    id_pedido      VARCHAR(10) PRIMARY KEY,
    id_cliente     VARCHAR(10) NOT NULL REFERENCES cliente(id_cliente),
    id_transporte  VARCHAR(10) REFERENCES transporte(id_transporte), 
    cantidad_sol   INTEGER NOT NULL,
    cantidad_fab   INTEGER NOT NULL,
    fecha_lim      DATE NOT NULL,
    etiqueta       BOOLEAN NOT NULL,
    estado         VARCHAR(20) NOT NULL
);

-- 4. Tabla Unidad
CREATE TABLE unidad (
    id_producto    VARCHAR(10) PRIMARY KEY,
    id_pedido      VARCHAR(10) NOT NULL REFERENCES pedido(id_pedido),
    distribuidor   VARCHAR(20) NOT NULL,
    fase_actual    INTEGER NOT NULL
);

-- 5. Tabla Estacion
CREATE TABLE estacion (
    id_estacion    VARCHAR(10),
    zona           VARCHAR(10),
    nombre         VARCHAR(20) NOT NULL,
    PRIMARY KEY (id_estacion, zona)
);

-- 6. Tabla Supervisor
CREATE TABLE supervisor (
    codigo_empleado VARCHAR(10) PRIMARY KEY,
    id_estacion     VARCHAR(10) NOT NULL,
	zona            VARCHAR(10) NOT NULL,
    nombre          VARCHAR(20) NOT NULL,
    turno           INTEGER,
    FOREIGN KEY (id_estacion, zona) REFERENCES estacion(id_estacion,zona)
);

-- 7. Tabla Se_realiza_en 
CREATE TABLE se_realiza_en (
    id_producto     VARCHAR(10) REFERENCES unidad(id_producto),
    id_estacion     VARCHAR(10) NOT NULL,
    zona            VARCHAR(10) NOT NULL,
    hora_ini        TIMESTAMP NOT NULL,
    hora_fin        TIMESTAMP NOT NULL,
    PRIMARY KEY (id_producto, id_estacion, zona, hora_ini),
    FOREIGN KEY (id_estacion, zona) REFERENCES estacion(id_estacion, zona)
);