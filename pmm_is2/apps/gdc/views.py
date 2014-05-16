from django.shortcuts import render
from django import forms
from pmm_is2.apps.gdc.models import Solicitud
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext

from pmm_is2.apps.gdc.forms import SolicitudForm
from pmm_is2.apps.gdc.forms import SolicitudRecibidoForm
from django.http import HttpResponseRedirect
from django.http import HttpResponse, HttpResponseRedirect
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet


from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont

@login_required
def index(request):
    context = RequestContext(request)
    return render_to_response('gdc/index.html', context)

def crear_solicitud(request):
    """Funcion para Crear Solicitud.
    Retorna la pagina correspondiente con el formulario para la creacion de la Solicitud

    :param request: Parametro a ser procesado.
    :type request: HttpRequest.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """
    context = RequestContext(request)
    creado = False
    if request.method == 'POST':
        solicitud_form = SolicitudForm(data=request.POST)
        if solicitud_form.is_valid():
            solicitud = solicitud_form.save()
            solicitud.save()
            creado = True
        else:
            print solicitud_form.errors

    else:
        solicitud_form = SolicitudForm()

    return render_to_response('gdc/crear_solicitud.html',
                              {
                                  'solicitud_form':solicitud_form,
                                  'creado': creado,
                              },
                              context
    )


def get_listar_solicitud():
    lista_solicitud = Solicitud.objects.filter(estado='EN-ESPERA')
    return lista_solicitud


@login_required
def listar_solicitud(request):
    context = RequestContext(request)
    lista_solicitud = get_listar_solicitud()
    context_dict = {}
    context_dict['lista_solicitud'] = lista_solicitud

    return render_to_response('gdc/lista_solicitud.html', context_dict, context)


@login_required
def editar_solicitud(request, pk):
    """Funcion para Modificar un Tipo Item.
    Retorna la pagina con el formulario correspondiente para la modificacion
    del Tipo Item.

    :param request: Parametro a ser procesado.
    :param pk: Parametro a ser procesado el identificador del tipo de Item que va a modificarse.
    :type request: HttpRequest.
    :type pk: int.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """
    context = RequestContext(request)
    solicitud = get_object_or_404(Solicitud, pk=pk)
    solicitud_form = SolicitudForm(request.POST or None, instance=solicitud)
    if solicitud_form.is_valid():
        solicitud_form.save()
        return redirect('listar_solicitud')

    return render_to_response('gdc/editar_solicitud.html', {'solicitud_form': solicitud_form}, context)

