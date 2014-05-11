--usuario administrador
INSERT INTO pmm.auth_user_groups VALUES (1, 1, 1);
INSERT INTO pmm.auth_user_groups VALUES (2, 2, 1);
INSERT INTO pmm.auth_user_groups VALUES (3, 3, 1);
INSERT INTO pmm.auth_user_groups VALUES (4, 4, 1);
--usuario lider de proyecto
INSERT INTO pmm.auth_user_groups VALUES (5, 1, 2);
INSERT INTO pmm.auth_user_groups VALUES (6, 2, 2);
INSERT INTO pmm.auth_user_groups VALUES (7, 3, 2);
INSERT INTO pmm.auth_user_groups VALUES (8, 4, 2);
SELECT setval('pmm.auth_user_groups_id_seq', 9, false);

