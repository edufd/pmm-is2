INSERT INTO pmm.adm_userprofile VALUES (1, 1, 'PMM', 'Administrador', 1, 1);
INSERT INTO pmm.adm_userprofile VALUES (2, 2, 'Derlis Ariel', 'Arguello Sosa', 4476360, 301739);
INSERT INTO pmm.adm_userprofile VALUES (3, 3, 'Eduardo', 'Florencio', 2, 2);
INSERT INTO pmm.adm_userprofile VALUES (4, 4, 'Adriana', 'Torales',3, 3 );
SELECT setval('pmm.adm_userprofile_id_seq', 5, false);
