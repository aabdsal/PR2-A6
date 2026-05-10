-- ============================================
--  DATOS DE PRUEBA
-- ============================================

SET search_path TO proyecto;

-- ============================================
-- CLIENTES
-- ============================================
INSERT INTO cliente (id_cliente, nombre, CIF, direccion, n_telefono)
VALUES
('CL001', 'Alfa Textil', 'CIF10001', 'Calle Norte 12', '910111111'),
('CL002', 'Beta Plast', 'CIF10002', 'Avenida Sur 45', '910222222'),
('CL003', 'Gamma Metal', 'CIF10003', 'Plaza Centro 3', '910333333'),
('CL004', 'Delta Agro', 'CIF10004', 'Camino Rural 8', '910444444'),
('CL005', 'Epsilon Med', 'CIF10005', 'Calle Rio 21', '910555555'),
('CL006', 'Zeta Papel', 'CIF10006', 'Avenida Sol 14', '910666666'),
('CL007', 'Eta Food', 'CIF10007', 'Calle Lago 6', '910777777'),
('CL008', 'Theta Print', 'CIF10008', 'Calle Mar 9', '910888888'),
('CL009', 'Iota Glass', 'CIF10009', 'Avenida Este 5', '910999999'),
('CL010', 'Kappa Tools', 'CIF10010', 'Calle Oeste 10', '911000000'),
('CL011', 'Lambda Home', 'CIF10011', 'Calle Norte 18', '911111111'),
('CL012', 'Mu Electric', 'CIF10012', 'Avenida Sur 70', '911222222'),
('CL013', 'Nu Pharma', 'CIF10013', 'Calle Centro 2', '911333333'),
('CL014', 'Xi Auto', 'CIF10014', 'Calle Rio 33', '911444444'),
('CL015', 'Omicron Lab', 'CIF10015', 'Plaza Norte 1', '911555555'),
('CL016', 'Pi Pack', 'CIF10016', 'Camino Verde 5', '911666666'),
('CL017', 'Rho Build', 'CIF10017', 'Avenida Mar 16', '911777777'),
('CL018', 'Sigma Clean', 'CIF10018', 'Calle Sol 77', '911888888'),
('CL019', 'Tau Sports', 'CIF10019', 'Calle Lago 22', '911999999'),
('CL020', 'Upsilon Tech', 'CIF10020', 'Avenida Este 40', '912000000');

-- ============================================
-- TRANSPORTE
-- ============================================
INSERT INTO transporte (id_transporte, companyia, direccion_destino, fecha_salida, n_telefono, estado_viaje)
VALUES
('TR001', 'FastMove', 'MAD01', '2026-01-10', '900101010', 'programado'),
('TR002', 'RouteMax', 'BCN02', '2026-01-12', '900202020', 'programado'),
('TR003', 'CargoLine', 'VAL03', '2026-01-14', '900303030', 'en_ruta'),
('TR004', 'TransEuropa', 'SEV04', '2026-01-16', '900404040', 'en_ruta'),
('TR005', 'IberLog', 'BIL05', '2026-01-18', '900505050', 'entregado'),
('TR006', 'NorteTrack', 'ZAR06', '2026-01-20', '900606060', 'entregado'),
('TR007', 'SurExpress', 'MAL07', '2026-01-22', '900707070', 'programado'),
('TR008', 'DeltaShip', 'ALC08', '2026-01-24', '900808080', 'programado');

