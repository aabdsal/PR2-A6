-- ============================================
-- PROYECTO - DATOS DE PRUEBA
-- ============================================

SET search_path TO proyecto;

-- ============================================
-- CLIENTES
-- ============================================
INSERT INTO cliente (id_cliente, nombre, CIF, "dirección", n_telefono)
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
('PE001', 'CL001', 'TR001', 1200, 800, '2026-01-20', 101, 'abierto'),
('PE002', 'CL002', 'TR001', 500, 500, '2026-01-22', 102, 'cerrado'),
('PE003', 'CL003', 'TR002', 300, 150, '2026-01-25', 103, 'abierto'),
('PE004', 'CL004', 'TR002', 900, 600, '2026-01-27', 104, 'en_fab'),
('PE005', 'CL005', 'TR003', 1500, 1200, '2026-01-30', 105, 'en_fab'),
('PE006', 'CL006', 'TR003', 700, 700, '2026-02-01', 106, 'cerrado'),
('PE007', 'CL007', 'TR004', 250, 200, '2026-02-03', 107, 'abierto'),
('PE008', 'CL008', 'TR004', 400, 350, '2026-02-05', 108, 'en_fab'),
('PE009', 'CL009', 'TR005', 1100, 900, '2026-02-07', 109, 'en_fab'),
('PE010', 'CL010', 'TR005', 600, 600, '2026-02-09', 110, 'cerrado'),
('PE011', 'CL011', 'TR006', 950, 500, '2026-02-11', 111, 'abierto'),
('PE012', 'CL012', 'TR006', 480, 420, '2026-02-13', 112, 'en_fab'),
('PE013', 'CL013', 'TR007', 1300, 900, '2026-02-15', 113, 'abierto'),
('PE014', 'CL014', 'TR007', 520, 300, '2026-02-17', 114, 'abierto'),
('PE015', 'CL015', 'TR008', 780, 780, '2026-02-19', 115, 'cerrado'),
('PE016', 'CL016', 'TR008', 860, 500, '2026-02-21', 116, 'en_fab'),
('PE017', 'CL017', 'TR001', 1400, 1000, '2026-02-23', 117, 'abierto'),
('PE018', 'CL018', 'TR002', 350, 200, '2026-02-25', 118, 'abierto'),
('PE019', 'CL019', 'TR003', 620, 620, '2026-02-27', 119, 'cerrado'),
('PE020', 'CL020', 'TR004', 910, 450, '2026-03-01', 120, 'en_fab');

-- ============================================
-- UNIDADES
-- ============================================
INSERT INTO unidad (id_producto, id_pedido, tipo, distribuidor, fase_actual)
VALUES
('PR001', 'PE001', 'caja', 'DIST01', 2),
('PR002', 'PE001', 'caja', 'DIST01', 3),
('PR003', 'PE001', 'palet', 'DIST02', 1),
('PR004', 'PE002', 'rollo', 'DIST03', 4),
('PR005', 'PE002', 'rollo', 'DIST03', 4),
('PR006', 'PE003', 'lamina', 'DIST02', 2),
('PR007', 'PE003', 'lamina', 'DIST02', 2),
('PR008', 'PE004', 'panel', 'DIST04', 1),
('PR009', 'PE004', 'panel', 'DIST04', 2),
('PR010', 'PE005', 'caja', 'DIST01', 3),
('PR011', 'PE005', 'caja', 'DIST01', 2),
('PR012', 'PE006', 'rollo', 'DIST03', 5),
('PR013', 'PE006', 'rollo', 'DIST03', 5),
('PR014', 'PE007', 'lamina', 'DIST02', 1),
('PR015', 'PE007', 'lamina', 'DIST02', 2),
('PR016', 'PE008', 'panel', 'DIST04', 1),
('PR017', 'PE008', 'panel', 'DIST04', 2),
('PR018', 'PE009', 'caja', 'DIST05', 3),
('PR019', 'PE009', 'caja', 'DIST05', 3),
('PR020', 'PE010', 'rollo', 'DIST03', 5),
('PR021', 'PE010', 'rollo', 'DIST03', 5),
('PR022', 'PE011', 'lamina', 'DIST02', 1),
('PR023', 'PE011', 'lamina', 'DIST02', 2),
('PR024', 'PE012', 'panel', 'DIST04', 2),
('PR025', 'PE012', 'panel', 'DIST04', 3),
('PR026', 'PE013', 'caja', 'DIST01', 2),
('PR027', 'PE013', 'palet', 'DIST05', 1),
('PR028', 'PE014', 'rollo', 'DIST03', 2),
('PR029', 'PE014', 'rollo', 'DIST03', 3),
('PR030', 'PE015', 'panel', 'DIST04', 5),
('PR031', 'PE015', 'panel', 'DIST04', 5),
('PR032', 'PE016', 'caja', 'DIST01', 2),
('PR033', 'PE016', 'caja', 'DIST01', 1),
('PR034', 'PE017', 'palet', 'DIST05', 2),
('PR035', 'PE017', 'palet', 'DIST05', 3),
('PR036', 'PE018', 'lamina', 'DIST02', 1),
('PR037', 'PE018', 'lamina', 'DIST02', 2),
('PR038', 'PE019', 'rollo', 'DIST03', 5),
('PR039', 'PE019', 'rollo', 'DIST03', 5),
('PR040', 'PE020', 'panel', 'DIST04', 2);

