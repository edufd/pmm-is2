-- Role: pmm

CREATE ROLE pmm LOGIN
  ENCRYPTED PASSWORD 'md5976ab57e46a152b86083967bd03cadf8'
  SUPERUSER INHERIT CREATEDB CREATEROLE REPLICATION;


-- Database: pmm

CREATE DATABASE pmm
  WITH OWNER = pmm
       ENCODING = 'SQL_ASCII'
       TABLESPACE = pg_default
       LC_COLLATE = 'es_PY.UTF-8'
       LC_CTYPE = 'es_PY.UTF-8'
       CONNECTION LIMIT = -1;


-- Schema: pmm

CREATE SCHEMA pmm
  AUTHORIZATION pmm;


-- Database: pmm_produccion

CREATE DATABASE pmm_produccion
  WITH OWNER = pmm
       ENCODING = 'SQL_ASCII'
       TABLESPACE = pg_default
       LC_COLLATE = 'es_PY.UTF-8'
       LC_CTYPE = 'es_PY.UTF-8'
       CONNECTION LIMIT = -1;



