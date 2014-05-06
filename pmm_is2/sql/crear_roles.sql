INSERT INTO pmm.auth_group VALUES (1, 'Administrador');
INSERT INTO pmm.auth_group VALUES (2, 'Lider de Proyecto');
INSERT INTO pmm.auth_group VALUES (3, 'Desarrollador');
SELECT setval('pmm.auth_group_id_seq',4, false);