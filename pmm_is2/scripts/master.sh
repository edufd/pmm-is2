#!/bin/bash

./cargar_tablas.sh
#levantar los servidores
/usr/bin/python ../../manage.py runserver 9000 --settings=pmm_is2.settings.production_settings &
/usr/bin/python ../../manage.py runserver 8000 --settings=pmm_is2.settings.development_settings &

#abrir firefox
/usr/bin/firefox http://127.0.0.1:8000 &
/usr/bin/firefox http://127.0.0.1:9000 &