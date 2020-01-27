# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from .models import Notificacion

def profile(request):
    current_url = request.resolver_match.url_name
    if current_url!="login" and request.path != "/":
        profile=request.user.perfil_usuario
        return {'profile': profile}
    else:
        return {}

def menu(request):
    MENU={'menu':[]}
    url_actual=request.path
    try:
        cat=request.user.perfil_usuario.categoria.nombre
    except:
        cat="anonimo"
    menu_dict={'menu':[
            {'name':'Inicio','url':reverse('inicio'),'icon':'glyphicon glyphicon-home','visible':['administrador','especialista','invitado','organismo','dpts', 'dpt_ee', 'dmt']},

            # VOLVER A PONER
            {'name':'Movimiento Laboral','url':reverse('movimiento_laboral'),'icon':'glyphicon glyphicon-briefcase','visible':['administrador','especialista','invitado','organismo','dpts'],
               'menu':[
                    {'name':'Pendientes','url':reverse('pendientes'),'icon':'glyphicon glyphicon-chevron-right','visible':['administrador','especialista','invitado','organismo']},
                    {'name':'Rechazados','url':reverse('rechazados'),'icon':'glyphicon glyphicon-chevron-right','visible':['administrador','especialista','invitado','organismo']},
                    {'name':'No Aprobados','url':reverse('no_aprobados'),'icon':'glyphicon glyphicon-chevron-right','visible':['administrador','especialista','invitado','organismo']},
                    {'name':'Aprobados','url':reverse('aprobados'),'icon':'glyphicon glyphicon-chevron-right','visible':['administrador','especialista','invitado','organismo','dpts']},
                    {'name':'Gestión de Externos','url':reverse('expedientes'),'icon':'glyphicon glyphicon-chevron-right','visible':['administrador','especialista']},
                    {'name':'Gestión de Internos','url':reverse('movimientos_internos'),'icon':'glyphicon glyphicon-chevron-right','visible':['administrador','especialista','organismo']},
                    {'name':'Registrar Expediente','url':reverse('registrar_expediente_estandar'),'icon':'glyphicon glyphicon-chevron-right','visible':['organismo']},
               ]
             },

            # VOLVER A PONER
            {'name':'Ubicación Laboral','url':reverse('ubicacion_laboral'),'icon':'glyphicon glyphicon-briefcase','visible':['administrador','especialista','organismo','dpts','mes'],
              'menu':[
                  {'name':'Disponibles','url':reverse('disponibles'),'icon':'glyphicon glyphicon-chevron-right','visible':['administrador','especialista','dpts','mes']},
                  {'name':'Ubicados','url':reverse('ubicados'),'icon':'glyphicon glyphicon-chevron-right','visible':['administrador','especialista','organismo','dpts','mes']},
              ]
             },
            {'name':'Inhabilitaciones','url':reverse('inhabilitaciones'),'icon':'glyphicon glyphicon-briefcase','visible':['administrador','juridico']},

            # ---------------codigo de daniel (INICIO)---------------
            {'name': 'Empleo Estatal', 'url': reverse('menu_empleo_estatal'), 'icon': 'glyphicon glyphicon-briefcase','visible': ['administrador', 'dpt_ee', 'dmt'],
             'menu': [
                 {'name': 'Licenciados del SMA', 'url': reverse('listar_licenciados_sma'), 'icon': 'glyphicon glyphicon-chevron-right', 'visible': ['administrador', 'especialista', 'dpt_ee', 'dmt']},
                 {'name': 'Egresados de EP y Sancionados', 'url': reverse('listar_egresados_establecimientos_penitenciarios'), 'icon': 'glyphicon glyphicon-chevron-right', 'visible': ['administrador', 'especialista', 'dpt_ee', 'dmt']},
                 {'name': 'Desvinculados', 'url': reverse('listar_desvinculados'), 'icon': 'glyphicon glyphicon-chevron-right', 'visible': ['administrador', 'especialista', 'dpt_ee', 'dmt']},
                 {'name': 'Técnicos medios, Obreros calificados y Escuelas de oficio', 'url': reverse('listar_tm_oc_eo'), 'icon': 'glyphicon glyphicon-chevron-right', 'visible': ['administrador', 'especialista', 'dpt_ee', 'dmt']},
                 {'name': 'Egresados de escuelas especiales', 'url': reverse('listar_egresados_escuelas_especiales'), 'icon': 'glyphicon glyphicon-chevron-right', 'visible': ['administrador', 'especialista', 'dpt_ee', 'dmt']},
                 {'name': 'Egresados de escuelas de conducta', 'url': reverse('listar_egresados_escuelas_conducta'), 'icon': 'glyphicon glyphicon-chevron-right', 'visible': ['administrador', 'especialista', 'dpt_ee', 'dmt']},
                 {'name': 'Egresados de la EFI', 'url': reverse('listar_egresados_efi'), 'icon': 'glyphicon glyphicon-chevron-right', 'visible': ['administrador', 'especialista', 'dpt_ee', 'dmt']},
                 {'name': 'Jóvenes de 15 y 16 años', 'url': reverse('listar_menores'), 'icon': 'glyphicon glyphicon-chevron-right', 'visible': ['administrador', 'especialista', 'dpt_ee', 'dmt']},
                 {'name': 'Discapacitados', 'url': reverse('listar_discapacitados'), 'icon': 'glyphicon glyphicon-chevron-right', 'visible': ['administrador', 'especialista', 'dpt_ee', 'dmt']},
                 {'name': 'Personas de riesgo', 'url': reverse('listar_personas_riesgo'), 'icon': 'glyphicon glyphicon-chevron-right', 'visible': ['administrador', 'especialista', 'dpt_ee', 'dmt']},
         ]
         },

        {'name': 'Interruptos', 'url': reverse('interruptos'), 'icon': 'glyphicon glyphicon-briefcase','visible': ['administrador', 'interrupto'],
         'menu': [
             {'name': 'Organismos Autorizados', 'url': reverse('gestion_organismos_autorizados'),'icon': 'glyphicon glyphicon-chevron-right', 'visible': ['administrador', 'especialista']},
         ]},

        {'name': 'Seguimiento a jóvenes que abandonan estudios en el NS', 'url': reverse('gestion_jovenes_abandonan_nivel_superior'), 'icon': 'glyphicon glyphicon-briefcase', 'visible': ['administrador', 'trabajador_social_joven_abandona', 'universidad_joven_abandona', 'dmt_joven_abandona']},

        # ---------------codigo de daniel (FIN)---------------

            {'name':'Reportes','url':reverse('reportes'),'icon':'glyphicon glyphicon-menu-hamburger','visible':['administrador','especialista','organismo','dpts','invitado','mes','juridico', 'dmt', 'dpt_ee', 'interrupto']},

            {'name':'Nomencladores','url':reverse('nomencladores'),'icon':'glyphicon glyphicon-bookmark','visible':['administrador','especialista', 'dpt_ee', 'interrupto'],
               'menu':[
                    {'name':'Organismos','url':reverse('organismos'),'icon':'glyphicon glyphicon-chevron-right','visible':['administrador','especialista']},
                    {'name':'Categorías de usuario','url':reverse('categorias_usuario'),'icon':'glyphicon glyphicon-chevron-right','visible':['administrador','especialista']},
                    {'name':'Causales','url':reverse('causales'),'icon':'glyphicon glyphicon-chevron-right','visible':['administrador','especialista']},
                    {'name':'DPT','url':reverse('dir_trabajo'),'icon':'glyphicon glyphicon-chevron-right','visible':['administrador','especialista']},
                    {'name':'Carreras','url':reverse('carreras'),'icon':'glyphicon glyphicon-chevron-right','visible':['administrador','especialista']},
                    {'name':'Centros','url':reverse('centros_estudios'),'icon':'glyphicon glyphicon-chevron-right','visible':['administrador','especialista']},
                    {'name':'Tipo de Entidades', 'url': reverse('tiposentidades'),'icon': 'glyphicon glyphicon-chevron-right', 'visible': ['administrador', 'especialista']},
                    {'name':'Entidades', 'url': reverse('entidades'),'icon': 'glyphicon glyphicon-chevron-right', 'visible': ['administrador', 'especialista', 'dpt_ee', 'interrupto']},
            #
            #        # Daniel - inicio
            #
                   {'name': 'Niveles escolares', 'url': reverse('niveles_escolares'), 'icon': 'glyphicon glyphicon-chevron-right', 'visible': ['administrador', 'especialista']},
                   {'name': 'Causales de no aceptación', 'url': reverse('causales_no_aceptacion'), 'icon': 'glyphicon glyphicon-chevron-right', 'visible': ['administrador', 'especialista']},
                   {'name': 'Causales de no incorporación', 'url': reverse('causales_no_incorporacion'), 'icon': 'glyphicon glyphicon-chevron-right', 'visible': ['administrador', 'especialista']},
                   {'name': 'Causales de no ubicación', 'url': reverse('causales_no_ubicacion'), 'icon': 'glyphicon glyphicon-chevron-right', 'visible': ['administrador', 'especialista']},
                   {'name': 'Causales de baja', 'url': reverse('causales_baja'), 'icon': 'glyphicon glyphicon-chevron-right', 'visible': ['administrador', 'especialista']},
                   {'name': 'Ubicaciones', 'url': reverse('ubicaciones'), 'icon': 'glyphicon glyphicon-chevron-right', 'visible': ['administrador', 'especialista']},
                   {'name': 'Estados de incorporado', 'url': reverse('estados_incorporados'), 'icon': 'glyphicon glyphicon-chevron-right', 'visible': ['administrador', 'especialista']},
                   {'name': 'Delitos', 'url': reverse('delitos'), 'icon': 'glyphicon glyphicon-chevron-right', 'visible': ['administrador', 'especialista']},
                   {'name': 'Motivo de egreso de EP', 'url': reverse('motivos_egreso'), 'icon': 'glyphicon glyphicon-chevron-right', 'visible': ['administrador', 'especialista']},
                   {'name': 'Fuentes de procedencia', 'url': reverse('fuentes_procedencia'), 'icon': 'glyphicon glyphicon-chevron-right', 'visible': ['administrador', 'especialista']},
                   {'name': 'Discapacidades', 'url': reverse('discapacidades'), 'icon': 'glyphicon glyphicon-chevron-right', 'visible': ['administrador', 'especialista']},
                   {'name': 'Asociaciones', 'url': reverse('asociaciones'), 'icon': 'glyphicon glyphicon-chevron-right', 'visible': ['administrador', 'especialista']},
                   {'name': 'Causales de interrupción', 'url': reverse('causales_interrupcion'), 'icon': 'glyphicon glyphicon-chevron-right', 'visible': ['administrador', 'especialista']},
                   {'name': 'Causales de no reincorporación', 'url': reverse('causales_no_reincorporacion'), 'icon': 'glyphicon glyphicon-chevron-right', 'visible': ['administrador', 'especialista']},
                   {'name': 'Actividades de interrupción', 'url': reverse('actividades_interrupto'), 'icon': 'glyphicon glyphicon-chevron-right', 'visible': ['administrador', 'especialista']},
                   {'name': 'Causales no requieren empleo', 'url': reverse('gestion_causales_no_requieren_empleo'), 'icon': 'glyphicon glyphicon-chevron-right', 'visible': ['administrador']},
            #
            #        # Daniel - fin
            #
               ]
             },
            {'name':'Usuarios','url':reverse('usuarios'),'icon':'glyphicon glyphicon-user','visible':['administrador' ,'especialista']},
            {'name':'Indicaciones','url':reverse('indicaciones'),'icon':'glyphicon glyphicon-tasks','visible':['administrador','especialista','organismo','dpts','invitado','mes']},
            {'name':'Descargar GFORZA','url':reverse('descargar_gforza'),'icon':'glyphicon glyphicon-download','visible':['administrador', 'organismo', 'dpts', 'dpt_ee']},
            #
             ]}
    return procesar_menu(menu_dict,url_actual,cat,MENU)

