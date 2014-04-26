--usuario administrador
INSERT INTO pmm.auth_group_permissions VALUES (1, 1, 1);
INSERT INTO pmm.auth_group_permissions VALUES (2, 1, 2);
INSERT INTO pmm.auth_group_permissions VALUES (3, 1, 3);
INSERT INTO pmm.auth_group_permissions VALUES (4, 1, 4);
INSERT INTO pmm.auth_group_permissions VALUES (5, 1, 5);
INSERT INTO pmm.auth_group_permissions VALUES (6, 1, 6);
--usuario lider de proyecto
INSERT INTO pmm.auth_group_permissions VALUES (7, 2, 1);
INSERT INTO pmm.auth_group_permissions VALUES (8, 2, 2);
INSERT INTO pmm.auth_group_permissions VALUES (9, 2, 3);
INSERT INTO pmm.auth_group_permissions VALUES (10, 2, 4);
INSERT INTO pmm.auth_group_permissions VALUES (11, 2, 5);
INSERT INTO pmm.auth_group_permissions VALUES (12, 2, 6);
--setear al siguiente valor siguiente de la secuencia
SELECT setval('pmm.auth_group_permissions_id_seq',13, false);