from pmm_is2.apps.adm.models import Proyecto


def get_project_list():
    project_list = Proyecto.objects.all().order_by('id_proyecto')
    return project_list