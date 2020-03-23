from django.conf.urls import  include, url

from django.contrib import admin

admin.autodiscover()
from SGMGU.views.views_usuarios import *
from SGMGU.views.views_expedientes import *
from SGMGU.views.views import *
from SGMGU.views.views_organismos import *
from SGMGU.views.views_causales import *
from SGMGU.views.view_movimientos_internos import *
from SGMGU.views.views_dir_trabajo import *
from SGMGU.views.views_carreras import *
from SGMGU.views.views_reportes import *
from SGMGU.views.views_ubicados import *
from SGMGU.views.views_fluctuacion import *
from SGMGU.views.views_inhabilitaciones import *
from SGMGU.views.views_centros_estudios import *
from SGMGU.views.views_entidades import *
from SGMGU.views.views_tiposentidades import *
from SGMGU.views.views_disponibles import *
from SGMGU.views.views_indicaciones import *
from SGMGU.views.views_demanda import *
from SGMGU.views.views_existencia import *
from django.conf import settings
from django.views.static import serve

# NOMENCLADORES -------------------------------------------------------------------
from SGMGU.views.Nomencladores.views_niveles_escolares import *
from SGMGU.views.Nomencladores.views_causales_no_aceptacion import *
from SGMGU.views.Nomencladores.views_ubicaciones import *
from SGMGU.views.Nomencladores.views_causales_no_incorporacion import *
from SGMGU.views.Nomencladores.views_causales_no_ubicacion import *
from SGMGU.views.Nomencladores.views_causales_baja import *
from SGMGU.views.Nomencladores.views_estados_incorporados import *
from SGMGU.views.Nomencladores.views_delitos import *
from SGMGU.views.Nomencladores.views_motivos_egreso import *
from SGMGU.views.Nomencladores.views_fuentes_procedencia import *
from SGMGU.views.Nomencladores.views_discapacidades import *
from SGMGU.views.Nomencladores.views_asociaciones import *
from SGMGU.views.Nomencladores.views_categorias_usuario import *
from SGMGU.views.Nomencladores.views_causales_interrupcion import *
from SGMGU.views.Nomencladores.views_actividad_interrupto import *
from SGMGU.views.Nomencladores.views_causales_no_reincorporacion import *
from SGMGU.views.Nomencladores.views_causales_no_requieren_empleo import *
from SGMGU.views.Nomencladores.views_causales_desvinculacion_ns import *
# ---------------------------------------------------------------------------------

# EMPLEO ESTATAL-------------------------------------------------------------------
from SGMGU.views.EmpleoEstatal.views_licenciados_sma import *
from SGMGU.views.EmpleoEstatal.views_egresados_establecimientos_penitenciarios import *
from SGMGU.views.EmpleoEstatal.views_desvinculados import *
from SGMGU.views.EmpleoEstatal.views_tecnicos_medios_obreros_calificados_escuelas_oficio import *
from SGMGU.views.EmpleoEstatal.views_menores import *
from SGMGU.views.EmpleoEstatal.views_egresados_escuelas_especiales import *
from SGMGU.views.EmpleoEstatal.views_egresados_escuelas_conducta import *
from SGMGU.views.EmpleoEstatal.views_egresados_efi import *
from SGMGU.views.EmpleoEstatal.views_discapacitados import *
from SGMGU.views.EmpleoEstatal.views_personas_riesgo import *
# ----------------------------------------------------------------------------------

# INTERRUPTOS-----------------------------------------------------------------------
from SGMGU.views.Interruptos.views_interruptos import *
from SGMGU.views.Interruptos.views_organismos_autorizados import *
# ----------------------------------------------------------------------------------

# REPORTES EMPLEO ESTATAL-----------------------------------------------------------
from SGMGU.views.ReportesEmpleoEstatal.views_reporte_nominal import *
from SGMGU.views.ReportesEmpleoEstatal.views_reporte_nominal_cierre_mes import *
from SGMGU.views.ReportesEmpleoEstatal.views_fuente_procedencia import *
from SGMGU.views.ReportesEmpleoEstatal.views_fuente_procedencia_cierre_mes import *
from SGMGU.views.ReportesEmpleoEstatal.views_filtrar_municipio_ubicados_y_pendientes import *
from SGMGU.views.ReportesEmpleoEstatal.views_general_provincias_ubicados_pendientes import *
from SGMGU.views.ReportesEmpleoEstatal.views_filtrar_mes_ubicados_y_pendientes import *
from SGMGU.views.ReportesEmpleoEstatal.views_total_personas_ubicadas_provincias import *
from SGMGU.views.ReportesEmpleoEstatal.views_total_personas_ubicadas_provincias_cierre_mes import *
from SGMGU.views.ReportesEmpleoEstatal.views_total_personas_ubicadas_provincias_y_municipios import *
from SGMGU.views.ReportesEmpleoEstatal.views_total_personas_ubicadas_provincias_y_municipios_cierre_mes import *
from SGMGU.views.ReportesEmpleoEstatal.views_total_personas_no_ubicadas_provincias import *
from SGMGU.views.ReportesEmpleoEstatal.views_total_personas_no_ubicadas_provincias_cierre_mes import *
from SGMGU.views.ReportesEmpleoEstatal.views_total_personas_no_ubicadas_provincias_y_municipios import *
from SGMGU.views.ReportesEmpleoEstatal.views_total_personas_no_ubicadas_provincias_y_municipios_cierre_mes import *
from SGMGU.views.ReportesEmpleoEstatal.views_no_ubicados_por_no_existir_oferta_cierre_mes import *
from SGMGU.views.ReportesEmpleoEstatal.views_no_ubicados_por_no_existir_oferta import *
from SGMGU.views.ReportesEmpleoEstatal.views_ubicados_y_pendientes_por_organismos import *
from SGMGU.views.ReportesEmpleoEstatal.views_ubicados_y_pendientes_por_organismos_cierre_mes import *
from SGMGU.views.ReportesEmpleoEstatal.views_desvinculados_no_ubicados_por_causales import *
from SGMGU.views.ReportesEmpleoEstatal.views_desvinculados_no_ubicados_por_causales_cierre_mes import *
from SGMGU.views.ReportesEmpleoEstatal.views_tecnicos_medios_pendientes_por_no_existir_oferta import *
from SGMGU.views.ReportesEmpleoEstatal.views_tecnicos_medios_pendientes_por_no_existir_oferta_cierre_mes import *
from SGMGU.views.ReportesEmpleoEstatal.views_obreros_calificados_pendientes_por_no_existir_oferta import *
from SGMGU.views.ReportesEmpleoEstatal.views_obreros_calificados_pendientes_por_no_existir_oferta_cierre_mes import *
from SGMGU.views.ReportesEmpleoEstatal.views_escuelas_oficio_pendientes_por_no_existir_oferta import *
from SGMGU.views.ReportesEmpleoEstatal.views_escuelas_oficio_pendientes_por_no_existir_oferta_cierre_mes import *
from SGMGU.views.ReportesEmpleoEstatal.views_mujeres_ubicadas_por_fuentes import *
from SGMGU.views.ReportesEmpleoEstatal.views_mujeres_ubicadas_por_fuentes_cierre_mes import *
from SGMGU.views.ReportesEmpleoEstatal.views_mujeres_no_ubicadas_por_fuentes import *
from SGMGU.views.ReportesEmpleoEstatal.views_mujeres_no_ubicadas_por_fuentes_cierre_mes import *
from SGMGU.views.ReportesEmpleoEstatal.views_menores_ubicados_por_sector import *
from SGMGU.views.ReportesEmpleoEstatal.views_menores_ubicados_por_sector_cierre_mes import *
from SGMGU.views.ReportesEmpleoEstatal.views_menores_ubicados_por_especialidad import *
from SGMGU.views.ReportesEmpleoEstatal.views_menores_ubicados_por_especialidad_cierre_mes import *
from SGMGU.views.ReportesEmpleoEstatal.views_obreros_calificados_pendientes_por_causales import *
from SGMGU.views.ReportesEmpleoEstatal.views_obreros_calificados_pendientes_por_causales_cierre_mes import *
from SGMGU.views.ReportesEmpleoEstatal.views_total_interruptos_por_organismos_cap import *
# ----------------------------------------------------------------------------------
# REPORTES LICENCIADOS SMA----------------------------------------------------------
from SGMGU.views.EmpleoEstatal.ReportesLicenciadosSMA.ubicacion_general_sma import *
from SGMGU.views.EmpleoEstatal.ReportesLicenciadosSMA.ubicacion_general_sma_diciembre import *
from SGMGU.views.EmpleoEstatal.ReportesLicenciadosSMA.ubicacion_general_sma_junio import *
from SGMGU.views.EmpleoEstatal.ReportesLicenciadosSMA.incorporados_por_organismos_sma import *
from SGMGU.views.EmpleoEstatal.ReportesLicenciadosSMA.incorporados_por_organismos_sma_diciembre import *
from SGMGU.views.EmpleoEstatal.ReportesLicenciadosSMA.incorporados_por_organismos_sma_junio import *
from SGMGU.views.EmpleoEstatal.ReportesLicenciadosSMA.causas_no_incorporado_sma import *
from SGMGU.views.EmpleoEstatal.ReportesLicenciadosSMA.relacion_no_ubicados_nominal_sma import *
from SGMGU.views.EmpleoEstatal.ReportesLicenciadosSMA.relacion_no_ubicados_nominal_sma_diciembre import *
from SGMGU.views.EmpleoEstatal.ReportesLicenciadosSMA.relacion_no_ubicados_nominal_sma_junio import *
from SGMGU.views.EmpleoEstatal.ReportesLicenciadosSMA.resultados_entrevistas_sma import *
from SGMGU.views.EmpleoEstatal.ReportesLicenciadosSMA.resultados_entrevistas_sma_diciembre import *
from SGMGU.views.EmpleoEstatal.ReportesLicenciadosSMA.resultados_entrevistas_sma_junio import *
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
# REPORTES INTERRUPTOS-----------------------------------------------------------
from SGMGU.views.ReportesInterruptos.views_interruptos_por_organismos import *
from SGMGU.views.ReportesInterruptos.views_interruptos_por_organismos_filtros import *
from SGMGU.views.ReportesInterruptos.views_interruptos_organismos_sin_entidades import *
from SGMGU.views.ReportesInterruptos.views_interruptos_provincias import *
from SGMGU.views.ReportesInterruptos.views_interruptos_provincias_sin_entidades import *
from SGMGU.views.ReportesInterruptos.views_interruptos_actividades import *
from SGMGU.views.ReportesInterruptos.views_interruptos_actividades_sin_entidades import *
from SGMGU.views.ReportesInterruptos.views_interruptos_causas_interrupcion import *
from SGMGU.views.ReportesInterruptos.views_interruptos_causas_interrupcion_sin_entidades import *
from SGMGU.views.ReportesInterruptos.views_interruptos_reubicados import *
# ----------------------------------------------------------------------------------