-- ============================================
-- PEDIDOS
-- ============================================
INSERT INTO pedido (id_pedido, id_cliente, id_transporte, cantidad_sol, cantidad_fab, fecha_lim, etiqueta, estado)
VALUES
('PE001', 'CL001', 'TR001', 1200, 800, '2026-01-20', TRUE, 'abierto'),
('PE002', 'CL002', 'TR001', 500, 500, '2026-01-22', TRUE, 'cerrado'),
('PE003', 'CL003', 'TR002', 300, 150, '2026-01-25', TRUE, 'abierto'),
('PE004', 'CL004', 'TR002', 900, 600, '2026-01-27', TRUE, 'en_fab'),
('PE005', 'CL005', 'TR003', 1500, 1200, '2026-01-30', TRUE, 'en_fab'),
('PE006', 'CL006', 'TR003', 700, 700, '2026-02-01', TRUE, 'cerrado'),
('PE007', 'CL007', 'TR004', 250, 200, '2026-02-03', FALSE, 'abierto'),
('PE008', 'CL008', 'TR004', 400, 350, '2026-02-05', FALSE, 'en_fab'),
('PE009', 'CL009', 'TR005', 1100, 900, '2026-02-07', TRUE, 'en_fab'),
('PE010', 'CL010', 'TR005', 600, 600, '2026-02-09', FALSE, 'cerrado'),
('PE011', 'CL011', 'TR006', 950, 500, '2026-02-11', TRUE, 'abierto'),
('PE012', 'CL012', 'TR006', 480, 420, '2026-02-13', TRUE, 'en_fab'),
('PE013', 'CL013', 'TR007', 1300, 900, '2026-02-15', FALSE, 'abierto'),
('PE014', 'CL014', 'TR007', 520, 300, '2026-02-17', TRUE, 'abierto'),
('PE015', 'CL015', 'TR008', 780, 780, '2026-02-19', TRUE, 'cerrado'),
('PE016', 'CL016', 'TR008', 860, 500, '2026-02-21', TRUE, 'en_fab'),
('PE017', 'CL017', 'TR001', 1400, 1000, '2026-02-23', FALSE, 'abierto'),
('PE018', 'CL018', 'TR002', 350, 200, '2026-02-25', TRUE, 'abierto'),
('PE019', 'CL019', 'TR003', 620, 620, '2026-02-27', TRUE, 'cerrado'),
('PE020', 'CL020', 'TR004', 910, 450, '2026-03-01', FALSE, 'en_fab');

-- ============================================
-- UNIDADES
-- ============================================
INSERT INTO unidad (id_producto, id_pedido, distribuidor, fase_actual)
VALUES
('PR001', 'PE001', 'DIST01', 2),
('PR002', 'PE001', 'DIST01', 3),
('PR003', 'PE001', 'DIST02', 1),
('PR004', 'PE002', 'DIST03', 4),
('PR005', 'PE002', 'DIST03', 4),
('PR006', 'PE003', 'DIST02', 2),
('PR007', 'PE003', 'DIST02', 2),
('PR008', 'PE004', 'DIST04', 1),
('PR009', 'PE004', 'DIST04', 2),
('PR010', 'PE005', 'DIST01', 3),
('PR011', 'PE005', 'DIST01', 2),
('PR012', 'PE006', 'DIST03', 5),
('PR013', 'PE006', 'DIST03', 5),
('PR014', 'PE007', 'DIST02', 1),
('PR015', 'PE007', 'DIST02', 2),
('PR016', 'PE008', 'DIST04', 1),
('PR017', 'PE008', 'DIST04', 2),
('PR018', 'PE009', 'DIST05', 3),
('PR019', 'PE009', 'DIST05', 3),
('PR020', 'PE010', 'DIST03', 5),
('PR021', 'PE010', 'DIST03', 5),
('PR022', 'PE011', 'DIST02', 1),
('PR023', 'PE011', 'DIST02', 2),
('PR024', 'PE012', 'DIST04', 2),
('PR025', 'PE012', 'DIST04', 3),
('PR026', 'PE013', 'DIST01', 2),
('PR027', 'PE013', 'DIST05', 1),
('PR028', 'PE014', 'DIST03', 2),
('PR029', 'PE014', 'DIST03', 3),
('PR030', 'PE015', 'DIST04', 5),
('PR031', 'PE015', 'DIST04', 5),
('PR032', 'PE016', 'DIST01', 2),
('PR033', 'PE016', 'DIST01', 1),
('PR034', 'PE017', 'DIST05', 2),
('PR035', 'PE017', 'DIST05', 3),
('PR036', 'PE018', 'DIST02', 1),
('PR037', 'PE018', 'DIST02', 2),
('PR038', 'PE019', 'DIST03', 5),
('PR039', 'PE019', 'DIST03', 5),
('PR040', 'PE020', 'DIST04', 2);

-- ============================================
-- ESTACIONES
-- ============================================
INSERT INTO estacion (id_estacion, zona, nombre)
VALUES 
('ES01', 'ZN01', 'prensado'),
('ES01', 'ZN02', 'soldado'),
('ES01', 'ZN03', 'etiquetado'),
('ES02', 'ZN01', 'prensado'),
('ES02', 'ZN02', 'soldado'),
('ES02', 'ZN03', 'etiquetado'),
('ES03', 'ZN01', 'prensado'),
('ES03', 'ZN02', 'soldado'),
('ES03', 'ZN03', 'etiquetado'),
('ES04', 'ZN01', 'prensado'),
('ES04', 'ZN02', 'soldado'),
('ES04', 'ZN03', 'etiquetado'),
('ES05', 'ZN01', 'prensado'),
('ES05', 'ZN02', 'soldado'),
('ES05', 'ZN03', 'etiquetado'),
('ES06', 'ZN01', 'prensado'),
('ES06', 'ZN02', 'soldado'),
('ES06', 'ZN03', 'etiquetado'),
('ES07', 'ZN01', 'prensado'),
('ES07', 'ZN02', 'soldado'),
('ES07', 'ZN03', 'etiquetado'),
('ES08', 'ZN01', 'prensado'),
('ES08', 'ZN02', 'soldado'),
('ES08', 'ZN03', 'etiquetado'),
('ES09', 'ZN01', 'prensado'),
('ES09', 'ZN02', 'soldado'),
('ES09', 'ZN03', 'etiquetado'),
('ES10', 'ZN01', 'prensado'),
('ES10', 'ZN02', 'soldado'),
('ES10', 'ZN03', 'etiquetado');

