--Tv Chat
INSERT INTO pmm.gdc_lineabase VALUES (1,'LB11','CERRADA',2,2,1);
INSERT INTO pmm.gdc_lineabase VALUES (2,'LB12','CERRADA',2,2,2);
INSERT INTO pmm.gdc_lineabase VALUES (3,'LB13','CERRADA',2,2,3);
--Tragamonedas
INSERT INTO pmm.gdc_lineabase VALUES (4,'LB31','CERRADA',2,4,8);
INSERT INTO pmm.gdc_lineabase VALUES (5,'LB32','CERRADA',2,4,9);

SELECT setval('pmm.gdc_lineabase_id_linea_base_seq', 6, false);