from SGMGU.views.SeguimientoJovenesAbandonanNS.views_seguimiento_jovenes_ans_ import *

# DESCARGAR GFORZA-----------------------------------------------------------
from SGMGU.views.views_descargar_gforza import *
# ----------------------------------------------------------------------------------

urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT, }),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^inicio$', inicio, name='inicio'),
    url(r'^$', login_view, ),
    url(r'^login$', login_view, name="login"),
    url(r'^logout$', logout_view),
    url(r'^contacto', contacto,name='contacto'),


    url(r'^enviar_notificacion$',enviar_notificacion),
    url(r'^revisar_notificacion/(?P<id_notificacion>[\w]+)$',revisar_notificacion),
    url(r'^eliminar_notificacion/(?P<id_notificacion>[\w]+)$',eliminar_notificacion),
    url(r'^notificaciones_usuarios/(?P<id_usuario>[\w]+)$',listado_usuarios_notificaciones),




    url(r'^usuarios$',gestion_usuarios,name='usuarios'),
    url(r'^usuarios/(?P<id_usuario>[\w]+)/modificar/$',modificar_usuario),
    url(r'^usuarios/(?P<id_usuario>[\w]+)/cambiar_contrasenna/$',cambiar_contrasenna),
    url(r'^usuarios/(?P<id_usuario>[\w]+)/eliminar/$',eliminar_usuario),
    url(r'^usuarios/registrar_usuario/$',registrar_usuario, name='registrar_usuario'),
    url(r'^usuario/cambiar_contrasenna/$',cambiar_contrasenna_user_actual),
    url(r'^usuario/modificar/$',modificar_usuario_actual),


    url(r'^gestion_expedientes$',gestion_expedientes,name='expedientes'),
    url(r'^autocompletar_expediente$',autocompletar_expediente,{'vista':'avanzada'}),
    url(r'^autocompletar_movimiento_interno$',autocompletar_expediente,{'vista':'interno'}),

    url(r'^autocompletar_expediente_estandar$',autocompletar_expediente,{'vista':'estandar'}),
    url(r'^gestion_expedientes/registrar_expediente$',registrar_expediente,{'vista':'avanzada'}),
    url(r'^gestion_expedientes/(?P<id_expediente>[\w]+)/modificar/$',editar_expediente,{'vista':'estandar'} ),
    url(r'^gestion_expedientes/(?P<id_expediente>[\w]+)/eliminar/$',eliminar_expediente),
    url(r'^registrar_expediente_estandar/$',registrar_expediente ,{'vista':'estandar'},name="registrar_expediente_estandar",),
    url(r'^gestion_expedientes/ci/(?P<ci>[\w]+)$',buscar_expediente_ci),
    url(r'^gestion_expedientes/id/(?P<id>[\w]+)$',buscar_expediente_id),
    url(r'^gestion_expedientes/(?P<id_expediente>[\w]+)$',detalle_expediente),

    url(r'^organismos$',gestion_organismos,name='organismos'),
    url(r'^organismos/registrar_organismo/$',registrar_organismo),
    url(r'^organismos/(?P<id_organismo>[\w]+)/eliminar/$',eliminar_organismo),
    url(r'^organismos/(?P<id_organismo>[\w]+)/modificar/$',modificar_organismo),


    url(r'^causales$',gestion_causales,name='causales'),
    url(r'^causales/registrar_causal/$',registrar_causal),
    url(r'^causales/(?P<id_causal>[\w]+)/eliminar/$',eliminar_causal),
    url(r'^causales/(?P<id_causal>[\w]+)/modificar/$',modificar_causal),


    url(r'^descargar_comprimido/(?P<id_expediente>[\w]+)$',descargar_comprimido),
    url(r'^descargar_informe/(?P<id_expediente>[\w]+)$',descargar_informe),
    url(r'^ver_informe/(?P<id_expediente>[\w]+)$',ver_informe),
    url(r'^exportar_resumen_mensual$',exportar_resumen_mensual),
    url(r'^exportar_carreras_expedientes$',exportar_carreras_expedientes),
    url(r'^exportar_causales_expedientes$',exportar_causales_expedientes),
    url(r'^exportar_provincias_expedientes$',exportar_provincias_expedientes),
    url(r'^exportar_organismos_expedientes$',exportar_organismos_expedientes),
    url(r'^exportar_expedientes_carrera$',exportar_expedientes_segun_carrera),
    url(r'^exportar_expedientes_causal$',exportar_expedientes_segun_causal),



    #mario------------------------------------------------------------------------------------------
    url(r'^carreras$',gestion_carreras,name='carreras'),
    url(r'^carreras/registrar_carrera$',registrar_carrera),
    url(r'^carreras/buscar$',buscar_carreras),
    url(r'^carreras/(?P<id_carrera>[\w]+)/eliminar$',eliminar_carrera),
    url(r'^carreras/(?P<id_carrera>[\w]+)/modificar$',modificar_carrera),


    url(r'^centros_estudios$',gestion_centros_estudios,name='centros_estudios'),
    url(r'^centros_estudios/registrar_centro$',registrar_centro_estudios),
    url(r'^centros_estudios/(?P<id_centro_estudio>[\w]+)/eliminar$',eliminar_centro_estudios),
    url(r'^centros_estudios/(?P<id_centro_estudio>[\w]+)/modificar$',modificar_centro_estudios),

    #url para el menu de geforza
    url(r'^geforza$',geforza,name='geforza'),

    url(r'^entidades$',gestion_entidades,name='entidades'),
    url(r'^entidades/registrar_entidad$',registrar_entidad, name='registrar_entidad'),
    url(r'^entidades/(?P<id_entidad>[\w]+)/eliminar$', eliminar_entidad),
    url(r'^entidades/(?P<id_entidad>[\w]+)/activar$', activar_entidad),
    url(r'^entidades/(?P<id_entidad>[\w]+)/modificar$', modificar_entidad, name='modificar_entidad'),

    url(r'^tiposentidades$', gestion_tiposentidades, name='tiposentidades'),
    url(r'^tiposentidades/registrar_tipoentidades$', registrar_tipoentidad),
    url(r'^tiposentidades/(?P<identificador>[\w]+)/eliminar$', eliminar_tipoentidad),
    url(r'^tiposentidades/(?P<identificador>[\w]+)/modificar$', modificar_tipoentidad),

    url(r'^demandas$',gestion_demanda,name='demandas'),
    url(r'^demandas/registrar_demanda$', registrar_demanda),
    url(r'^demandas/buscar$',buscar_demanda),
    url(r'^demandas/(?P<identificador>[\w]+)/eliminar$', eliminar_demanda),
    url(r'^demandas/(?P<identificador>\d+)/modificar$', modificar_demanda),

   #------------------------------------------
    # url(r'^demandas$',gestion_demanda, name='demandas'),
    # url(r'^demandas/demanda_create/$',demanda_create,name='demanda_create'),


    #-------------------------------------------------------

    url(r'^existencias$', gestion_existencias, name='existencias'),
    url(r'^existencias/registrar_existencia$', registrar_existencia),
    url(r'^existencias/buscar$', buscar_existencias),
    url(r'^existencias/(?P<id_existencia>[\w]+)/eliminar$', eliminar_existencia),
    url(r'^existencias/(?P<id_existencia>[\w]+)/modificar$', modificar_existencia),

    url(r'^fluctuaciones$', gestion_fluctuacion, name='fluctuaciones'),
    url(r'^fluctuaciones/registrar_fluctuacion$', registrar_fluctuacion),
    url(r'^fluctuaciones/buscar$', buscar_fluctuaciones),
    url(r'^fluctuaciones/(?P<id_fluctuacion>[\w]+)/eliminar$', eliminar_fluctuacion),
    url(r'^fluctuaciones/(?P<id_fluctuacion>[\w]+)/modificar$', modificar_fluctuacion),

    #/mario-------------------------------------------------------------------------------------------



    url(r'^expedientes_pendientes$',listado_expedientes_pendientes,name='pendientes'),
    url(r'^expedientes_pendientes/(?P<id_expediente>[\w]+)$',detalle_expediente_pendiente),
    url(r'^aprobar_expediente_pendiente/(?P<id_expediente_pend>[\w]+)$',aprobar_expediente_pendiente),
    url(r'^rechazar_expediente_pendiente/(?P<id_expediente_pend>[\w]+)$',rechazar_expediente_pendiente),
    url(r'^no_aprobar_expediente_pendiente/(?P<id_expediente_pend>[\w]+)$',no_aprobar_expediente_pendiente),
    url(r'^exportar_expediente/(?P<id_expediente>[\d]+)$',exportar_expediente),
    url(r'^exportar_expediente_aprobado/(?P<id_expediente>[\d]+)$',exportar_expediente_aprobado),


    url(r'^expedientes_pendientes/(?P<id_expediente>[\w]+)/editar$',editar_expediente,{'vista':'pendiente'}),
    url(r'^expedientes_rechazados/(?P<id_expediente>[\w]+)/editar$',editar_expediente,{'vista':'rechazado'}),
    url(r'^expedientes_aprobados/(?P<id_expediente>[\w]+)/editar$',editar_expediente,{'vista':'aprobado'}),
    url(r'^expedientes_no_aprobados/(?P<id_expediente>[\w]+)/editar$',editar_expediente,{'vista':'no_aprobado'}),
    url(r'^expedientes_pendientes/ci/(?P<ci>[\w]+)$',buscar_expedientes_pendientes_ci),


    url(r'^expedientes_rechazados$',listado_expedientes_rechazado,name='rechazados'),
    url(r'^aprobar_expediente_rechazado/(?P<id_expediente_rech>[\w]+)$',aprobar_expediente_rechazado),
    url(r'^no_aprobar_expediente_rechazado/(?P<id_expediente_rech>[\w]+)$',no_aprobar_expediente_rechazado),
    url(r'^pasar_a_pendientes_de_rechazo/(?P<id_expediente>[\w]+)$',pasar_a_pendientes_from_rechazo),
    url(r'^expedientes_rechazados/(?P<id_expediente>[\w]+)$',detalle_expediente_rechazado),
    url(r'^expedientes_rechazados/ci/(?P<ci>[\w]+)$',buscar_expedientes_rechazados_ci),


    url(r'^expedientes_no_aprobados$',listado_expedientes_no_aprobados,name='no_aprobados'),
    url(r'^pasar_a_pendientes_de_no_aprobado/(?P<id_expediente>[\w]+)$',pasar_a_pendientes_de_no_aprobado),
    url(r'^expedientes_no_aprobados/detalle_expediente_no_aprobado/(?P<id_expediente>[\w]+)$',detalle_expediente_no_aprobado),
    url(r'^aprobar_expediente_no_aprobado/(?P<id_expediente_no_aprob>[\w]+)$',aprobar_expediente_no_aprobado),
    url(r'^rechazar_expediente_no_aprobado/(?P<id_expediente_no_aprob>[\w]+)$',rechazar_expediente_no_aprobado),
    url(r'^expedientes_no_aprobados/(?P<id_expediente>[\w]+)$',detalle_expediente_no_aprobado),
    url(r'^expedientes_no_aprobados/ci/(?P<ci>[\w]+)$',buscar_expedientes_no_aprobados_ci),


    url(r'^expedientes_aprobados$',listado_expedientes_aprobados,name='aprobados'),
    url(r'^pasar_a_pendientes/(?P<id_expediente>[\w]+)$',pasar_a_pendientes),
    url(r'^no_aprobar_expediente_aprobado/(?P<id_expediente_aprob>[\w]+)$',no_aprobar_expediente_aprobado),
    url(r'^rechazar_expediente_aprobado/(?P<id_expediente_aprob>[\w]+)$',rechazar_expediente_aprobado),
    url(r'^expedientes_aprobados/ci/(?P<ci>[\w]+)$',buscar_expedientes_aprobados_ci),
    url(r'^expedientes_aprobados/rs/(?P<rs>[\w]+)$',buscar_expedientes_aprobados_rs),
    url(r'^expedientes_aprobados/(?P<id_expediente>[\w]+)$',detalle_expediente_aprobado),


    url(r'^movimientos_internos$',movimientos_internos,name='movimientos_internos'),
    url(r'^movimientos_internos/(?P<id_expediente>[\w]+)/eliminar/$',eliminar_movimiento_interno),
    url(r'^movimientos_internos/(?P<id_expediente>[\w]+)/modificar/$',modificar_movimiento_interno),
    url(r'^movimientos_internos/registrar/$',registrar_movimiento_interno),
    url(r'^movimientos_internos/ci/(?P<ci>[\w]+)$',buscar_movimientos_internos_ci),

    url(r'^reportes$',reportes,name='reportes'),
    url(r'^reportes/reporte_exp_org_carrera$',reporte_exp_organismo_carrera),
    url(r'^reportes/reporte_exp_organismos$',reporte_exp_organismo),
    url(r'^reportes/reporte_exp_org_provincia$',reporte_exp_org_provincia),

    url(r'^reportes/reporte_noexp_org_carrera$',reporte_noexp_organismo_carrera),
    url(r'^reportes/reporte_noexp_organismos$',reporte_noexp_organismo),
    url(r'^reportes/reporte_mov_int_organismos$',reporte_mov_int_organismos),
    url(r'^direcciones_trabajo$',gestion_dir_trabajo,name='dir_trabajo'),
    url(r'^direcciones_trabajo/(?P<id_dir>[\w]+)/modificar$',modificar_dir_trabajo),
    url(r'^ubicados$',m_ubicados, {'filtro':''},name="ubicados"),
    url(r'^ubicados/desfasados$',m_ubicados, {'filtro':'desfasados'},name="ubicados"),
    url(r'^ubicados/graduados$',m_ubicados, {'filtro':'graduados'},name="ubicados"),
    url(r'^ubicados/registrar$',registrar_ubicacion),
    url(r'^ubicados/no_presentacion',no_presentacion),
    url(r'^ubicados/(?P<id_ubicacion>[\d]+)/presentacion$',presentacion),
    url(r'^ubicados/todos$',m_ubicados,{'filtro':'todos'}),
    url(r'^ubicados/ci/(?P<ci>[\d]+)$',buscar_ci_ubicado),
    url(r'^ubicados/(?P<id_ubicacion>[\d]+)/modificar$',modificar_ubicacion_laboral),
    url(r'^ubicados/(?P<id_ubicacion>[\d]+)/pasar_a_disponibles',pasar_a_disponibles),
    url(r'^ubicados/(?P<id_ubicacion>[\d]+)/eliminar$',eliminar_ubicacion),
    url(r'^ubicados/propios/(?P<opcion>(organismo|carrera|provincia_residencia|provincia_ubicacion|centro_estudio){1})/(?P<id_opcion>[\w]+)$',filtrar_ubicados),


     url(r'^inhabilitaciones$',inhabilitaciones,name="inhabilitaciones"),
     url(r'^inhabilitaciones/registrar$',registrar_inhabilitacion),
     url(r'^inhabilitaciones/autocompletar_inhabilitado$',autocompletar_inhabilitado),
     url(r'^inhabilitaciones/ci/(?P<ci>[\d]+)$',buscar_ci_inhabilitado),
     url(r'^inhabilitaciones/no/(?P<no>[\d]+)$',buscar_no_inhabilitado),
     url(r'^inhabilitaciones/(?P<id_proceso>[\d]+)$',detalle_proceso),
     url(r'^inhabilitaciones/(?P<id_proceso>[\d]+)/editar$',modificar_proceso),
     url(r'^inhabilitaciones/(?P<id_proceso>[\d]+)/eliminar$',eliminar_proceso),
     url(r'^exportar_total_procesos$',exportar_total_procesos),
     url(r'^exportar_total_procesos_causales$',exportar_total_procesos_causales),
     url(r'^exportar_total_procesos_organismos$',exportar_total_procesos_organismos),
     url(r'^exportar_total_procesos_niveles$',exportar_total_procesos_niveles),
     url(r'^exportar_procesos_registro_nominal$',exportar_procesos_registro_nominal),



     url(r'^disponibles/registrar$',registrar_disponibilidad),
     url(r'^disponibles$',m_disponibles,name="disponibles"),
     url(r'^disponibles/(?P<id_disponibilidad>[\d]+)/ubicar$',ubicar_disponibilidad),
     url(r'^disponibles/(?P<id_disponibilidad>[\d]+)/eliminar',eliminar_disponibilidad),
     url(r'^disponibles/(?P<id_disponibilidad>[\d]+)$',detalle_disponibilidad),
     url(r'^disponibles/ci/(?P<ci>[\d]+)$',buscar_ci_disponible),
     url(r'^disponibles/importar$',importar_disponibilidad),
     url(r'^disponibles/buscar_disponibles_carrera$',buscar_disponibles,{'opcion':'carrera'}),
     url(r'^disponibles/buscar_disponibles_municipio_residencia$',buscar_disponibles,{'opcion':'municipio_residencia'}),
     url(r'^disponibles/buscar_disponibles_centro_estudio$',buscar_disponibles,{'opcion':'centro_estudio'}),
     url(r'^disponibles/(?P<opcion>(carrera|organismo|municipio_residencia|centro_estudio){1})/(?P<id_opcion>[\d]+)$',filtrar_disponibles),
     url(r'^exportar_analisis_ubicacion$',exportar_analisis_ubicacion),

    url(r'^ubicados/buscar_ubicados_organismo$',buscar_ubicados,{'opcion':'organismo'}),
    url(r'^ubicados/buscar_ubicados_provincia_carrera$',buscar_ubicados,{'opcion':'carrera'}),
    url(r'^ubicados/buscar_ubicados_provincia_residencia$',buscar_ubicados,{'opcion':'provincia_residencia'}),
    url(r'^ubicados/buscar_ubicados_provincia_ubicacion$',buscar_ubicados,{'opcion':'provincia_ubicacion'}),
    url(r'^ubicados/buscar_ubicados_centro_estudio$',buscar_ubicados,{'opcion':'centro_estudio'}),

    url(r'^exportar_ubicados_provincia_residencia$',exportar_ubicados_provincia,{'opcion':'residencia'}),
    url(r'^exportar_ubicados_provincia_ubicacion$',exportar_ubicados_provincia,{'opcion':'ubicacion'}),
    url(r'^exportar_ubicados_organismo$',exportar_ubicados_organismo),
    url(r'^exportar_total_ubicados_organismos$',exportar_total_ubicados_organismos),
    url(r'^exportar_total_ubicados_provincias_ubicacion$',exportar_total_ubicados_provincias,{'opcion':'ubicacion'}),
    url(r'^exportar_total_ubicados_provincias_residencia$',exportar_total_ubicados_provincias,{'opcion':'residencia'}),
    url(r'^exportar_ubicados$',exportar_ubicados),
    url(r'^exportar_ubicados_universidades$',exportar_ubicados_universidades),
    url(r'^ubicados/(?P<id_ubicacion>[\d]+)$',detalle_ubicacion),

    url(r'^graduado/ci/(?P<ci>[\d]+)$',ficha_graduado,name='ficha_graduado'),
    url(r'^movimiento_laboral$',movimiento_laboral,name='movimiento_laboral'),
    url(r'^ubicacion_laboral$',ubicacion_laboral,name='ubicacion_laboral'),
    url(r'^nomencladores$',nomencladores,name='nomencladores'),


    url(r'^indicaciones$',indicaciones,name='indicaciones'),
    url(r'^indicaciones/categorias/registrar$',registar_castegoria_indicacion),
    url(r'^indicaciones/categorias/(?P<id_categoria>[\w]+)$',indicaciones,name='indicaciones_categorias'),
    url(r'^indicaciones/(?P<id_indicacion>[\w]+)/download$',download_indicacion),
    url(r'^indicaciones/registrar$',registrar_indicacion),
    url(r'^indicaciones/(?P<id_indicacion>[\w]+)/editar$',editar_indicacion),
    url(r'^indicaciones/(?P<id_indicacion>[\w]+)/eliminar$',eliminar_indicacion),



    # ---------------codigo de daniel (INICIO)---------------


    # EMPLEO ESTATAL
    url(r'^menu_empleo_estatal', menu_empleo_estatal, name="menu_empleo_estatal"),

    # LICENCIADOS DEL SMA
    url(r'^licenciados_sma$', listado_licenciados_sma, name="listar_licenciados_sma"),
    url(r'^licenciados_sma/registrar', registrar_licenciado_sma, name="registrar_licenciado_sma"),
    url(r'^licenciados_sma/(?P<id_licenciado_sma>[\w]+)/dar_baja', dar_baja_licenciado_sma,
        name="dar_baja_licenciado_sma"),
    url(r'^licenciados_sma/(?P<id_licenciado_sma>[\w]+)/modificar', modificar_licenciado_sma,
        name="modificar_licenciado_sma"),
    url(r'^licenciados_sma/(?P<id_licenciado_sma>[\d]+)$', detalle_licenciado_sma, name='detalles_licenciado_sma'),
    url(r'^licenciados_sma/(?P<id_licenciado_sma>[\w]+)/control', control_licenciado_sma,
        name="control_licenciado_sma"),
    url(r'^licenciados_sma/(?P<id_licenciado_sma>[\d]+)/re_incorporar', re_incorporar_licenciado_sma,
        name='re_incorporar_licenciado_sma'),
    url(r'^licenciados_sma/ci/(?P<ci>[\d]+)$', buscar_ci_licenciados_sma),
    url(r'^licenciados_sma/arreglar_errores$', arreglar_errores, name="arreglar_errores"),
    url(r'^licenciados_sma/habilitar_usando_ci', habilitar_licenciado_sma, name="habilitar_licenciado_sma"),

    # REPORTES (Licenciados del SMA)
    url(r'^licenciados_sma/reportes$', reportes_licenciados_sma, name="reportes_licenciados_sma"),
    # TOTAL
    url(r'^licenciados_sma/reportes/ubicacion_general_sma$', ubicacion_general_sma, name="ubicacion_general_sma"),
    url(r'^licenciados_sma/reportes/incorporados_por_organismos$', incorporados_por_organismos_sma, name="incorporados_por_organismos_sma"),
    url(r'^licenciados_sma/reportes/causas_no_incorporado$', causas_no_incorporado_sma, name="causas_no_incorporado_sma"),
    url(r'^licenciados_sma/reportes/relacion_nominal_no_incorporados$', relacion_no_ubicados_nominal_sma, name="relacion_no_ubicados_nominal_sma"),
    url(r'^licenciados_sma/reportes/resultados_entrevistas_sma$', resultados_entrevistas_sma, name="resultados_entrevistas_sma"),
    # JUNIO
    url(r'^licenciados_sma/reportes/ubicacion_general_sma_junio$', ubicacion_general_sma_junio, name="ubicacion_general_sma_junio"),
    url(r'^licenciados_sma/reportes/incorporados_por_organismos_junio$', incorporados_por_organismos_sma_junio, name="incorporados_por_organismos_sma_junio"),
    url(r'^licenciados_sma/reportes/relacion_nominal_no_incorporados_junio$', relacion_no_ubicados_nominal_sma_junio, name="relacion_no_ubicados_nominal_sma_junio"),
    url(r'^licenciados_sma/reportes/resultados_entrevistas_sma_junio$', resultados_entrevistas_sma_junio, name="resultados_entrevistas_sma_junio"),
    # DICIEMBRE
    url(r'^licenciados_sma/reportes/ubicacion_general_sma_diciembre$', ubicacion_general_sma_diciembre, name="ubicacion_general_sma_diciembre"),
    url(r'^licenciados_sma/reportes/incorporados_por_organismos_diciembre$', incorporados_por_organismos_sma_diciembre, name="incorporados_por_organismos_sma_diciembre"),
    url(r'^licenciados_sma/reportes/relacion_nominal_no_incorporados_diciembre$', relacion_no_ubicados_nominal_sma_diciembre, name="relacion_no_ubicados_nominal_sma_diciembre"),
    url(r'^licenciados_sma/reportes/resultados_entrevistas_sma_diciembre$', resultados_entrevistas_sma_diciembre, name="resultados_entrevistas_sma_diciembre"),
    # CATEGORIAS DE USUARIOS
    url(r'^categorias_usuario$', gestion_categorias_usuario, name='categorias_usuario'),
    url(r'^categorias_usuario/registrar$', registrar_categoria_usuario, name='registrar_categoria_usuario'),
    url(r'^categorias_usuario/(?P<id_categoria_usuario>[\w]+)/eliminar$', eliminar_categoria_usuario),
    url(r'^categorias_usuario/(?P<id_categoria_usuario>[\w]+)/modificar$', modificar_categoria_usuario),
    # url(r'^categorias_usuario/(?P<id_categoria_usuario>[\w]+)/activar$', activar_categoria_usuario),


    # NIVELES ESCOLARES
    url(r'^niveles_escolares$', gestion_niveles_escolares, name='niveles_escolares'),
    url(r'^niveles_escolares/registrar$', registrar_nivel_escolar, name='registrar_nivel_escolar'),
    url(r'^niveles_escolares/(?P<id_nivel_escolar>[\w]+)/eliminar$', eliminar_nivel_escolar),
    url(r'^niveles_escolares/(?P<id_nivel_escolar>[\w]+)/modificar$', modificar_nivelel_escolar),
    # url(r'^niveles_escolares/(?P<id_nivel_escolar>[\w]+)/activar$', activar_nivel_escolar),

    # CAUSALES DE NO ACEPTACION
    url(r'^causales_no_aceptacion$', gestion_causales_no_aceptacion, name='causales_no_aceptacion'),
    url(r'^causales_no_aceptacion/registrar_causal_no_aceptacion$', registrar_causal_no_aceptacion,
        name='registrar_causal_no_aceptacion'),
    url(r'^causales_no_aceptacion/(?P<id_causal_no_aceptacion>[\w]+)/eliminar$', eliminar_causal_no_aceptacion),
    url(r'^causales_no_aceptacion/(?P<id_causal_no_aceptacion>[\w]+)/modificar$', modificar_causal_no_aceptacion),
    # url(r'^causales_no_aceptacion/(?P<id_causal_no_aceptacion>[\w]+)/activar$', activar_causal_no_aceptacion),

    # CAUSALES DE NO INCORPORACION
    url(r'^causales_no_incorporacion$', gestion_causales_no_incorporacion, name='causales_no_incorporacion'),
    url(r'^causales_no_incorporacion/registrar$', registrar_causal_no_incorporacion,
        name='registrar_causal_no_incorporacion'),
    url(r'^causales_no_incorporacion/(?P<id_causal_no_incorporacion>[\w]+)/eliminar$',
        eliminar_causal_no_incorporacion),
    url(r'^causales_no_incorporacion/(?P<id_causal_no_incorporacion>[\w]+)/modificar$',
        modificar_causal_no_incorporacion),
    # url(r'^causales_no_incorporacion/(?P<id_causal_no_incorporacion>[\w]+)/activar$', activar_causal_no_incorporacion),


    # CAUSALES DE BAJA
    url(r'^causales_baja$', gestion_causales_baja, name='causales_baja'),
    url(r'^causales_baja/registrar$', registrar_causal_baja, name='registrar_causal_baja'),
    url(r'^causales_baja/(?P<id_causal_baja>[\w]+)/eliminar$', eliminar_causal_baja),
    url(r'^causales_baja/(?P<id_causal_baja>[\w]+)/modificar$', modificar_causal_baja),
    # url(r'^causales_baja/(?P<id_causal_baja>[\w]+)/activar$', activar_causal_baja),


    # UBICACION
    url(r'^ubicaciones$', gestion_ubicaciones, name='ubicaciones'),
    url(r'^ubicaciones/registrar_ubicacion$', registrar_ub, name='registrar_ub'),
    url(r'^ubicaciones/(?P<id_ubicacion>[\w]+)/eliminar$', eliminar_ubicacion),
    url(r'^ubicaciones/(?P<id_ubicacion>[\w]+)/modificar$', modificar_ubicacion),
    # url(r'^ubicaciones/(?P<id_ubicacion>[\w]+)/activar$', activar_ubicacion),

    #     ------------------------------------------------------------

    # EGRESADOS DE ESTABLECIMIENTOS PENITENCIARIOS Y SANCIONADOS
    url(r'^egresados_establecimientos_penitenciarios$', listado_egresados_establecimientos_penitenciarios,
        name="listar_egresados_establecimientos_penitenciarios"),
    url(r'^egresados_establecimientos_penitenciarios/registrar$', registrar_egresado_establecimiento_penitenciario,
        name="registrar_egresado_establecimiento_penitenciario"),
    url(r'^egresados_establecimientos_penitenciarios/(?P<id_egresado_establecimiento_penitenciario>[\w]+)/dar_baja',
        dar_baja_egresado_ep, name="dar_baja_egresado_ep"),
    url(r'^egresados_establecimientos_penitenciarios/(?P<id_egresado_establecimiento_penitenciario>[\w]+)/modificar',
        modificar_egresado_establecimiento_penitenciario, name="modificar_egresado_establecimiento_penitenciario"),
    url(r'^egresados_establecimientos_penitenciarios/(?P<id_egresado_establecimiento_penitenciario>[\d]+)$',
        detalle_egresado_establecimiento_penitenciario, name='detalle_egresado_establecimiento_penitenciario'),
    url(
        r'^egresados_establecimientos_penitenciarios/(?P<id_egresado_establecimiento_penitenciario>[\d]+)/re_incorporar',
        re_incorporar_egresado_establecimiento_penitenciario,
        name='re_incorporar_egresado_establecimiento_penitenciario'),
    url(r'^egresados_establecimientos_penitenciarios/ci/(?P<ci>[\d]+)$', buscar_ci_egresados_sancionados),
    url(r'^egresados_establecimientos_penitenciarios/habilitar_usando_ci', habilitar_egresado_establecimiento_penitenciario,
        name="habilitar_egresado_establecimiento_penitenciario"),

    # REPORTES
    url(r'^egresados_establecimientos_penitenciarios/reportes$', reportes_egresados_establecimientos_penitenciarios,
        name="reportes_egresados_establecimientos_penitenciarios"),

    # CAUSALES DE NO ACEPTACION
    url(r'^causales_no_ubicacion$', gestion_causales_no_ubicacion, name='causales_no_ubicacion'),
    url(r'^causales_no_ubicacion/registrar$', registrar_causal_no_ubicacion, name='registrar_causal_no_ubicacion'),
    url(r'^causales_no_ubicacion/(?P<id_causal_no_ubicacion>[\w]+)/eliminar$', eliminar_causal_no_ubicacion),
    url(r'^causales_no_ubicacion/(?P<id_causal_no_ubicacion>[\w]+)/modificar$', modificar_causal_no_ubicacion),
    # url(r'^causales_no_ubicacion/(?P<id_causal_no_ubicacion>[\w]+)/activar$', activar_causal_no_ubicacion),


    # ESTADOS DE INCORPORADOS
    url(r'^estados_incorporados$', gestion_estados_incorporados, name='estados_incorporados'),
    url(r'^estados_incorporados/registrar$', registrar_estado_incorporado, name='registrar_estado_incorporado'),
    url(r'^estados_incorporados/(?P<id_estado_incorporado>[\w]+)/eliminar$', eliminar_estado_incorporado),
    url(r'^estados_incorporados/(?P<id_estado_incorporado>[\w]+)/modificar$', modificar_estado_incorporado),
    # url(r'^estados_incorporados/(?P<id_estado_incorporado>[\w]+)/activar$', activar_estado_incorporado),


    # FUENTES DE PROCEDENCIA
    url(r'^fuentes_procedencia$', gestion_fuentes_procedencia, name='fuentes_procedencia'),
    url(r'^fuentes_procedencia/registrar$', registrar_fuente_procedencia, name='registrar_fuente_procedencia'),
    url(r'^fuentes_procedencia/(?P<id_fuente_procedencia>[\w]+)/eliminar$', eliminar_fuente_procedencia),
    url(r'^fuentes_procedencia/(?P<id_fuente_procedencia>[\w]+)/modificar$', modificar_fuente_procedencia),
    # url(r'^fuentes_procedencia/(?P<id_fuente_procedencia>[\w]+)/activar$', activar_fuente_procedencia),


    # TIPOS DE MEDIDAS
    url(r'^delitos$', gestion_delitos, name='delitos'),
    url(r'^delitos/registrar$', registrar_delito, name='registrar_delito'),
    url(r'^delitos/(?P<id_delito>[\w]+)/eliminar$', eliminar_delito),
    url(r'^delitos/(?P<id_delito>[\w]+)/modificar$', modificar_delito),
    # # url(r'^delitos/(?P<id_delito>[\w]+)/activar$', activar_delito),


    # MOTIVOS DE EGRESO
    url(r'^motivos_egreso$', gestion_motivos_egreso, name='motivos_egreso'),
    url(r'^motivos_egreso/registrar$', registrar_motivo_egreso, name='registrar_motivo_egreso'),
    url(r'^motivos_egreso/(?P<id_motivo_egreso>[\w]+)/eliminar$', eliminar_motivo_egreso),
    url(r'^motivos_egreso/(?P<id_motivo_egreso>[\w]+)/modificar$', modificar_motivo_egreso),
    # url(r'^motivos_egreso/(?P<id_motivo_egreso>[\w]+)/activar$', activar_motivo_egreso),


    # DISCAPACIDADES
    url(r'^discapacidades$', gestion_discapacidades, name='discapacidades'),
    url(r'^discapacidades/registrar$', registrar_discapacidad, name='registrar_discapacidad'),
    url(r'^discapacidades/(?P<id_discapacidad>[\w]+)/eliminar$', eliminar_discapacidad),
    url(r'^discapacidades/(?P<id_discapacidad>[\w]+)/modificar$', modificar_discapacidad),
    # url(r'^discapacidades/(?P<id_discapacidad>[\w]+)/activar$', activar_discapacidad),


    # ASOCIACIONES
    url(r'^asociaciones$', gestion_asociaciones, name='asociaciones'),
    url(r'^asociaciones/registrar$', registrar_asociacion, name='registrar_asociacion'),
    url(r'^asociaciones/(?P<id_asociacion>[\w]+)/eliminar$', eliminar_asociacion),
    url(r'^asociaciones/(?P<id_asociacion>[\w]+)/modificar$', modificar_asociacion),
    # url(r'^asociaciones/(?P<id_asociacion>[\w]+)/activar$', activar_asociacion),


    # DESVINCULADOS
    url(r'^desvinculados$', listado_desvinculados, name="listar_desvinculados"),
    url(r'^desvinculados/registrar$', registrar_desvinculado, name="registrar_desvinculado"),
    url(r'^desvinculados/(?P<id_desvinculado>[\w]+)/dar_baja', dar_baja_desvinculado, name="dar_baja_desvinculado"),
    url(r'^desvinculados/(?P<id_desvinculado>[\w]+)/modificar', modificar_desvinculado, name="modificar_desvinculado"),
    url(r'^desvinculados/(?P<id_desvinculado>[\d]+)$', detalle_desvinculado, name='detalle_desvinculado'),
    url(r'^desvinculados/(?P<id_desvinculado>[\d]+)/re_incorporar', re_incorporar_desvinculado,
        name='re_incorporar_desvinculado'),
    url(r'^desvinculados/(?P<id_desvinculado>[\w]+)/ubicar_desvinculado', ubicar_desvinculado, name="ubicar_desvinculado"),
    url(r'^desvinculados/ci/(?P<ci>[\d]+)$', buscar_ci_desvinculados),
    url(r'^desvinculados/habilitar_usando_ci', habilitar_desvinculado, name="habilitar_desvinculado"),

    # REPORTES
    url(r'^desvinculados/reportes$', reportes_desvinculados, name="reportes_desvinculados"),

    # TECNICOS MEDIOS, OBREROS CALIFICADOS Y ESCUELAS DE OFICIO
    url(r'^tecnicosmedios_obreroscalificados_escuelasoficio$', listado_tm_oc_eo, name="listar_tm_oc_eo"),
    url(r'^tecnicosmedios_obreroscalificados_escuelasoficio/registrar$', registrar_tm_oc_eo, name="registrar_tm_oc_eo"),
    url(r'^tecnicosmedios_obreroscalificados_escuelasoficio/(?P<id_tm_oc_eo>[\w]+)/dar_baja', dar_baja_tm_oc_eo,
        name="dar_baja_tm_oc_eo"),
    url(r'^tecnicosmedios_obreroscalificados_escuelasoficio/(?P<id_tm_oc_eo>[\w]+)/modificar', modificar_tm_oc_eo,
        name="modificar_tm_oc_eo"),
    url(r'^tecnicosmedios_obreroscalificados_escuelasoficio/(?P<id_tm_oc_eo>[\d]+)$', detalle_tm_oc_eo,
        name='detalle_tm_oc_eo'),
    url(r'^tecnicosmedios_obreroscalificados_escuelasoficio/(?P<id_tm_oc_eo>[\d]+)/re_incorporar',
        re_incorporar_tm_oc_eo, name='re_incorporar_tm_oc_eo'),
    url(r'^tecnicosmedios_obreroscalificados_escuelasoficio/ci/(?P<ci>[\d]+)$', buscar_ci_tm_oc_eo),
    url(r'^tecnicosmedios_obreroscalificados_escuelasoficio/habilitar_usando_ci', habilitar_tm_oc_eo, name="habilitar_tm_oc_eo"),
    # REPORTES
    url(r'^tecnicosmedios_obreroscalificados_escuelasoficio/reportes$', reportes_tm_oc_eo, name="reportes_tm_oc_eo"),

    # EGRESADOS DE ESCUELAS ESPECIALES
    url(r'^egresados_escuelas_especiales$', listado_egresados_escuelas_especiales,
        name="listar_egresados_escuelas_especiales"),
    url(r'^egresados_escuelas_especiales/registrar$', registrar_egresado_escuela_especial,
        name="registrar_egresado_escuela_especial"),
    url(r'^egresados_escuelas_especiales/(?P<id_egresado_escuela_especial>[\w]+)/dar_baja',
        dar_baja_egresado_escuela_especial, name="dar_baja_egresado_escuela_especial"),
    url(r'^egresados_escuelas_especiales/(?P<id_egresado_escuela_especial>[\w]+)/modificar',
        modificar_egresado_escuela_especial, name="modificar_egresado_escuela_especial"),
    url(r'^egresados_escuelas_especiales/(?P<id_egresado_escuela_especial>[\d]+)$', detalle_egresado_escuela_especial,
        name='detalle_egresado_escuela_especial'),
    url(r'^egresados_escuelas_especiales/(?P<id_egresado_escuela_especial>[\d]+)/re_incorporar',
        re_incorporar_egresado_escuela_especial, name='re_incorporar_egresado_escuela_especial'),
    url(r'^egresados_escuelas_especiales/ci/(?P<ci>[\d]+)$', buscar_ci_egresados_escuelas_especiales),
    url(r'^egresados_escuelas_especiales/habilitar_usando_ci', habilitar_egresados_escuelas_especiales, name="habilitar_egresados_escuelas_especiales"),
    # REPORTES
    url(r'^egresados_escuelas_especiales/reportes$', reportes_egresados_escuelas_especiales,
        name="reportes_egresados_escuelas_especiales"),

    # EGRESADOS DE ESCUELAS DE CONDUCTA
    url(r'^egresados_escuelas_conducta$', listado_egresados_escuelas_conducta,
        name="listar_egresados_escuelas_conducta"),
    url(r'^egresados_escuelas_conducta/registrar$', registrar_egresado_escuela_conducta,
        name="registrar_egresado_escuela_conducta"),
    url(r'^egresados_escuelas_conducta/(?P<id_egresado_escuela_conducta>[\w]+)/dar_baja',
        dar_baja_egresado_escuela_conducta, name="dar_baja_egresado_escuela_conducta"),
    url(r'^egresados_escuelas_conducta/(?P<id_egresado_escuela_conducta>[\w]+)/modificar',
        modificar_egresado_escuela_conducta, name="modificar_egresado_escuela_conducta"),
    url(r'^egresados_escuelas_conducta/(?P<id_egresado_escuela_conducta>[\d]+)$', detalle_egresado_escuela_conducta,
        name='detalle_egresado_escuela_conducta'),
    url(r'^egresados_escuelas_conducta/(?P<id_egresado_escuela_conducta>[\d]+)/re_incorporar',
        re_incorporar_egresado_escuela_conducta, name='re_incorporar_egresado_escuela_conducta'),
    url(r'^egresados_escuelas_conducta/ci/(?P<ci>[\d]+)$', buscar_ci_egresados_escuelas_conducta),
    url(r'^egresados_escuelas_conducta/habilitar_usando_ci', habilitar_egresado_escuela_conducta,
        name="habilitar_egresado_escuela_conducta"),
    # REPORTES
    url(r'^egresados_escuelas_conducta/reportes$', reportes_egresados_escuelas_conducta,
        name="reportes_egresados_escuelas_conducta"),

    # EGRESADOS DE LA EFI
    url(r'^egresados_efi$', listado_egresados_efi, name="listar_egresados_efi"),
    url(r'^egresados_efi/registrar$', registrar_egresado_efi, name="registrar_egresado_efi"),
    url(r'^egresados_efi/(?P<id_egresado_efi>[\w]+)/dar_baja', dar_baja_egresado_efi, name="dar_baja_egresado_efi"),
    url(r'^egresados_efi/(?P<id_egresado_efi>[\w]+)/modificar', modificar_egresado_efi, name="modificar_egresado_efi"),
    url(r'^egresados_efi/(?P<id_egresado_efi>[\d]+)$', detalle_egresado_efi, name='detalle_egresado_efi'),
    url(r'^egresados_efi/(?P<id_egresado_efi>[\d]+)/re_incorporar', re_incorporar_egresado_efi, name='re_incorporar_egresado_efi'),
    url(r'^egresados_efi/ci/(?P<ci>[\d]+)$', buscar_ci_egresado_efi),
    url(r'^egresados_efi/habilitar_usando_ci', habilitar_egresado_efi, name="habilitar_egresado_efi"),
    # REPORTES
    url(r'^egresados_efi/reportes$', reportes_egresados_efi, name="reportes_egresados_efi"),

    # MENORES
    url(r'^menores$', listado_menores, name="listar_menores"),
    url(r'^menores/registrar$', registrar_menor, name="registrar_menor"),
    url(r'^menores/(?P<id_menor>[\w]+)/dar_baja', dar_baja_menor, name="dar_baja_menor"),
    url(r'^menores/(?P<id_menor>[\w]+)/modificar', modificar_menor, name="modificar_menor"),
    url(r'^menores/(?P<id_menor>[\d]+)$', detalle_menor, name='detalle_menor'),
    url(r'^menores/(?P<id_menor>[\d]+)/re_incorporar', re_incorporar_menor, name='re_incorporar_menor'),
    url(r'^menores/ci/(?P<ci>[\d]+)$', buscar_ci_menor),
    url(r'^menores/habilitar_usando_ci', habilitar_menor, name="habilitar_menor"),
    # REPORTES
    url(r'^menores/reportes$', reportes_menores, name="reportes_menores"),

    # DISCAPACITADOS
    url(r'^discapacitados$', listado_discapacitados, name="listar_discapacitados"),
    url(r'^discapacitados/registrar$', registrar_discapacitado, name="registrar_discapacitado"),
    url(r'^discapacitados/(?P<id_discapacitado>[\w]+)/dar_baja', dar_baja_discapacitado, name="dar_baja_discapacitado"),
    url(r'^discapacitados/(?P<id_discapacitado>[\w]+)/modificar', modificar_discapacitado,
        name="modificar_discapacitado"),
    url(r'^discapacitados/(?P<id_discapacitado>[\d]+)$', detalle_discapacitado, name='detalle_discapacitado'),
    url(r'^discapacitados/(?P<id_discapacitado>[\d]+)/re_incorporar', re_incorporar_discapacitado, name='re_incorporar_discapacitado'),
    url(r'^discapacitados/ci/(?P<ci>[\d]+)$', buscar_ci_discapacitado),
    url(r'^discapacitados/habilitar_usando_ci', habilitar_discapacitado, name="habilitar_discapacitado"),
    # REPORTES
    url(r'^discapacitados/reportes$', reportes_discapacitados, name="reportes_discapacitados"),

    # PERSONAS DE RIESGO
    url(r'^personas_riesgo$', listado_personas_riesgo, name="listar_personas_riesgo"),
    url(r'^personas_riesgo/registrar$', registrar_personas_riesgo, name="registrar_personas_riesgo"),
    url(r'^personas_riesgo/(?P<id_persona_riesgo>[\w]+)/dar_baja', dar_baja_persona_riesgo,
        name="dar_baja_persona_riesgo"),
    url(r'^personas_riesgo/(?P<id_persona_riesgo>[\w]+)/modificar', modificar_personas_riesgo,
        name="modificar_persona_riesgo"),
    url(r'^personas_riesgo/(?P<id_persona_riesgo>[\d]+)$', detalle_persona_riesgo, name='detalle_persona_riesgo'),
    url(r'^personas_riesgo/(?P<id_persona_riesgo>[\d]+)/re_incorporar', re_incorporar_persona_riesgo, name='re_incorporar_persona_riesgo'),
    url(r'^personas_riesgo/ci/(?P<ci>[\d]+)$', buscar_ci_persona_riesgo),
    url(r'^personas_riesgo/habilitar_usando_ci', habilitar_persona_riesgo, name="habilitar_persona_riesgo"),
    # REPORTES
    url(r'^personas_riesgo/reportes$', reportes_personas_riesgo, name="reportes_personas_riesgo"),

    # PETICIONES AJAXs

    url(r'^peticion_ajax/$', login_required(PeticionAjax.as_view())),
    url(r'^peticion_ajax/seleccionar_carreras/$', login_required(PeticionAjaxSeleccionarCarreras.as_view())),
    url(r'^peticion_ajax/filtrar_entidades_empleo_estatal/$', login_required(PeticionAjaxFiltrarEntidadesEmpleoEstatal.as_view())),
    url(r'^peticion_ajax/filtrar_entidades_interruptos/$', login_required(PeticionAjaxFiltrarEntidadesInterruptos.as_view())),
    url(r'^peticion_ajax/filtrar_entidades_interruptos_modificar/$', login_required(PeticionAjaxFiltrarEntidadesInterruptosModificar.as_view())),

    # CAUSALES DE INTERRUPCION
    url(r'^causales_interrupcion$', gestion_causales_interrupcion, name='causales_interrupcion'),
    url(r'^causales_interrupcion/registrar$', registrar_causal_interrupcion, name='registrar_causal_interrupcion'),
    url(r'^causales_interrupcion/(?P<id_causal_interrupcion>[\w]+)/eliminar$', eliminar_causal_interrupcion),
    url(r'^causales_interrupcion/(?P<id_causal_interrupcion>[\w]+)/modificar$', modificar_causal_interrupcion),

    # CAUSALES DE NO REINCORPORACION
    url(r'^causales_no_reincorporacion$', gestion_causales_no_reincorporacion, name='causales_no_reincorporacion'),
    url(r'^causales_no_reincorporacion/registrar$', registrar_causal_no_reincorporacion, name='registrar_causal_no_reincorporacion'),
    url(r'^causales_no_reincorporacion/(?P<id_causal_no_reincorporacion>[\w]+)/eliminar$', eliminar_causal_no_reincorporacion),
    url(r'^causales_no_reincorporacion/(?P<id_causal_no_reincorporacion>[\w]+)/modificar$', modificar_causal_no_reincorporacion, name='modificar_causal_no_reincorporacion'),

    # ACTIVIDADES DE INTERRUPTOS
    url(r'^actividades_interrupto$', gestion_actividades_interrupto, name='actividades_interrupto'),
    url(r'^actividades_interrupto/registrar$', registrar_actividad_interrupto, name='registrar_actividad_interrupto'),
    url(r'^actividades_interrupto/(?P<id_actividad>[\w]+)/eliminar$', eliminar_actividad_interrupto),
    url(r'^actividades_interrupto/(?P<id_actividad>[\w]+)/modificar$', modificar_actividad_interrupto),


    # INTERRUPTOS
    url(r'^interruptos$', gestion_interruptos, name='interruptos'),
    url(r'^interruptos/registrar$', registrar_interrupto, name='registrar_interrupto'),
    url(r'^interruptos/(?P<id_interrupto>[\w]+)/eliminar$', eliminar_interrupto),
    url(r'^interruptos/(?P<id_interrupto>[\w]+)/modificar$', modificar_interrupto, name='modificar_interrupto'),
    url(r'^interruptos/(?P<id_interrupto>[\w]+)/informe_valorativo$', descargar_informe_valorativo, name='informe_valorativo'),
    url(r'^interruptos/(?P<id_interrupto>[\w]+)$', detalles_interrupto, name='detalles_interrupto'),

    # ORGANISMOS AUTORIZADOS A REGISTRAR INTERRUPTOS FUERA DEL PLAZO
    url(r'^organismos_autorizados$', gestion_organismos_autorizados, name='gestion_organismos_autorizados'),
    url(r'^organismos_autorizados/autorizar_organismo$', autorizar_organismo, name='autorizar_organismo'),
    url(r'^organismos_autorizados/(?P<id_organismo_autorizado>[\w]+)/eliminar$', eliminar_organismo_autorizado),

    # REPORTES EMPLEO ESTATAL
    url(r'^reportes/reporte_nominal$', reporte_nominal, name='reporte_nominal'),
    url(r'^reportes/reporte_nominal_cierre_mes$', reporte_nominal_cierre_mes, name='reporte_nominal_cierre_mes'),
    url(r'^reportes/totales_fuentes_procedencia$', totales_fuentes_procedencia, name='totales_fuentes_procedencia'),
    url(r'^reportes/totales_fuentes_procedencia_cierre_mes$', totales_fuentes_procedencia_cierre_mes, name='totales_fuentes_procedencia_cierre_mes'),
    # url(r'^reportes/reporte_c$', comportamiento_figuras_priorizadas_filtrar_municipio, name='comportamiento_figuras_priorizadas_filtrar_municipio'),
    # url(r'^reportes/reporte_d$', comportamiento_figuras_priorizadas_general_provincias, name='comportamiento_figuras_priorizadas_general_provincias'),
    # url(r'^reportes/reporte_f$', comportamiento_figuras_priorizadas_filtrar_mes, name='comportamiento_figuras_priorizadas_filtrar_mes'),
    url(r'^reportes/total_personas_ubicadas_provincias$', total_personas_ubicadas_provincias, name='total_personas_ubicadas_provincias'),
    url(r'^reportes/total_personas_ubicadas_provincias_cierre_mes$', total_personas_ubicadas_provincias_cierre_mes, name='total_personas_ubicadas_provincias_cierre_mes'),
    url(r'^reportes/total_personas_ubicadas_provincias_y_municipios$', total_personas_ubicadas_provincias_y_municipios, name='total_personas_ubicadas_provincias_y_municipios'),
    url(r'^reportes/total_personas_ubicadas_provincias_y_municipios_cierre_mes$', total_personas_ubicadas_provincias_y_municipios_cierre_mes, name='total_personas_ubicadas_provincias_y_municipios_cierre_mes'),
    url(r'^reportes/total_personas_no_ubicadas_provincias$', total_personas_no_ubicadas_provincias, name='total_personas_no_ubicadas_provincias'),
    url(r'^reportes/total_personas_no_ubicadas_provincias_cierre_mes$', total_personas_no_ubicadas_provincias_cierre_mes, name='total_personas_no_ubicadas_provincias_cierre_mes'),
    url(r'^reportes/total_personas_no_ubicadas_provincias_y_municipios$', total_personas_no_ubicadas_provincias_y_municipios, name='total_personas_no_ubicadas_provincias_y_municipios'),
    url(r'^reportes/total_personas_no_ubicadas_provincias_y_municipios_cierre_mes$', total_personas_no_ubicadas_provincias_y_municipios_cierre_mes, name='total_personas_no_ubicadas_provincias_y_municipios_cierre_mes'),
    url(r'^reportes/no_ubicados_por_no_existir_oferta$', no_ubicados_por_no_existir_oferta, name='no_ubicados_por_no_existir_oferta'),
    url(r'^reportes/no_ubicados_por_no_existir_oferta_cierre_mes$', no_ubicados_por_no_existir_oferta_cierre_mes, name='no_ubicados_por_no_existir_oferta_cierre_mes'),
    url(r'^reportes/comportamiento_figuras_priorizadas_organismos$', comportamiento_figuras_priorizadas_organismos, name='comportamiento_figuras_priorizadas_organismos'),
    url(r'^reportes/comportamiento_figuras_priorizadas_organismos_cierre_mes$', comportamiento_figuras_priorizadas_organismos_cierre_mes, name='comportamiento_figuras_priorizadas_organismos_cierre_mes'),
    url(r'^reportes/desvinculados_no_ubicados_por_causales$', desvinculados_no_ubicados_por_causales, name='desvinculados_no_ubicados_por_causales'),
    url(r'^reportes/desvinculados_no_ubicados_por_causales_cierre_mes$', desvinculados_no_ubicados_por_causales_cierre_mes, name='desvinculados_no_ubicados_por_causales_cierre_mes'),
    url(r'^reportes/tecnicos_medios_pendientes_por_no_existir_oferta$', tecnicos_medios_pendientes_por_no_existir_oferta, name='tecnicos_medios_pendientes_por_no_existir_oferta'),
    url(r'^reportes/tecnicos_medios_pendientes_por_no_existir_oferta_cierre_mes$', tecnicos_medios_pendientes_por_no_existir_oferta_cierre_mes, name='tecnicos_medios_pendientes_por_no_existir_oferta_cierre_mes'),
    url(r'^reportes/obreros_calificados_pendientes_por_no_existir_oferta$', obreros_calificados_pendientes_por_no_existir_oferta, name='obreros_calificados_pendientes_por_no_existir_oferta'),
    url(r'^reportes/obreros_calificados_pendientes_por_no_existir_oferta_cierre_mes$', obreros_calificados_pendientes_por_no_existir_oferta_cierre_mes, name='obreros_calificados_pendientes_por_no_existir_oferta_cierre_mes'),
    url(r'^reportes/escuelas_oficio_pendientes_por_no_existir_oferta$', escuelas_oficio_pendientes_por_no_existir_oferta, name='escuelas_oficio_pendientes_por_no_existir_oferta'),
    url(r'^reportes/escuelas_oficio_pendientes_por_no_existir_oferta_cierre_mes$', escuelas_oficio_pendientes_por_no_existir_oferta_cierre_mes, name='escuelas_oficio_pendientes_por_no_existir_oferta_cierre_mes'),
    url(r'^reportes/mujeres_ubicadas_por_fuentes$', mujeres_ubicadas_por_fuentes, name='mujeres_ubicadas_por_fuentes'),
    url(r'^reportes/mujeres_ubicadas_por_fuentes_cierre_mes$', mujeres_ubicadas_por_fuentes_cierre_mes, name='mujeres_ubicadas_por_fuentes_cierre_mes'),
    url(r'^reportes/mujeres_no_ubicadas_por_fuentes$', mujeres_no_ubicadas_por_fuentes, name='mujeres_no_ubicadas_por_fuentes'),
    url(r'^reportes/mujeres_no_ubicadas_por_fuentes_cierre_mes$', mujeres_no_ubicadas_por_fuentes_cierre_mes, name='mujeres_no_ubicadas_por_fuentes_cierre_mes'),
    url(r'^reportes/menores_ubicados_por_sector$', menores_ubicados_por_sector, name='menores_ubicados_por_sector'),
    url(r'^reportes/menores_ubicados_por_sector_cierre_mes$', menores_ubicados_por_sector_cierre_mes, name='menores_ubicados_por_sector_cierre_mes'),
    url(r'^reportes/menores_ubicados_por_especialidad$', menores_ubicados_por_especialidad, name='menores_ubicados_por_especialidad'),
    url(r'^reportes/menores_ubicados_por_especialidad_cierre_mes$', menores_ubicados_por_especialidad_cierre_mes, name='menores_ubicados_por_especialidad_cierre_mes'),
    url(r'^reportes/obreros_calificados_pendientes_por_causales$', obreros_calificados_pendientes_por_causales, name='obreros_calificados_pendientes_por_causales'),
    url(r'^reportes/obreros_calificados_pendientes_por_causales_cierre_mes$', obreros_calificados_pendientes_por_causales_cierre_mes, name='obreros_calificados_pendientes_por_causales_cierre_mes'),
    url(r'^reportes/total_interruptos_por_organismos_cap$', total_interruptos_por_organismos_cap, name='total_interruptos_por_organismos_cap'),

    # REPORTES INTERRUPTOS
    url(r'^reportes/interruptos_por_organismos$', interruptos_por_organismos, name='interruptos_por_organismos'),
    url(r'^reportes/interruptos_por_organismos_sin_entidades$', interruptos_por_organismos_sin_entidades, name='interruptos_por_organismos_sin_entidades'),
    url(r'^reportes/interruptos_por_organismos_filtros$', interruptos_por_organismos_filtros, name='interruptos_por_organismos_filtros'),
    url(r'^reportes/interruptos_por_provincias$', interruptos_por_provincias, name='interruptos_por_provincias'),
    url(r'^reportes/interruptos_por_provincias_sin_entidades$', interruptos_por_provincias_sin_entidades, name='interruptos_por_provincias_sin_entidades'),
    url(r'^reportes/interruptos_por_actividades$', interruptos_por_actividades, name='interruptos_por_actividades'),
    url(r'^reportes/interruptos_por_actividades_sin_entidades$', interruptos_por_actividades_sin_entidades, name='interruptos_por_actividades_sin_entidades'),
    url(r'^reportes/interruptos_por_causas_interrupcion$', interruptos_por_causas_interrupcion, name='interruptos_por_causas_interrupcion'),
    url(r'^reportes/interruptos_por_causas_interrupcion_sin_entidades$', interruptos_por_causas_interrupcion_sin_entidades, name='interruptos_por_causas_interrupcion_sin_entidades'),
    url(r'^reportes/interruptos_reubicados$', interruptos_situacion_duracion, name='interruptos_situacion_duracion'),


    # SEGUIMIENTO A JOVENES QUE ABANDONAN EL NIVEL SUPERIOR
    url(r'^seguimiento_jovenes_abandonan_nivel_superior$', gestion_jovenes_abandonan_nivel_superior, name='gestion_jovenes_abandonan_nivel_superior'),
    url(r'^seguimiento_jovenes_abandonan_nivel_superior/registrar$', registrar_joven_abandona_nivel_superior, name='registrar_joven_abandona_nivel_superior'),
    url(r'^seguimiento_jovenes_abandonan_nivel_superior/(?P<id_joven>[\w]+)/eliminar$', eliminar_joven_abandona_nivel_superior, name='eliminar_joven_abandona_nivel_superior'),
    url(r'^seguimiento_jovenes_abandonan_nivel_superior/(?P<id_joven>[\w]+)/modificar$', modificar_joven_abandona_nivel_superior, name='modificar_joven_abandona_nivel_superior'),
    url(r'^seguimiento_jovenes_abandonan_nivel_superior/(?P<id_joven>[\w]+)/proceso_trabajo_social$', proceso_trabajador_social_jans, name='proceso_trabajador_social_jans'),
    url(r'^seguimiento_jovenes_abandonan_nivel_superior/(?P<id_joven>[\w]+)/proceso_direccion_trabajo$', proceso_direccion_empleo_jans, name='proceso_direccion_empleo_jans'),
    url(r'^seguimiento_jovenes_abandonan_nivel_superior/(?P<id_joven>[\w]+)/control$', proceso_control_jans, name='proceso_control_jans'),
    url(r'^seguimiento_jovenes_abandonan_nivel_superior/(?P<id_joven>[\w]+)$', detalles_joven_abandona_nivel_superior, name='detalles_joven_abandona_nivel_superior'),
    url(r'^jovenes_abandonan_nivel_superior/importar$', importar_jovenes_abandonan),

    # ASOCIACIONES
    url(r'^causales_no_requieren_empleo$', gestion_causales_no_requieren_empleo, name='gestion_causales_no_requieren_empleo'),
    url(r'^causales_no_requieren_empleo/registrar$', registrar_causal_no_requiere_empleo, name='registrar_causal_no_requiere_empleo'),
    # url(r'^causales_no_requieren_empleo/(?P<id_causa>[\w]+)/eliminar$', eliminar_causal_no_requiere_empleo),
    # url(r'^causales_no_requieren_empleo/(?P<id_causa>[\w]+)/modificar$', modificar_causal_no_requiere_empleo),
    # # url(r'^causales_no_requieren_empleo/(?P<id_causa>[\w]+)/activar$', activar_causal_no_requiere_empleo),

    # CAUSALES DE INTERRUPCION
    url(r'^causales_desvinculacion_ns$', gestion_causales_desvinculacion_ns, name='causales_desvinculacion_ns'),
    url(r'^causales_desvinculacion_ns/registrar$', registrar_causal_desvinculacion_ns, name='registrar_causal_desvinculacion_ns'),
    url(r'^causales_desvinculacion_ns/(?P<id_causal_desvinculacion_ns>[\w]+)/modificar$', modificar_causal_desvinculacion_ns, name='modificar_causal_desvinculacion_ns'),
    url(r'^causales_desvinculacion_ns/(?P<id_causal_desvinculacion_ns>[\w]+)/eliminar$', eliminar_causal_desvinculacion_ns),

    # DESCARGAR GFORZA
    url(r'^descargar_gforza', descargar_gforza, name='descargar_gforza'),

    # ---------------codigo de daniel (FIN)---------------

]