-- ============================================
-- SUPERVISORES
-- ============================================
INSERT INTO supervisor (codigo_empleado, id_estacion, zona, nombre, turno)
VALUES
('SP001', 'ES01', 'ZN01', 'Mario Ruiz', 1),
('SP002', 'ES02', 'ZN01', 'Sara Molina', 2),
('SP003', 'ES03', 'ZN01', 'Luis Vega', 1),
('SP004', 'ES04', 'ZN01', 'Elena Diaz', 3),
('SP005', 'ES05', 'ZN01', 'Carlos Sanz', 2),
('SP006', 'ES06', 'ZN01', 'Nuria Prieto', 1),
('SP007', 'ES01', 'ZN02', 'Jorge Gil', 2),
('SP008', 'ES02', 'ZN02', 'Irene Lara', 3),
('SP009', 'ES03', 'ZN02', 'Hugo Rey', 2),
('SP010', 'ES04', 'ZN02', 'Marta Cano', 1);

-- ============================================
-- SE REALIZA EN
-- ============================================
INSERT INTO se_realiza_en (id_producto, id_estacion, zona, hora_ini, hora_fin)
VALUES
('PR001', 'ES01', 'ZN01', '08:00:00', '08:02:00'),
('PR002', 'ES02', 'ZN01', '08:00:00', '08:02:00'),
('PR003', 'ES03', 'ZN01', '08:00:00', '08:02:00'),
('PR004', 'ES04', 'ZN01', '08:00:00', '08:02:00'),
('PR005', 'ES05', 'ZN01', '08:00:00', '08:02:00'),
('PR006', 'ES06', 'ZN01', '08:00:00', '08:02:00'),
('PR007', 'ES01', 'ZN02', '08:00:00', '08:02:00'),
('PR008', 'ES02', 'ZN02', '08:00:00', '08:02:00'),
('PR009', 'ES03', 'ZN02', '08:00:00', '08:02:00'),
('PR010', 'ES04', 'ZN02', '08:00:00', '08:02:00'),
('PR011', 'ES05', 'ZN02', '08:00:00', '08:02:00'),
('PR012', 'ES06', 'ZN02', '08:00:00', '08:02:00'),
('PR013', 'ES01', 'ZN03', '08:00:00', '08:02:00'),
('PR014', 'ES02', 'ZN03', '08:00:00', '08:02:00'),
('PR015', 'ES03', 'ZN03', '08:00:00', '08:02:00'),
('PR016', 'ES04', 'ZN03', '08:00:00', '08:02:00'),
('PR017', 'ES05', 'ZN03', '08:00:00', '08:02:00'),
('PR018', 'ES06', 'ZN03', '08:00:00', '08:02:00'),
('PR019', 'ES01', 'ZN01', '08:00:00', '08:02:00'),
('PR020', 'ES02', 'ZN03', '08:00:00', '08:02:00'),
('PR021', 'ES03', 'ZN02', '08:00:00', '08:02:00'),
('PR022', 'ES04', 'ZN02', '08:00:00', '08:02:00'),
('PR023', 'ES05', 'ZN02', '08:00:00', '08:02:00'),
('PR024', 'ES06', 'ZN03', '08:00:00', '08:02:00'),
('PR025', 'ES01', 'ZN02', '08:00:00', '08:02:00'),
('PR026', 'ES02', 'ZN02', '08:00:00', '08:02:00'),
('PR027', 'ES03', 'ZN01', '08:00:00', '08:02:00'),
('PR028', 'ES04', 'ZN02', '08:00:00', '08:02:00'),
('PR029', 'ES05', 'ZN01', '08:00:00', '08:02:00'),
('PR030', 'ES06', 'ZN01', '08:00:00', '08:02:00');