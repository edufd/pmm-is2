#!/bin/bash

#tablas_a_insertar_1
echo cargando tablas
psql -U pmm -h 127.0.0.1 -d pmm < ../sql/crear_permisos.sql
