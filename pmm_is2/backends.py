__author__ = 'adriana'

from pmm_is2.apps.adm import SESSION_KEY
from django.contrib.auth.models import User, Group, Permission
from pmm_is2.apps.adm import SESSION_KEY_MSG


def iniciar_sesion(request, usuario):
    if usuario is None:
        usuario = request.user
    if SESSION_KEY in request.session:
        if request.session[SESSION_KEY] != usuario.username:
            request.session.flush()
    else:
        request.session.cycle_key()
        request.session[SESSION_KEY] = usuario.username
        request.session[SESSION_KEY_MSG] = ["hola"]
    if hasattr(request, 'user'):
        request.user = usuario


def cerrar_sesion(request):
    request.session.flush()
    if hasattr(request, 'user'):
        request.user = None


    #def usuario_verificarRolUsuario(request):
    #   valido = False
    #    alias=request.session[SESSION_KEY]
    #  print alias
    #  UsuarioId = User.objects.get(username=alias)
    # valido=UsuarioId.has_perm ('adm.add_user')
    # return valido


def verificar_rol_usuario(user):
    valido = False
    if user:
        combined_queryset = user.groups.filter(name='Administrador').exists() |\
                            user.groups.filter(name='Lider de Proyecto').exists()
        valido = combined_queryset
    return valido

def calcular_impacto_item(item):
    """
    Retorna el impacto calculado correspondiente al item.
    @type item: item
    @param item: el item cuyo impacto se desea calcular
    @rtype: int
    @return: retorna el valor calculado del impacto del item
    """

    impacto_item = 0

    item_relacionados = obtener_item_relacionados(item)

    for item_relacionado in item_relacionados:
        impacto_item = impacto_item + item_relacionado.complejidad

    impacto_item = impacto_item + item.complejidad

    return impacto_item

def obtener_item_relacionados(item):
    item_encontrados = set()
    item_revisados = set()
    item_encontrados.add(item)


    while len(item_encontrados)>0:
        item_actual = item_encontrados.pop()

        if item_actual.id_item != item.id_item:
            item_revisados.add(item_actual)

        #Padres del item
        relaciones_padre_hijo = RelacionPadreHijo.objects.filter(id_item_hijo=item_actual.id_item).filter(relacion_valida=True)
        item_padres = set()

        for relacion_padre_hijo in relaciones_padre_hijo:
            item_padres.add(item_padre_hijo.id_item_padre)

        for item_padre in item_padres:
            if item_padre not in item_encontrados and item_padre not in item_revisados:
                item_encontrados.add(item_padre)

        #Hijos del item
        relaciones_hijo_padre = RelacionPadreHijo.objects.filter(id_item_padre=item_actual.id_item).filter(relacion_valida=True)
        item_hijos = set()

        for relacion_hijo_padre in relaciones_hijo_padre :
            item_hijos.add(relacion_hijo_padre.id_item_hijo)

        for item_hijo in item_hijos:
            if item_hijo not in item_encontrados and item_hijo not in item_revisados:
                item_encontrados.add(item_hijo)

        #Antecesores del item
        relaciones_item_fase_anterior = RelacionItemFaseAnterior.objects.filter(id_item_fase_actual=item_actual.id_item).filter(relacion_valida=True)
        item_antecesores = set()

        for relacion_item_fase_anterior in relaciones_item_fase_anterior :
            item_antecesores.add(relacion_item_fase_anterior.id_item_fase_anterior)

        for item_antecesor in item_antecesores:
            if item_antecesor not in item_encontrados and item_antecesor not in item_revisados:
                item_encontrados.add(item_antecesor)

        #Sucesores del item
        relaciones_fase_anterior_item = RelacionItemFaseAnterior.objects.filter(id_item_fase_anterior=item_actual.id_item).filter(relacion_valida=True)
        item_sucesores = set()

        for relacion_fase_anterior_item in relaciones_fase_anterior_item :
            item_sucesores.add(relacion_fase_anterior_item.id_item_fase_actual)

        for item_sucesor in item_sucesores:
            if item_sucesor not in item_encontrados and item_sucesor not in item_revisados:
                item_encontrados.add(item_sucesor)

    return  item_revisados