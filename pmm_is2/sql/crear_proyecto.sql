INSERT INTO pmm.adm_proyecto VALUES (1, 'Tv Chat', 'Proyecto x terminar', 3000000, 0, 0, 'INICIADO', 4, '2014-07-05','2014-08-20', 21, 2);
INSERT INTO pmm.adm_proyecto VALUES (2, 'Ruleta Millonaria', 'en ejecucion',3000000,0,0,'NO-INICIADO', 3, '2014-07-11','2014-09-28',21,2);
INSERT INTO pmm.adm_proyecto VALUES (3, 'Tragamonedas', 'Terminado',3000000,0,0,'FINALIZADO', 2, '2014-05-11','2014-07-05',21,2);
SELECT setval(' pmm.adm_proyecto_id_proyecto_seq', 4, false);