-- ============================================
-- ESTACIONES
-- ============================================
INSERT INTO estacion (id_estacion, nombre, zona)
VALUES ('ES01', 'Estacion unica');
('ZN01', 'ES01', 'plegado'),
('ZN02', 'ES01', 'prensado'),
('ZN03', 'ES01', 'etiquetado');

-- ============================================
-- SUPERVISORES
-- ============================================
INSERT INTO supervisor (codigo_empleado, id_estacion, nombre, turno)
VALUES
('SP001', 'ES01', 'Mario Ruiz', 1),
('SP002', 'ES02', 'Sara Molina', 2),
('SP003', 'ES03', 'Luis Vega', 1),
('SP004', 'ES04', 'Elena Diaz', 3),
('SP005', 'ES05', 'Carlos Sanz', 2),
('SP006', 'ES06', 'Nuria Prieto', 1),
('SP007', 'ES01', 'Jorge Gil', 2),
('SP008', 'ES02', 'Irene Lara', 3),
('SP009', 'ES03', 'Hugo Rey', 2),
('SP010', 'ES04', 'Marta Cano', 1);

-- ============================================
-- SE REALIZA EN
-- ============================================
INSERT INTO se_realiza_en (id_producto, id_estacion, hora_ini, hora_fin)
VALUES
('PR001', 'ES01', '2026-01-11', '2026-01-12'),
('PR002', 'ES02', '2026-01-11', '2026-01-13'),
('PR003', 'ES03', '2026-01-12', '2026-01-14'),
('PR004', 'ES04', '2026-01-12', '2026-01-15'),
('PR005', 'ES05', '2026-01-13', '2026-01-15'),
('PR006', 'ES06', '2026-01-13', '2026-01-16'),
('PR007', 'ES01', '2026-01-14', '2026-01-16'),
('PR008', 'ES02', '2026-01-14', '2026-01-17'),
('PR009', 'ES03', '2026-01-15', '2026-01-18'),
('PR010', 'ES04', '2026-01-16', '2026-01-19'),
('PR011', 'ES05', '2026-01-16', '2026-01-20'),
('PR012', 'ES06', '2026-01-17', '2026-01-20'),
('PR013', 'ES01', '2026-01-18', '2026-01-21'),
('PR014', 'ES02', '2026-01-18', '2026-01-22'),
('PR015', 'ES03', '2026-01-19', '2026-01-22'),
('PR016', 'ES04', '2026-01-20', '2026-01-23'),
('PR017', 'ES05', '2026-01-20', '2026-01-24'),
('PR018', 'ES06', '2026-01-21', '2026-01-24'),
('PR019', 'ES01', '2026-01-22', '2026-01-25'),
('PR020', 'ES02', '2026-01-22', '2026-01-26'),
('PR021', 'ES03', '2026-01-23', '2026-01-26'),
('PR022', 'ES04', '2026-01-24', '2026-01-27'),
('PR023', 'ES05', '2026-01-24', '2026-01-28'),
('PR024', 'ES06', '2026-01-25', '2026-01-28'),
('PR025', 'ES01', '2026-01-26', '2026-01-29'),
('PR026', 'ES02', '2026-01-26', '2026-01-30'),
('PR027', 'ES03', '2026-01-27', '2026-01-30'),
('PR028', 'ES04', '2026-01-28', '2026-01-31'),
('PR029', 'ES05', '2026-01-28', '2026-02-01'),
('PR030', 'ES06', '2026-01-29', '2026-02-01');