def procesar_menu(menu_main,url_actual,cat,MENU):
   for item in menu_main['menu']:
        if is_visible(item,cat):
            item['active']= is_activo(item,url_actual)
            if item.get('menu')!= None:
                submenus=[]
                for i,item2 in enumerate(item.get('menu')):
                    if is_visible(item2,cat):
                        item2['active']= is_activo(item2,url_actual)
                        submenus.append(item2)
                item['menu']=submenus
            MENU['menu'].append(item)
   return MENU

def is_activo(item,url_actual):
    control=False
    if item['url'] == url_actual:
            control=  True
    elif url_actual.split("/")[1] == item['url'].split("/")[1]:
            control = True
    elif item.get('menu') != None:
        for item2 in item.get('menu'):
            if is_activo(item2,url_actual)==True:
                control=True
                break
    return control


def is_visible(item,cat):
        control=False
        if item['visible'].__contains__(cat):
            control=True
        return control










def notificaciones(request):
    current_url = request.resolver_match.url_name
    if current_url!="login" and request.path != "/":
        notificaciones=Notificacion.objects.filter(remitente=request.user).order_by("-fecha")
        notificaciones={'notificaciones':notificaciones,'cantidad_no_revisadas':Notificacion.objects.filter(revisado=False,remitente=request.user).count()}
        return notificaciones
    else:
        notificaciones={'notificaciones':[]}
        return notificaciones






