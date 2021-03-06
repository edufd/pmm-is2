/*create trigger after_insert_item
	after insert on pmm.des_item
	for each row execute procedure actualizar_version_item()*/

CREATE OR REPLACE FUNCTION pmm.actualizar_version_item()
  RETURNS trigger AS $$
	DECLARE

		v_ultimo_version_item_guardada record;

	BEGIN

		SELECT * INTO v_ultimo_version_item_guardada
		FROM pmm.des_item
		where id_item = new.id_item;

		/*select *
		from indice_mensajes_periodicos
		where id_promocion = 3 and tipo = 0
		order by 2 desc limit 1*/

		IF v_ultimo_version_item_guardada.id_item IS NOT NULL THEN

			RAISE NOTICE 'Nuevo item:[%]', new.id_item;

			/*UPDATE indice_mensajes_periodicos SET id_siguiente_contenido = new.id_mensaje_periodico
			WHERE id_contenido = v_ultimo_indice_guardado.id_contenido and id_promocion = new.id_promocion and tipo = new.tipo;*/

			RAISE NOTICE 'id_item:[%]', new.id_item;
			insert into pmm.des_versionitem (item_id, nombre_item,version_item, prioridad, estado, descripcion, numero, observaciones,
			complejidad, costo, ultima_version_item_id, id_tipo_item_id, id_fase_id, modificado_id, fecha_modificacion)
			values (new.id_item, new.nombre_item, new.version_item, new.prioridad, new.estado, new.descripcion, new.numero, new.observaciones,
			new.complejidad, new.costo, new.ultima_version_item_id, new.id_tipo_item_id, new.id_fase_id, new.modificado_id, new.fecha_modificacion);
			/*
				item_id integer NOT NULL,
				nombre_item character varying(200) NOT NULL,
				version_item integer NOT NULL,
				prioridad character varying(1) NOT NULL,
				estado character varying(1) NOT NULL,
				descripcion character varying(200) NOT NULL,
				observaciones character varying(5000) NOT NULL,
				complejidad integer NOT NULL,
				ultima_version_item_id integer NOT NULL,
				id_tipo_item_id integer NOT NULL,
				id_fase_id integer NOT NULL,

			    id_version_item = models.AutoField(primary_key=True)
			    item = models.ForeignKey(Item)
			    nombre_item = models.CharField(unique=False, max_length=200)
			    version_item = models.IntegerField(blank=True)
			    prioridad = models.CharField(max_length=1) #Alta:'A', Media:'M', Baja:'B'
			    estado = models.CharField(max_length=1) # I:Inactivo  B:Bloqueado C:Revision A:Aprobado D:Desaprobado
			    descripcion = models.CharField(max_length=200)
			    observaciones = models.CharField(max_length=5000)
			    complejidad = models.IntegerField(max_length=10)
			    ultima_version_item_id = models.IntegerField(blank=True)
			    id_tipo_item = models.ForeignKey(TipoItem, verbose_name="Tipo de Item")
			    id_fase = models.ForeignKey('adm.Fase', verbose_name="Fase")
			*/

		END IF;

		RETURN new;
	END;
	$$
	  LANGUAGE plpgsql VOLATILE
	  COST 100;
ALTER FUNCTION pmm.actualizar_version_item()
  OWNER TO pmm;


/*create trigger after_update_item
	after update on pmm.des_item
	for each row execute procedure agregar_version_item()*/

CREATE OR REPLACE FUNCTION pmm.agregar_version_item()
  RETURNS trigger AS $$
	DECLARE

		v_ultimo_version_item_guardada record;

	BEGIN

		SELECT * INTO v_ultimo_version_item_guardada
		FROM pmm.des_item
		where id_item = new.id_item;

		/*select *
		from indice_mensajes_periodicos
		where id_promocion = 3 and tipo = 0
		order by 2 desc limit 1*/

		IF v_ultimo_version_item_guardada.id_item IS NOT NULL THEN

			RAISE NOTICE 'Actualizar item:[%]', new.id_item;

			/*UPDATE indice_mensajes_periodicos SET id_siguiente_contenido = new.id_mensaje_periodico
			WHERE id_contenido = v_ultimo_indice_guardado.id_contenido and id_promocion = new.id_promocion and tipo = new.tipo;*/

			RAISE NOTICE 'id_item:[%]', new.id_item;
			insert into pmm.des_versionitem (item_id, nombre_item,version_item, prioridad, estado, descripcion, numero, observaciones,
			complejidad, costo, ultima_version_item_id, id_tipo_item_id, id_fase_id, modificado_id, fecha_modificacion)
			values (new.id_item, new.nombre_item, new.version_item, new.prioridad, new.estado, new.descripcion, new.numero, new.observaciones,
			new.complejidad, new.costo, new.ultima_version_item_id, new.id_tipo_item_id, new.id_fase_id, new.modificado_id, new.fecha_modificacion);

		END IF;

		RETURN new;
	END;
	$$
	  LANGUAGE plpgsql VOLATILE
	  COST 100;
