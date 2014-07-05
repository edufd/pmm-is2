--Tv Chat
--LB1
INSERT INTO pmm.gdc_lineabase_items VALUES (1,1,1);
INSERT INTO pmm.gdc_lineabase_items VALUES (2,1,2);
INSERT INTO pmm.gdc_lineabase_items VALUES (3,1,3);
INSERT INTO pmm.gdc_lineabase_items VALUES (4,1,4);
--LB2
INSERT INTO pmm.gdc_lineabase_items VALUES (5,2,5);
INSERT INTO pmm.gdc_lineabase_items VALUES (6,2,6);
--LB3
INSERT INTO pmm.gdc_lineabase_items VALUES (7,3,7);
INSERT INTO pmm.gdc_lineabase_items VALUES (8,3,8);
INSERT INTO pmm.gdc_lineabase_items VALUES (9,3,9);
--Tragamonedas
--LB1
INSERT INTO pmm.gdc_lineabase_items VALUES (10,4,18);
INSERT INTO pmm.gdc_lineabase_items VALUES (11,4,19);
INSERT INTO pmm.gdc_lineabase_items VALUES (12,4,20);
INSERT INTO pmm.gdc_lineabase_items VALUES (13,4,21);
--LB2
INSERT INTO pmm.gdc_lineabase_items VALUES (14,5,5);
INSERT INTO pmm.gdc_lineabase_items VALUES (15,5,6);
INSERT INTO pmm.gdc_lineabase_items VALUES (16,5,8);
INSERT INTO pmm.gdc_lineabase_items VALUES (17,5,9);

SELECT setval('pmm.gdc_lineabase_items_id_seq', 18, false);