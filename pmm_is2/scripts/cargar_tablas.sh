#!/bin/bash

#por si hay se levanta todo por primera vez
/usr/bin/python ../../manage.py syncdb

#tablas_a_insertar_1
echo cargando tablas
psql -U pmm -h 127.0.0.1 -d pmm < ../sql/truncar_tablas.sql
psql -U pmm -h 127.0.0.1 -d pmm < ../sql/crear_django_content_type.sql
psql -U pmm -h 127.0.0.1 -d pmm < ../sql/crear_permisos.sql
psql -U pmm -h 127.0.0.1 -d pmm < ../sql/crear_roles.sql
psql -U pmm -h 127.0.0.1 -d pmm < ../sql/crear_usuario_administrador.sql
psql -U pmm -h 127.0.0.1 -d pmm < ../sql/crear_usuario_grupo.sql
psql -U pmm -h 127.0.0.1 -d pmm < ../sql/crear_roles_permisos.sql

#levantar el servidor
/usr/bin/python ../../manage.py syncdb
/usr/bin/python ../../manage.py runserver 9000