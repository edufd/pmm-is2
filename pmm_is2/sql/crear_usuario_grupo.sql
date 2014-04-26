--usuario administrador
INSERT INTO pmm.auth_user_groups VALUES (1, 1, 1);
--usuario lider de proyecto
INSERT INTO pmm.auth_user_groups VALUES (2, 1, 2);
SELECT setval('pmm.auth_user_groups_id_seq',3, false);

