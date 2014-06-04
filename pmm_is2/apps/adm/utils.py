from django.contrib.auth.models import User, Group, Permission
from pmm_is2.apps.adm.models import Proyecto, Fase, Comite


def get_project_list():
    project_list = Proyecto.objects.all().order_by('id_proyecto')
    return project_list


def get_user_list(user_id):
    """Funcion para Listar un Usuarios.
        Retorna la pagina correspondiente con la lista de usuarios

        :param pk: Parametro a ser procesado. Identificador del usuario
        :type request: HttpRequest.
        :returns: La pagina correspondiente.
        :rtype: El response correspondiente.
        """

    #join quilombo trae todos los elementos de las dos relaciones
    user_list = User.objects.exclude(id=user_id).select_related("userprofile").all().order_by('id')

    return user_list


def get_group_list():

    group_list = Group.objects.all().order_by('id')
    return group_list


def get_category_list(max_results=0, starts_with=''):
        cat_list = []
        if starts_with:
            starts_with = starts_with + '%'
            cat_list = User.objects.filter(username__ilike=starts_with)
        # else:
        #         cat_list = User.objects.all()
        #
        # print cat_list

        if max_results > 0:
                if len(cat_list) > max_results:
                        cat_list = cat_list[:max_results]

        return cat_list


def get_roles_list(max_results=0, starts_with=''):
        cat_list = []
        if starts_with:
            starts_with = starts_with + '%'
            cat_list = Group.objects.filter(name__ilike=starts_with)
        # else:
        #         cat_list = User.objects.all()
        #
        # print cat_list

        if max_results > 0:
                if len(cat_list) > max_results:
                        cat_list = cat_list[:max_results]

        return cat_list


#busca el texto ingresado en permisos
def get_permisos_list(max_results=0, starts_with=''):
        cat_list = []
        if starts_with:
            starts_with = starts_with + '%'
            cat_list = Permission.objects.filter(name__ilike=starts_with)
        # else:
        #         cat_list = User.objects.all()
        #
        # print cat_list

        if max_results > 0:
                if len(cat_list) > max_results:
                        cat_list = cat_list[:max_results]

        return cat_list


#busca el texto ingresado en proyectos
def get_proyectos_list(max_results=0, starts_with=''):
        cat_list = []
        if starts_with:
            starts_with = starts_with + '%'
            cat_list = Proyecto.objects.filter(nombre_proyecto__ilike=starts_with)
        # else:
        #         cat_list = User.objects.all()
        #
        # print cat_list

        if max_results > 0:
                if len(cat_list) > max_results:
                        cat_list = cat_list[:max_results]

        return cat_list


#busca el texto ingresado en fases
def get_phases_list(pk):
    phases_list = Fase.objects.filter(proyecto_id=pk).order_by('numero_secuencia')
    return phases_list


#busca el texto ingresado en comites
def get_comite_list():
    comite_list = Comite.objects.all()
    return comite_list


#edu me dijo que va a usar
def encode_url(name):
    return name.replace(' ', '_')


def decode_url(url):
    return url.replace('_', ' ')
