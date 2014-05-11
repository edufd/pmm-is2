INSERT INTO pmm.adm_comite VALUES (1, 1);
INSERT INTO pmm.adm_comite VALUES (2, 2);
INSERT INTO pmm.adm_comite VALUES (3, 3);
SELECT setval('pmm.adm_comite_id_comite_seq', 4, false);
