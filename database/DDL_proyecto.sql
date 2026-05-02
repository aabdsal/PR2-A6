-- ============================================
-- NUEVO ESQUEMA
-- ============================================

CREATE SCHEMA proyecto;

SET search_path TO proyecto;

CREATE TABLE cliente (
    id_cliente      VARCHAR(10) PRIMARY KEY,
    nombre          VARCHAR(100) NOT NULL,
    CIF             VARCHAR(10) UNIQUE,
    dirección       VARCHAR(100) NOT NULL,
    n_telefono      VARCHAR(100) NOT NULL
);

CREATE TABLE transporte (
    id_transporte      VARCHAR(10) PRIMARY KEY,
    companyia          VARCHAR(100) NOT NULL,
    direccion_destino  VARCHAR(10) NOT NULL,
    fecha_salida       DATE NOT NULL,
    n_telefono      VARCHAR(100) NOT NULL
    estado_viaje      VARCHAR(100) NOT NULL
);

CREATE TABLE pedido (
    id_pedido      VARCHAR(10) PRIMARY KEY,
    id_cliente      VARCHAR(10) REFERENCES cliente(id_cliente),
    id_transporte      VARCHAR(10) NOT NULL REFERENCES transporte(id_transporte),
    cantidad_sol     INTEGER NOT NULL,
    cantidad_fab    INTEGER NOT NULL,
    fecha_lim       DATE NOT NULL,
    etiqueta        INTEGER NOT NULL,
    estado          VARCHAR(10) NOT NULL
);

CREATE TABLE unidad (
    id_producto      VARCHAR(10) PRIMARY KEY,
    id_pedido       VARCHAR(10) NOT NULL REFERENCES pedido(id_pedido),
    tipo            VARCHAR(100) NOT NULL,
    distribuidor     VARCHAR(10) NOT NULL,
    fase_actual      INTEGER NOT NULL,
);

CREATE TABLE estacion (
    id_estacion VARCHAR(10) PRIMARY KEY,
    nombre      VARCHAR(100) NOT NULL
    zona     VARCHAR(10)  NOT NULL,
    nombre      VARCHAR(100) NOT NULL
);

CREATE TABLE supervisor (
    codigo_empleado      VARCHAR(10) PRIMARY KEY,
    id_estacion      VARCHAR(10) NOT NULL,
    nombre          VARCHAR(100) NOT NULL,
    turno             INTEGER,
);

CREATE TABLE se_realiza_en (
    id_producto      VARCHAR(10) PRIMARY KEY,
    id_estacion      VARCHAR(10) PRIMARY KEY,
    hora_ini        DATE PRIMARY KEY,
    hora_fin        DATE NOT NULL,
);

