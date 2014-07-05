--Tv Chat
INSERT INTO pmm.adm_fase VALUES (1, 1, 'FASE 1','Analisis de Requerimientos','FINALIZADA', 1);
INSERT INTO pmm.adm_fase VALUES (2, 1, 'FASE 2','Analisis de Requerimientos','FINALIZADA', 2);
INSERT INTO pmm.adm_fase VALUES (3, 1, 'FASE 3','Analisis de Requerimientos','FINALIZADA', 3);
INSERT INTO pmm.adm_fase VALUES (4, 1, 'FASE 4','Analisis de Requerimientos','NO-INICIADA', 4);
--Ruleta Millonaria
INSERT INTO pmm.adm_fase VALUES (5, 2, 'Analisis','Analisis de Requerimientos','ABIERTA',1);
INSERT INTO pmm.adm_fase VALUES (6, 2, 'Disenho','Analisis de Requerimientos','NO-INICIADA',2);
INSERT INTO pmm.adm_fase VALUES (7, 2, 'Desarrollo','Analisis de Requerimientos','NO-INICIADA',3);
--Tragamonedas
INSERT INTO pmm.adm_fase VALUES (8, 3, 'Fase 1','Analisis de Requerimientos','FINALIZADA',1);
INSERT INTO pmm.adm_fase VALUES (9, 3, 'Fase 2','Analisis de Requerimientos','FINALIZADA',2);
SELECT setval(' pmm.adm_fase_id_fase_seq', 10, false);