@login_required
def imprimir_solicitud(request, pk):
    """Funcion para Modificar un Tipo Item.
    Retorna la pagina con el formulario correspondiente para la modificacion
    del Tipo Item.

    :param request: Parametro a ser procesado.
    :param pk: Parametro a ser procesado el identificador del tipo de Item que va a modificarse.
    :type request: HttpRequest.
    :type pk: int.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """
    context = RequestContext(request)
    solicitud = get_object_or_404(Solicitud, pk=pk)
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'filename="Solicitud.pdf"'
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    style = ParagraphStyle(
 		name='Normal',
 		fontName='Helvetica-Bold',
 		fontSize=12,
 		alignment=TA_CENTER
 	)
    elements.append(Paragraph("SOLICITUD", style))
    elements.append(Spacer(1, 1 * cm))

    LEFTMARGIN = 1 * cm
    RIGHTMARGIN = 1 * cm
    TOPMARGIN = 1 * cm
    BOTTONMARGIN = 1 * cm

    COLOR_FONDO_CABECERA_1 = colors.blueviolet
    COLOR_TEXTO_CABECERA_1 = colors.white

    COLOR_FONDO_CABECERA_2 = colors.cadetblue
    COLOR_TEXTO_CABECERA_2 = colors.black

    COLOR_FONDO_CABECERA_3 = colors.gray
    COLOR_TEXTO_CABECERA_3 = colors.white

    ESTILO_GENERAL = [
    ('BOX', (0, 0), (-1, -1), 1.0, colors.black),
    ('GRID', (0, 0), (-1, -1), 1.0, colors.black),
    ('BACKGROUND', (0, 0), (-1, -1), colors.transparent),
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('LEFTPADDING', (0, 0), (-1, -1), 3),
    ('RIGHTPADDING', (0, 0), (-1, -1), 3),
    ]

    #data= [['comentarios','descripcion','nombre_linea_base','tipo']]
    data= [['fecha_inicio','nombre_proyecto','nombre_fase','nombre_item']]
    data.append([
            solicitud.fecha_inicio,
 			solicitud.nombre_proyecto,
 			solicitud.nombre_fase,
 			solicitud.nombre_item,
            #solicitud.usuario,
            #solicitud.estado,
            #solicitud.prioridad,
            #solicitud.comentarios,
            #solicitud.descripcion,
            #solicitud.nombre_linea_base,
 			#solicitud.tipo
 	])
    columnas = [100, 100, 100,100]
    t=Table(data, columnas)
    t.setStyle(ESTILO_GENERAL)

    t.setStyle([

    ('SPAN', (0, 0), (0, 0)),
    ('BACKGROUND', (0, 0), (0, 0), COLOR_FONDO_CABECERA_3),
    ('TEXTCOLOR', (0, 0), (0, 0), COLOR_TEXTO_CABECERA_3),
    ('FONTNAME', (0, 0), (0, 0), 'Helvetica'),
    ('FONTSIZE', (0, 0), (0, 0), 11),


    ('SPAN', (1, 0), (1, 0)),
    ('BACKGROUND', (1, 0), (1, 0), COLOR_FONDO_CABECERA_3),
    ('TEXTCOLOR', (1, 0), (1, 0), COLOR_TEXTO_CABECERA_3),
    ('FONTNAME', (1, 0), (1, 0), 'Helvetica'),
    ('FONTSIZE', (1, 0), (1, 0), 11),
    ('ALIGN', (1, 0), (1, 0), 'LEFT'),
    #('SPAN', (1, 0), (3, 3)),
    #('SPAN', (0, 3), (3, 3)),
    #('SPAN', (0, 4), (1, 4)),
     ])

    elements.append(t)

    elements.append(Spacer(0, 5))

    data1= [['usuario']]
    data1.append([
            solicitud.usuario,

 	])
    columnas1 = [100]



    t1=Table(data1, columnas1)
    t1.setStyle(ESTILO_GENERAL)
    elements.append(t1)

    doc.build(elements)
    response.write(buffer.getvalue())
    buffer.close()
    return response
    return render_to_response("gdc/index1.html", context_instance=RequestContext(request))


@login_required
def enviar_solicitud(request, pk):
    """Funcion para Modificar un Tipo Item.
    Retorna la pagina con el formulario correspondiente para la modificacion
    del Tipo Item.

    :param request: Parametro a ser procesado.
    :param pk: Parametro a ser procesado el identificador del tipo de Item que va a modificarse.
    :type request: HttpRequest.
    :type pk: int.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """
    context = RequestContext(request)
    solicitud = get_object_or_404(Solicitud, pk=pk)
    solicitud.estado='EN-PROCESO'
    solicitud.save()

    return render_to_response("gdc/enviar.html", context_instance=RequestContext(request))

def get_listar_solicitudRecibido():
    lista_solicitud = Solicitud.objects.filter(estado='EN-PROCESO')
    return lista_solicitud


@login_required
def listar_solicitudRecibido(request):
    context = RequestContext(request)
    lista_solicitud = get_listar_solicitudRecibido()
    context_dict = {}
    context_dict['lista_solicitud'] = lista_solicitud

    return render_to_response('gdc/lista_solicitudRecibido.html', context_dict, context)


@login_required
def editar_solicitudRecibido(request, pk):
    context = RequestContext(request)
    solicitud = get_object_or_404(Solicitud, pk=pk)
    solicitud_form = SolicitudRecibidoForm(request.POST or None, instance=solicitud)
    if request.method == 'POST':
        votar=request.POST.getlist('opciones')
        if votar[0]=='1':
            solicitud.contador =  solicitud.contador + 1
            solicitud.encontra=solicitud.encontra

        if votar[0]=='2':
            solicitud.encontra =  solicitud.encontra + 1
            solicitud.contador=solicitud.contador

        total=solicitud.contador+solicitud.encontra
        if total==3:
            solicitud.estado='RECHAZADA'
        if solicitud.contador==3:
            solicitud.estado='APROBADA'
        if solicitud.encontra==3:
            solicitud.estado='RECHAZADA'
        commen=request.POST.getlist('comentarios')
        solicitud.comentarios=commen[0]
        solicitud.save()
        return redirect('listar_solicitudRecibido')


    return render_to_response('gdc/editar_solicitudRecibido.html', {'solicitud_form': solicitud_form}, context)