ALTER FUNCTION pmm.agregar_version_item()
  OWNER TO pmm;



create trigger after_update_item
	after update on pmm.des_item
	for each row execute procedure pmm.agregar_version_item();

create trigger after_insert_item
	after insert on pmm.des_item
	for each row execute procedure pmm.actualizar_version_item();


/*create trigger after_update_linea_base
	after update on pmm.gdc_lineabase
	for each row execute procedure pmm.cerrar_fase()*/

/*CREATE OR REPLACE FUNCTION pmm.cerrar_fase()
  RETURNS trigger AS $$
	DECLARE

	BEGIN

		IF new.estado = 'FINALIZADA' THEN

			RAISE NOTICE 'Actualizar Fase:[%]', new.fase_id;

			UPDATE pmm.adm_fase SET estado_fase = 'FINALIZADA'
			WHERE id_fase = new.fase_id;

		END IF;

		RETURN new;
	END;
	$$
	  LANGUAGE plpgsql VOLATILE
	  COST 100;
ALTER FUNCTION pmm.cerrar_fase()
  OWNER TO pmm;


create trigger after_update_linea_base
	after update on pmm.gdc_lineabase
	for each row execute procedure pmm.cerrar_fase();
*/

CREATE OR REPLACE FUNCTION pmm.actualizar_estado_item()
  RETURNS trigger AS $$
	DECLARE

	BEGIN

		RAISE NOTICE 'Actualizar Item:[%]', new.item_id;
		UPDATE pmm.des_item SET estado = 'BLOQUEADO'
		WHERE id_item= new.item_id;

		RETURN new;
	END;
	$$
	  LANGUAGE plpgsql VOLATILE
	  COST 100;
ALTER FUNCTION pmm.actualizar_estado_item()
  OWNER TO pmm;

create trigger after_insert_linea_base_item
	after insert on pmm.gdc_lineabase_items
	for each row execute procedure pmm.actualizar_estado_item();

/*CREATE OR REPLACE FUNCTION pmm.actualizar_estado_fase()
  RETURNS trigger AS $$
	DECLARE

		v_ultimo_version_item_guardada record;

	BEGIN

		IF new.fase_id IS NOT NULL THEN

			RAISE NOTICE 'Nuevo linea base:[%]', new.fase_id;

			UPDATE pmm.adm_fase SET estado_fase = 'FINALIZADA'
			WHERE id_fase = new.fase_id;

		END IF;

		RETURN new;
	END;
	$$
	  LANGUAGE plpgsql VOLATILE
	  COST 100;
ALTER FUNCTION pmm.actualizar_estado_fase()
  OWNER TO pmm;

create trigger after_insert_item
	after insert on pmm.gdc_lineabase
	for each row execute procedure pmm.actualizar_estado_fase();

*/
CREATE OR REPLACE FUNCTION pmm.anhadir_lider_proyecto()
  RETURNS trigger AS $$

	BEGIN

		IF new.id_proyecto IS NOT NULL THEN

			RAISE NOTICE 'id_proyecto:[%]', new.id_proyecto;

			insert into pmm.adm_proyecto_miembros (proyecto_id, user_id)
			values (new.id_proyecto, new.lider_proyecto_id);

		END IF;

		RETURN new;
	END;
	$$
	  LANGUAGE plpgsql VOLATILE
	  COST 100;
ALTER FUNCTION pmm.anhadir_lider_proyecto()
  OWNER TO pmm;

create trigger after_insert_proyecto
	after insert on pmm.adm_proyecto
	for each row execute procedure pmm.anhadir_lider_proyecto();


CREATE OR REPLACE FUNCTION pmm.actualizar_lider_proyecto()
  RETURNS trigger AS $$

	BEGIN

		IF new.lider_proyecto_id IS NOT NULL THEN

			RAISE NOTICE 'id_proyecto:[%]', new.id_proyecto;

			UPDATE pmm.adm_proyecto_miembros SET user_id = new.lider_proyecto_id
			WHERE proyecto_id = old.lider_proyecto_id;

		END IF;

		RETURN new;
	END;
	$$
	  LANGUAGE plpgsql VOLATILE
	  COST 100;
ALTER FUNCTION pmm.actualizar_lider_proyecto()
  OWNER TO pmm;


create trigger after_update_proyecto
	after update on pmm.adm_proyecto
	for each row execute procedure pmm.actualizar_lider_proyecto();