--Tv Chat
--F1
INSERT INTO pmm.des_relacion VALUES (1,1,2,'PADRE-HIJO',1,TRUE);
INSERT INTO pmm.des_relacion VALUES (2,2,3,'PADRE-HIJO',1,TRUE);
INSERT INTO pmm.des_relacion VALUES (3,2,4,'PADRE-HIJO',1,TRUE);
INSERT INTO pmm.des_relacion VALUES (4,2,5,'ANTECESOR-SUCESOR',1,TRUE);
--F2
INSERT INTO pmm.des_relacion VALUES (5,5,6,'PADRE-HIJO',2,TRUE);
INSERT INTO pmm.des_relacion VALUES (6,6,7,'ANTECESOR-SUCESOR',2,TRUE);
--F3
INSERT INTO pmm.des_relacion VALUES (7,7,8,'PADRE-HIJO',3,TRUE);
INSERT INTO pmm.des_relacion VALUES (8,7,9,'PADRE-HIJO',3,TRUE);
INSERT INTO pmm.des_relacion VALUES (9,9,10,'ANTECESOR-SUCESOR',3,TRUE);
--F4
INSERT INTO pmm.des_relacion VALUES (10,10,11,'PADRE-HIJO',4,TRUE);
INSERT INTO pmm.des_relacion VALUES (11,10,12,'PADRE-HIJO',4,TRUE);
--Ruleta Millonaria
--F1
INSERT INTO pmm.des_relacion VALUES (12,13,14,'PADRE-HIJO',5,TRUE);
--F2
INSERT INTO pmm.des_relacion VALUES (13,15,16,'PADRE-HIJO',6,TRUE);
--Tragamonedas
--F1
INSERT INTO pmm.des_relacion VALUES (14,18,19,'PADRE-HIJO',8,TRUE);
INSERT INTO pmm.des_relacion VALUES (15,19,20,'PADRE-HIJO',8,TRUE);
INSERT INTO pmm.des_relacion VALUES (16,20,21,'PADRE-HIJO',8,TRUE);
INSERT INTO pmm.des_relacion VALUES (17,20,22,'PADRE-HIJO',8,TRUE);
INSERT INTO pmm.des_relacion VALUES (18,20,23,'ANTECESOR-SUCESOR',8,TRUE);
--F2
INSERT INTO pmm.des_relacion VALUES (19,23,24,'PADRE-HIJO',9,TRUE);
INSERT INTO pmm.des_relacion VALUES (20,24,25,'PADRE-HIJO',9,TRUE);
INSERT INTO pmm.des_relacion VALUES (21,24,26,'PADRE-HIJO',9,TRUE);

SELECT setval('pmm.des_relacion_id_seq', 22, false);