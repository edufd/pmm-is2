#!/bin/bash

#Servidor de Desarrollo
echo cargando tablas
psql -U postgres -h 127.0.0.1 < ../sql/crear_bases_de_datos.sql
psql -U pmm -h 127.0.0.1 -d pmm < ../sql/crear_schema.sql
#por si hay se levanta todos por primera vez
/usr/bin/python ../../manage.py syncdb
#/usr/bin/python ../../manage.py syncdb --database=produccion

psql -U pmm -h 127.0.0.1 -d pmm < ../sql/truncar_tablas.sql
psql -U pmm -h 127.0.0.1 -d pmm < ../sql/crear_django_content_type.sql
psql -U pmm -h 127.0.0.1 -d pmm < ../sql/crear_permisos.sql
psql -U pmm -h 127.0.0.1 -d pmm < ../sql/crear_roles.sql
psql -U pmm -h 127.0.0.1 -d pmm < ../sql/crear_usuario_administrador.sql
psql -U pmm -h 127.0.0.1 -d pmm < ../sql/crear_usuario_grupo.sql
psql -U pmm -h 127.0.0.1 -d pmm < ../sql/crear_roles_permisos.sql
psql -U pmm -h 127.0.0.1 -d pmm < ../sql/crear_usuario_perfil.sql
psql -U pmm -h 127.0.0.1 -d pmm < ../sql/crear_proyecto.sql
psql -U pmm -h 127.0.0.1 -d pmm < ../sql/crear_fase.sql
psql -U pmm -h 127.0.0.1 -d pmm < ../sql/crear_comite.sql
psql -U pmm -h 127.0.0.1 -d pmm < ../sql/crear_comite.sql
psql -U pmm -h 127.0.0.1 -d pmm < ../sql/crear_comite_usuario.sql
#nuevos scripts
psql -U pmm -h 127.0.0.1 -d pmm < ../sql/crear_fase_grupo.sql
psql -U pmm -h 127.0.0.1 -d pmm < ../sql/crear_tipos_items.sql
psql -U pmm -h 127.0.0.1 -d pmm < ../sql/crear_atributos_tipos_items.sql
psql -U pmm -h 127.0.0.1 -d pmm < ../sql/crear_fase_tipos_items.sql
psql -U pmm -h 127.0.0.1 -d pmm < ../sql/crear_triggers_funciones.sql

psql -U pmm -h 127.0.0.1 -d pmm < ../sql/crear_tipo.sql
psql -U pmm -h 127.0.0.1 -d pmm < ../sql/crear_opciones.sql


#Servidor de Produccion
#echo cargando tablas
#psql -U pmm -h 127.0.0.1 -d pmm_produccion < ../sql/crear_schema.sql
#psql -U pmm -h 127.0.0.1 -d pmm_produccion < ../sql/truncar_tablas.sql
#psql -U pmm -h 127.0.0.1 -d pmm_produccion < ../sql/crear_django_content_type.sql
#psql -U pmm -h 127.0.0.1 -d pmm_produccion < ../sql/crear_permisos.sql
#psql -U pmm -h 127.0.0.1 -d pmm_produccion < ../sql/crear_roles.sql
#psql -U pmm -h 127.0.0.1 -d pmm_produccion < ../sql/crear_usuario_administrador.sql
#psql -U pmm -h 127.0.0.1 -d pmm_produccion < ../sql/crear_usuario_grupo.sql
#psql -U pmm -h 127.0.0.1 -d pmm_produccion < ../sql/crear_roles_permisos.sql
#psql -U pmm -h 127.0.0.1 -d pmm_produccion < ../sql/crear_usuario_perfil.sql
#psql -U pmm -h 127.0.0.1 -d pmm_produccion < ../sql/crear_proyecto.sql
#psql -U pmm -h 127.0.0.1 -d pmm_produccion < ../sql/crear_fase.sql

#levantar el servidor
#/usr/bin/python ../../manage.py runserver 9000