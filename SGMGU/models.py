# -*- coding: utf-8 -*-
import re

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from django.contrib.sessions.models import Session
from django.core.exceptions import ValidationError
from django.utils import timezone

from views.utiles import obtener_edad


class Organismo(models.Model):
    nombre = models.CharField(max_length=250)
    siglas = models.CharField(max_length=20)
    activo = models.BooleanField(default=True)
    hijode = models.ForeignKey('self', blank=True, null=True)

    def __unicode__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]


class Categoria_usuario(models.Model):
    nombre = models.CharField(max_length=256)

    def __unicode__(self):
        return self.nombre


class Provincia(models.Model):
    nombre = models.CharField(max_length=250)
    siglas = models.CharField(max_length=255)

    def __unicode__(self):
        return self.nombre

    class Meta:
        ordering = ["id"]


class Municipio(models.Model):
    codigo_mes = models.CharField(max_length=100, blank=True, null=True)
    nombre = models.CharField(max_length=250)
    provincia = models.ForeignKey(Provincia)

    def __unicode__(self):
        return "%s" % (self.nombre)

    class Meta:
        ordering = ["nombre"]


class MunicipioEntidad(models.Model):
    codigo_mes = models.IntegerField(primary_key=True)
    id = models.IntegerField()
    nombre = models.CharField(max_length=250)
    provincia = models.ForeignKey(Provincia)

    def __unicode__(self):
        return "%s" % (self.nombre)

    class Meta:
        ordering = ["nombre"]


class Centro_estudio(models.Model):
    codigo_mes = models.CharField(max_length=100, blank=True, null=True)
    nombre = models.CharField(max_length=1000)
    siglas = models.CharField(max_length=20, blank=True, null=True)
    activo = models.BooleanField(default=True)
    provincia = models.ForeignKey(Provincia, blank=True, null=True)

    def __unicode__(self):
        return "%s" % (self.nombre)


class Perfil_usuario(models.Model):
    usuario = models.OneToOneField(User)
    foto = models.ImageField(upload_to='uploads/img_usuarios/', blank=True, null=True)
    organismo = models.ForeignKey(Organismo)
    telefono = models.CharField(max_length=250, blank=True, null=True)
    categoria = models.ForeignKey(Categoria_usuario)
    provincia = models.ForeignKey(Provincia, blank=True, null=True)
    municipio = models.ForeignKey(Municipio, blank=True, null=True)
    universidad = models.ForeignKey(Centro_estudio, blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __unicode__(self):
        return self.usuario.username

    class Meta:
        verbose_name_plural = "Perfiles de usuarios"
        verbose_name = "Perfil de usuario"


class Notificacion(models.Model):
    emisor = models.ForeignKey(User, related_name="emisores")
    remitente = models.ForeignKey(User, related_name="remitentes")
    texto = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    revisado = models.BooleanField(default=False)


class Carrera(models.Model):
    codigo_mes = models.CharField(max_length=100, blank=True, null=True)
    nombre = models.CharField(max_length=1000)
    activo = models.BooleanField(default=True)
    tipo = models.CharField(max_length=90, choices=[
        ('nm', 'Nivel Medio'),
        ('ns', 'Nivel Superior'),
        ('oc', 'Obrero Calificado'),
        ('eo', 'Escuela de Oficio')
    ])

    def __unicode__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]

    def get_codigo_mes(self):
        return self.codigo_mes if self.codigo_mes else ''


class Causal_movimiento(models.Model):
    nombre = models.CharField(max_length=500)
    tipo = models.CharField(max_length=90, choices=[
        ('ml', 'Movimiento Laboral'),
        ('i', 'Inhabilitación'),
        ('f', 'Fluctuación')
    ])
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Causales"

    def __unicode__(self):
        return self.nombre


class Persona(models.Model):
    nombre = models.CharField(max_length=250)

    class Meta:
        ordering = ["nombre"]

    def __unicode__(self):
        return "%s" % (self.nombre)


from django.core.validators import RegexValidator


class Graduado(Persona):
    ci = models.CharField(max_length=11, blank=True, null=True, validators=[RegexValidator(
        regex='^[0-9]{2}(0[1-9]|1[0-2])(31|30|(0[1-9]|[1-2][0-9]))[0-9]{5}$',
        message='CI incorrecto',
    )])
    carrera = models.ForeignKey(Carrera, null=True, blank=True)
    anno_graduacion = models.IntegerField()
    centro_estudio = models.ForeignKey(Centro_estudio, null=True, blank=True)
    codigo_boleta = models.CharField(null=True, blank=True, max_length=250)
    imagen_boleta = models.ImageField(upload_to='uploads/img_boletas/', blank=True, null=True)
    detalle_direccion_residencia = models.CharField(max_length=500, null=True, blank=True)
    provincia_direccion_residencia = models.ForeignKey(Provincia, null=True, blank=True)
    municipio_direccion_residencia = models.ForeignKey(Municipio, null=True, blank=True)


class Facultado(Persona):
    cargo = models.CharField(max_length=250, blank=True, null=True)
    activo = models.BooleanField(default=True)
    organismo = models.ForeignKey(Organismo)


class Expediente(models.Model):
    graduado = models.OneToOneField(Graduado, null=True, blank=True)
    entidad_liberacion = models.CharField(max_length=500, null=True, blank=True)
    entidad_aceptacion = models.CharField(max_length=500, null=True, blank=True)
    mun_entidad_liberacion = models.ForeignKey(Municipio, related_name="municipio_liberacion", null=True, blank=True)
    mun_entidad_aceptacion = models.ForeignKey(Municipio, related_name="municipio_aceptacion", null=True, blank=True)
    causal_movimiento = models.ForeignKey(Causal_movimiento, null=True, blank=True)
    sintesis_causal_movimiento = models.CharField(max_length=1000, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "Expediente del graudado %s" % (self.graduado.nombre)


class Expediente_movimiento_interno(Expediente):
    aprobado_por = models.CharField(max_length=500)
    organismo = models.ForeignKey(Organismo)


class Expediente_movimiento_externo(Expediente):
    organismo_liberacion = models.ForeignKey(Organismo, related_name="organismo_liberacion")
    organismo_aceptacion = models.ForeignKey(Organismo, related_name="organismo_aceptacion")
    facultado_liberacion = models.CharField(max_length=250, null=True, blank=True)
    facultado_aceptacion = models.CharField(max_length=250, null=True, blank=True)
    comprimido = models.FileField(upload_to='uploads/adjuntos_expedientes/', null=True, blank=True)


class Expediente_rechazado(models.Model):
    expediente = models.ForeignKey(Expediente_movimiento_externo)
    fecha_rechazo = models.DateTimeField(auto_now=True)
    sintesis_rechazo = models.CharField(max_length=500)

    def __unicode__(self):
        return "Expediente del graudado %s" % (self.expediente.graduado.nombre)


class Expediente_pendiente(models.Model):
    expediente = models.ForeignKey(Expediente_movimiento_externo)
    fecha_pendiente = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "Expediente del graudado %s" % (self.expediente.graduado.nombre)


class Expediente_aprobado(models.Model):
    codigo_DE_RE = models.CharField(max_length=250, null=True, blank=True)
    codigo_DE_RS = models.CharField(max_length=250, null=True, blank=True, unique_for_year=True)
    expediente = models.ForeignKey(Expediente_movimiento_externo)
    fecha_aprobado = models.DateTimeField(default=datetime.now())
    carta_expediente = models.FileField(upload_to='uploads/cartas_expedientes/', blank=True, null=True)

    def __unicode__(self):
        return "Expediente del graudado %s" % (self.expediente.graduado.nombre)

    class Meta:
        ordering = ['-fecha_aprobado']


class Expediente_no_aprobado(models.Model):
    expediente = models.ForeignKey(Expediente_movimiento_externo)
    fecha_no_aprobado = models.DateTimeField(auto_now=True)
    sintesis_no_aprobado = models.CharField(max_length=500)

    def __unicode__(self):
        return "Expediente del graudado %s" % (self.expediente.graduado.nombre)


class Direccion_trabajo(models.Model):
    provincia = models.OneToOneField(Provincia)
    director = models.CharField(max_length=256, blank=True, null=True)
    sexo_director = models.CharField(max_length=30, blank=True, null=True)
    especialista = models.CharField(max_length=256, blank=True, null=True)
    correo_director = models.EmailField(blank=True, null=True)
    correo_especialista = models.EmailField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __unicode__(self):
        return "Dirección de Trabajo de %s".decode("utf-8") % (self.provincia.nombre)


class UbicacionLaboral(models.Model):
    ESTADOS_SEXO = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]

    boleta = models.CharField(max_length=15, blank=True, null=True)
    anno_graduado = models.IntegerField()
    centro_estudio = models.ForeignKey(Centro_estudio)
    carrera = models.ForeignKey(Carrera)
    ci = models.CharField(
        max_length=11,
        validators=[RegexValidator(regex='^[0-9]{2}(0[1-9]|1[0-2])(31|30|(0[1-9]|[1-2][0-9]))[0-9]{5}$',
                                   message='CI incorrecto', )],
        unique=True
    )
    nombre_apellidos = models.CharField(max_length=256)
    cumple_servicio_social = models.BooleanField()
    entidad = models.CharField(max_length=256)
    organismo = models.ForeignKey(Organismo)
    municipio_residencia = models.ForeignKey(Municipio, related_name="ubicacion_municipio_residencia")
    provincia_ubicacion = models.ForeignKey(Provincia, related_name="ubicacion_provincia_ubicacion")
    sexo = models.CharField(max_length=20)
    direccion_particular = models.CharField(max_length=256)
    presentado = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    causa_no_presentacion = models.TextField(null=True, blank=True)
    estado_ubicacion = models.CharField(max_length=20, choices=(('desfasado', 'Desfasado'), ('graduado', 'Graduado')))

    def sexo_verbose(self):
        return dict(UbicacionLaboral.ESTADOS_SEXO)[self.sexo]

    def css(self):
        if self.cumple_servicio_social:
            return "Si"
        else:
            return "No"

    def is_presentado(self):
        if self.presentado:
            return "Si"
        else:
            return "No"

    def __unicode__(self):
        return "Ubicacion de %s " % self.nombre_apellidos

    class Meta:
        ordering = ["-fecha_registro"]


class GraduadoInhabilitacion(models.Model):
    nombre_apellidos = models.CharField(max_length=256)
    ci = models.CharField(max_length=11, blank=True, null=True, validators=[RegexValidator(
        regex='^[0-9]{2}(0[1-9]|1[0-2])(31|30|(0[1-9]|[1-2][0-9]))[0-9]{5}$',
        message='CI incorrecto',
    )])

    carrera = models.ForeignKey(Carrera)
    nivel_educacional = models.CharField(max_length=90, choices=[
        ('Superior', 'NS'),
        ('Medio', 'NM'),
    ])
    cumple_servicio_social = models.CharField(max_length=90, choices=[
        ('Si', 'C'),
        ('No', 'NC'),
    ])

    provincia = models.ForeignKey(Provincia)
    organismo = models.ForeignKey(Organismo)
    fecha_registrado = models.DateTimeField(auto_now_add=True)

    def c_nc(self):
        if self.cumple_servicio_social == 'Si':
            return "C"
        else:
            return "NC"

    def nm_ns(self):
        if self.nivel_educacional == 'Superior':
            return "NS"
        else:
            return "NM"


class ProcesoInhabilitacion(models.Model):
    numero_resolucion = models.CharField(max_length=10, unique_for_year=True)
    graduado = models.ForeignKey(GraduadoInhabilitacion)
    fecha = models.DateTimeField(auto_now_add=True)
    causal = models.ForeignKey(Causal_movimiento, blank=True, null=True)
    proceso = models.CharField(max_length=90, choices=[
        ('i', 'Inhabilitación'),
        ('s', 'Suspensión de la Inhabilitación'),
    ])


class DisponibilidadGraduados(models.Model):
    ESTADOS_SEXO = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]

    centro_estudio = models.ForeignKey(Centro_estudio)
    carrera = models.ForeignKey(Carrera)
    cumple_servicio_social = models.BooleanField()
    ci = models.CharField(max_length=11, blank=True, null=True, validators=[RegexValidator(
        regex='^[0-9]{2}(0[1-9]|1[0-2])(31|30|(0[1-9]|[1-2][0-9]))[0-9]{5}$',
        message='CI incorrecto',
    )], unique=True)
    nombre_apellidos = models.CharField(max_length=256)
    municipio_residencia = models.ForeignKey(Municipio, related_name="disponibilidad_municipio_residencia")
    sexo = models.CharField(max_length=20)
    direccion_particular = models.CharField(max_length=256)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def sexo_verbose(self):
        return dict(DisponibilidadGraduados.ESTADOS_SEXO)[self.sexo]

    def __unicode__(self):
        return self.nombre_apellidos

    class Meta:
        ordering = ["-fecha_registro"]


# -----------codigo mario david--------------



class Tipo_Entidad(models.Model):
    identificador = models.CharField(primary_key=True, max_length=250)
    nombre_tipo = models.CharField(max_length=250)
    estado = models.BooleanField(default=True)

    def __unicode__(self):
        return self.nombre_tipo

    class Meta:
        ordering = ["nombre_tipo"]


class Entidad(models.Model):
    id_codigo_entidad = models.CharField(primary_key=True, max_length=250)
    e_nombre = models.CharField(max_length=250)
    id_organismo_s = models.ForeignKey(Organismo, blank=True, null=True)
    municipio = models.ForeignKey(MunicipioEntidad)
    estado = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(default=datetime.today())

    def __unicode__(self):
        return self.e_nombre

    class Meta:
        ordering = ["e_nombre"]


# class DemandaGraduados(models.Model):
#     codigo_demanda = models.IntegerField(primary_key=True,unique=True)
#     entidad = models.ForeignKey(Entidad,blank=True, null= True)
#     municipio_entidad = models.ForeignKey(Municipio,blank=True, null= True)
#     carrera = models.ForeignKey(Carrera,blank=True, null= True)
#     organismo = models.ForeignKey(Organismo,blank=True, null= True)
#     anno_realizacion = models.IntegerField(blank=True,null=True)
#     anno_mas_uno = models.IntegerField(blank=True,null=True)
#     anno_mas_dos = models.IntegerField(blank=True,null=True)
#     anno_mas_tres = models.IntegerField(blank=True,null=True)
#     anno_mas_cuatro = models.IntegerField(blank=True,null=True)
#     anno_mas_cinco = models.IntegerField(blank=True,null=True)
#     anno_mas_seis = models.IntegerField(blank=True,null=True)
#     anno_mas_siete = models.IntegerField(blank=True,null=True)
#     anno_mas_ocho = models.IntegerField(blank=True,null=True)
#     anno_mas_nueve = models.IntegerField(blank=True,null=True)
#     anno_mas_diez = models.IntegerField(blank=True,null=True)

# class Existencia(models.Model):
#     id_ocupados = models.IntegerField(primary_key=True,unique=True)
#     id_organismo = models.ForeignKey(Organismo,blank=True,null=True)
#     id_codigo_entidad = models.ForeignKey(Entidad,blank=True,null=True)
#     id_cod_carrera = models.ForeignKey(Carrera,blank=True,null=True)
#     id_municipio_ocupado = models.ForeignKey(Municipio,blank=True,null=True)
#     id_tipo_plaza = models.CharField(max_length=255,choices=[
#         ('CI', 'Indeterminado'),
#         ('CDSS', 'Determinado en cumplimiento del servicio social'),
#         ('RCCI', 'Reserva científica CI'),
#         ('RCCD', 'Reserva científica CD'),
#         ('DIC', 'Determinado ICRT y MINCULT')
#     ])
#     id_rango_edad = models.CharField(max_length=255,choices=[
#         ('-31','Menores de 31 años'),
#         ('31<x<50','De 31 a 50 años'),
#         ('51<x<60','De 51 a 60 años'),
#         ('+60','Mayores de 60 años'),
#     ])
#     cant_graduados = models.IntegerField(blank=True,null=True)
#     ano_realizacion = models.IntegerField(blank=True,null=True)

# class Fluctuacion(models.Model):
#     id_organismo = models.ForeignKey(Organismo,blank=True,null=True)
#     id_fluctuacion = models.IntegerField(primary_key=True,unique=True)
#     id_entidad = models.ForeignKey(Entidad,blank=True,null=True)
#     id_munic_entidad = models.ForeignKey(Municipio,blank=True,null=True)
#     id_causal = models.ForeignKey(Causal_movimiento,blank=True,null=True)
#     id_carrera = models.ForeignKey(Carrera,blank=True,null=True)
#     cantidad = models.IntegerField(blank=True,null=True)
#     anno_realizacion = models.IntegerField(blank=True,null=True)



# ---------------------------------------------

class CategoriaIndicacion(models.Model):
    nombre = models.CharField(max_length=256)

    def __unicode__(self): return self.nombre


class Indicacion(models.Model):
    titulo = models.CharField(max_length=256)
    categoria = models.ForeignKey(CategoriaIndicacion)
    texto = models.TextField()
    autor = models.ForeignKey(User)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fichero = models.FileField(upload_to='uploads/archivos_indicaciones/', blank=True, null=True)

    def get_nombre_fichero(self):
        if self.fichero:
            return self.fichero.name.split("/")[-1]
        else:
            return None

    class Meta:
        ordering = ["-fecha_registro"]
        verbose_name_plural = "Indicaciones"
        verbose_name = "Indicacion"


@receiver(post_save)
def limpiar_cache0(sender, instance, created, **kwargs):
    if created:
        if sender != Session:
            cache.clear()


@receiver(post_save)
def limpiar_cache1(sender, instance, **kwargs):
    if sender != Session:
        cache.clear()


@receiver(post_delete)
def limpiar_cache2(sender, **kwargs):
    if sender != Session:
        cache.clear()


@receiver(post_save, sender=User)
def actualizar_perfil(sender, instance, **kwargs):
    # instance.perfil_usuario.save()
    pass


# ---------------codigo de daniel (INICIO)---------------


class NivelEscolar(models.Model):
    nombre = models.CharField(max_length=255)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.nombre

    class Meta:
        ordering = ["id"]


class CausalNoIncorporado(models.Model):
    causa = models.CharField(max_length=255)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.causa

    class Meta:
        ordering = ["id"]


class CausalNoAceptacion(models.Model):
    causa = models.CharField(max_length=255)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.causa

    class Meta:
        ordering = ["id"]


class CausalBaja(models.Model):
    causa = models.CharField(max_length=255)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.causa


class CausalNoUbicado(models.Model):
    causa = models.CharField(max_length=255)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.causa


class Ubicacion(models.Model):
    ubicacion = models.CharField(max_length=255)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.ubicacion

    class Meta:
        ordering = ["id"]


class EstadoIncorporado(models.Model):
    estado = models.CharField(max_length=255)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.estado


def validation_ci_licenciadossma(value):
    if not re.match(u'[0-9]{2}((0[1-9])|(1[0-2]))((0[1-9])|([1-2][0-9])|(3[0-1]))[0-9]{5}$', value):
        raise ValidationError(
            'CI incorrecto.')
    ci = int(value)
    fecha = ci / 100000
    anno = fecha / 10000
    mes = (fecha / 100) % 100
    dia = fecha % 100
    if str(mes) == '2':
        if anno % 4 == 0 and dia > 29:
            raise ValidationError('CI incorrecto.')
        if anno % 4 != 0 and dia > 28:
            raise ValidationError('CI incorrecto.')
    if obtener_edad(value) < 18:
        raise ValidationError('No se aceptan menores de 18 años.')
    if obtener_edad(value) > 26:
        raise ValidationError('No se aceptan mayores de 26 años.')


class HistorialLicenciadosSMA(models.Model):
    id_licenciado_sma = models.IntegerField()
    municipio_solicita_empleo = models.ForeignKey(Municipio, related_name='mun_solicita_empleo_h_licenciado_sma')
    ubicacion = models.ForeignKey(Ubicacion)
    fecha_ubicacion = models.DateTimeField(auto_now_add=True)
    organismo = models.ForeignKey(Organismo)
    # AGREGAR LAS ACTIVIDADES DE TPCP
    entidad = models.ForeignKey(Entidad)
    municipio_entidad = models.ForeignKey(Municipio, related_name='mun_entidad_h_licenciado_sma')


class LicenciadosSMA(models.Model):
    ESTADOS_SEXO = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]

    nombre_apellidos = models.CharField(max_length=255)
    ci = models.CharField(max_length=11, unique=True, validators=[validation_ci_licenciadossma])
    edad = models.IntegerField()
    sexo = models.CharField(max_length=20)
    direccion_particular = models.CharField(max_length=255)
    nivel_escolar = models.ForeignKey(NivelEscolar)
    carrera = models.ForeignKey(Carrera, blank=True, null=True)
    municipio_residencia = models.ForeignKey(Municipio, related_name='municipio_recidencia_licenciado_sma')
    mes_entrevista = models.CharField(max_length=255)
    anno_entrevista = models.IntegerField()
    recibio_oferta = models.BooleanField()
    acepto_oferta = models.CharField(max_length=255, blank=True, null=True)
    causa_no_aceptacion = models.ForeignKey(CausalNoAceptacion, blank=True, null=True)
    # Ubicacion = Oferta seleccionada (son lo mismo)
    ubicacion = models.ForeignKey(Ubicacion, blank=True, null=True)
    fecha_ubicacion = models.DateTimeField(blank=True, null=True)
    organismo = models.ForeignKey(Organismo, blank=True, null=True)
    # AGREGAR LAS ACTIVIDADES DE TPCP
    entidad = models.ForeignKey(Entidad, blank=True, null=True)
    municipio_entidad = models.ForeignKey(Municipio, related_name='municipio_entidad_licenciado_sma', blank=True,
                                          null=True)
    causa_no_ubicado = models.ForeignKey(CausalNoUbicado, blank=True, null=True)
    incorporado = models.ForeignKey(EstadoIncorporado, blank=True, null=True)
    # fecha de la baja??????
    fecha_baja = models.DateTimeField(blank=True, null=True)
    causa_baja = models.ForeignKey(CausalBaja, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def sexo_verbose(self):
        return dict(LicenciadosSMA.ESTADOS_SEXO)[self.sexo]

    def ao(self):
        if self.acepto_oferta == "S":
            return "Si"
        elif self.acepto_oferta == "N":
            return "No"
        else:
            return "----"

    def ro(self):
        if self.recibio_oferta:
            return "Si"
        elif not self.recibio_oferta:
            return "No"
        else:
            return "----"


class ControlLicenciadosSMA(models.Model):
    ESTADOS_INCORPORADO = [
        ('S', 'Si'),
        ('N', 'No'),
        ('LD', 'Lo dejó'),
    ]
    # cambiar INCORPORADO  como ForeignKey(EstadoIncorporado)
    incorporado = models.CharField(max_length=255)
    ubicacion = models.ForeignKey(Ubicacion, blank=True, null=True)
    organismo = models.ForeignKey(Organismo, blank=True, null=True)
    entidad = models.ForeignKey(Entidad, blank=True, null=True)
    municipio = models.ForeignKey(Municipio, blank=True, null=True)
    causa_no_ubicado = models.ForeignKey(CausalNoUbicado, blank=True, null=True)
    licenciado_sma = models.ForeignKey(LicenciadosSMA)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def estados_incorporado(self):
        return dict(ControlLicenciadosSMA.ESTADOS_INCORPORADO)[self.incorporado]


class FuenteProcedencia(models.Model):
    nombre = models.CharField(max_length=255)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.nombre


class ComprobacionAnualEmpleoEstatal(models.Model):
    fuente_procedencia = models.ForeignKey(FuenteProcedencia)
    fecha_comprobacion = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.fuente_procedencia

    class Meta:
        ordering = ["id"]


class Delito(models.Model):
    nombre = models.CharField(max_length=255)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.nombre


class MotivoEgreso(models.Model):
    nombre = models.CharField(max_length=255)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.nombre


def validacion_ci_egresado_ep(value):
    if not re.match(u'[0-9]{2}((0[1-9])|(1[0-2]))((0[1-9])|([1-2][0-9])|(3[0-1]))[0-9]{5}$', value):
        raise ValidationError(
            'CI incorrecto.')
    ci = int(value)
    fecha = ci / 100000
    anno = fecha / 10000
    mes = (fecha / 100) % 100
    dia = fecha % 100
    if str(mes) == '2':
        if anno % 4 == 0 and dia > 29:
            raise ValidationError('CI incorrecto.')
        if anno % 4 != 0 and dia > 28:
            raise ValidationError('CI incorrecto.')
    if obtener_edad(value) < 17:
        raise ValidationError('No se aceptan menores de 17 años.')


class HistorialEgresadosYSancionados(models.Model):
    id_egresado_sancionado = models.IntegerField()
    municipio_solicita_empleo = models.ForeignKey(Municipio, related_name='mun_solicita_empleo_egresado_sancionado')
    ubicacion = models.ForeignKey(Ubicacion)
    fecha_ubicacion = models.DateTimeField(auto_now_add=True)
    organismo = models.ForeignKey(Organismo, blank=True, null=True)
    # AGREGAR LAS ACTIVIDADES DE TPCP
    entidad = models.ForeignKey(Entidad, blank=True, null=True)
    municipio_entidad = models.ForeignKey(Municipio, related_name='mun_entidad_egresado_sancionado', blank=True,
                                          null=True)


class EgresadosEstablecimientosPenitenciarios(models.Model):
    ESTADOS_SEXO = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]

    fuente_procedencia = models.ForeignKey(FuenteProcedencia)
    municipio_solicita_empleo = models.ForeignKey(Municipio, related_name='municipio_solicita_empleo')
    nombre_apellidos = models.CharField(max_length=255)
    ci = models.CharField(max_length=11, unique=True, validators=[validacion_ci_egresado_ep])
    edad = models.IntegerField()
    sexo = models.CharField(max_length=20)
    municipio_residencia = models.ForeignKey(Municipio, related_name='municipio_residencia')
    direccion_particular = models.CharField(max_length=255)
    delito = models.ForeignKey(Delito, blank=True, null=True)
    motivo_egreso = models.ForeignKey(MotivoEgreso, blank=True, null=True)
    nivel_escolar = models.ForeignKey(NivelEscolar)
    carrera = models.ForeignKey(Carrera, blank=True, null=True)
    ubicado = models.BooleanField()
    ubicacion = models.ForeignKey(Ubicacion, blank=True, null=True)
    # TODO: arreglar fecha de ubicacion
    fecha_ubicacion = models.DateTimeField(auto_now_add=True)
    organismo = models.ForeignKey(Organismo, blank=True, null=True)
    # AGREGAR LAS ACTIVIDADES DE TPCP
    entidad = models.ForeignKey(Entidad, blank=True, null=True)
    municipio_entidad = models.ForeignKey(Municipio, related_name='municipio_entidad', blank=True, null=True)
    causa_no_ubicado = models.ForeignKey(CausalNoUbicado, blank=True, null=True)
    incorporado = models.ForeignKey(EstadoIncorporado, blank=True, null=True)
    fecha_baja = models.DateTimeField(blank=True, null=True)
    causa_baja = models.ForeignKey(CausalBaja, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def sexo_verbose(self):
        return dict(EgresadosEstablecimientosPenitenciarios.ESTADOS_SEXO)[self.sexo]

    def ubicado_estado(self):
        if self.ubicado:
            return "Si"
        else:
            return "No"


class HistorialDesvinculado(models.Model):
    id_desvinculado = models.IntegerField()
    municipio_solicita_empleo = models.ForeignKey(Municipio, related_name='mun_solicita_empleo_h_desvinculado')
    ubicacion = models.ForeignKey(Ubicacion)
    fecha_ubicacion = models.DateTimeField(auto_now_add=True)
    organismo = models.ForeignKey(Organismo, blank=True, null=True)
    # AGREGAR LAS ACTIVIDADES DE TPCP
    entidad = models.ForeignKey(Entidad, blank=True, null=True)
    municipio_entidad = models.ForeignKey(Municipio, related_name='mun_entidad_h_desvinculado', blank=True, null=True)


class Desvinculado(models.Model):
    ESTADOS_SEXO = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]

    municipio_solicita_empleo = models.ForeignKey(Municipio, related_name='municipio_solicita_empleo_desvinculado')
    nombre_apellidos = models.CharField(max_length=255)
    ci = models.CharField(max_length=11, unique=True, validators=[validacion_ci_egresado_ep])
    edad = models.IntegerField()
    sexo = models.CharField(max_length=20)
    municipio_residencia = models.ForeignKey(Municipio, related_name='municipio_residencia_desvinculado')
    direccion_particular = models.CharField(max_length=255)
    nivel_escolar = models.ForeignKey(NivelEscolar)
    carrera = models.ForeignKey(Carrera, blank=True, null=True)
    ubicado = models.BooleanField()
    ubicacion = models.ForeignKey(Ubicacion, blank=True, null=True)
    fecha_ubicacion = models.DateTimeField(blank=True, null=True)
    organismo = models.ForeignKey(Organismo, blank=True, null=True)
    # AGREGAR LAS ACTIVIDADES DE TPCP
    entidad = models.ForeignKey(Entidad, blank=True, null=True)
    municipio_entidad = models.ForeignKey(Municipio, related_name='municipio_entidad_desvinculado', blank=True,
                                          null=True)
    causa_no_ubicado = models.ForeignKey(CausalNoUbicado, blank=True, null=True)
    incorporado = models.ForeignKey(EstadoIncorporado, blank=True, null=True)
    fecha_baja = models.DateTimeField(blank=True, null=True)
    causa_baja = models.ForeignKey(CausalBaja, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def sexo_verbose(self):
        return dict(Desvinculado.ESTADOS_SEXO)[self.sexo]

    def ubicado_estado(self):
        if self.ubicado:
            return "Si"
        else:
            return "No"


class HistorialTMedioOCalificadoEOficio(models.Model):
    id_tm_oc_eo = models.IntegerField()
    municipio_solicita_empleo = models.ForeignKey(Municipio, related_name='mun_solicita_empleo_h_tm_oc_eo')
    ubicacion = models.ForeignKey(Ubicacion)
    fecha_ubicacion = models.DateTimeField(auto_now_add=True)
    organismo = models.ForeignKey(Organismo, blank=True, null=True)
    # AGREGAR LAS ACTIVIDADES DE TPCP
    entidad = models.ForeignKey(Entidad, blank=True, null=True)
    municipio_entidad = models.ForeignKey(Municipio, related_name='mun_entidad_h_tm_oc_eo', blank=True, null=True)


def validacion_ci_tm_oc_eo(value):
    if not re.match(u'[0-9]{2}((0[1-9])|(1[0-2]))((0[1-9])|([1-2][0-9])|(3[0-1]))[0-9]{5}$', value):
        raise ValidationError(
            'CI incorrecto.')
    ci = int(value)
    fecha = ci / 100000
    anno = fecha / 10000
    mes = (fecha / 100) % 100
    dia = fecha % 100
    if str(mes) == '2':
        if anno % 4 == 0 and dia > 29:
            raise ValidationError('CI incorrecto.')
        if anno % 4 != 0 and dia > 28:
            raise ValidationError('CI incorrecto.')
    if obtener_edad(value) < 15:
        raise ValidationError('No se aceptan menores de 15 años.')
    if obtener_edad(value) > 21:
        raise ValidationError('No se aceptan mayores de 20 años.')


class TMedioOCalificadoEOficio(models.Model):
    ESTADOS_SEXO = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]

    fuente_procedencia = models.ForeignKey(FuenteProcedencia)
    municipio_solicita_empleo = models.ForeignKey(Municipio, related_name='municipio_solicita_empleo_tm_oc_eo')
    nombre_apellidos = models.CharField(max_length=255)
    ci = models.CharField(max_length=11, unique=True, validators=[validacion_ci_tm_oc_eo])
    edad = models.IntegerField()
    sexo = models.CharField(max_length=20)
    municipio_residencia = models.ForeignKey(Municipio, related_name='municipio_residencia_tm_oc_eo')
    direccion_particular = models.CharField(max_length=255)
    nivel_escolar = models.ForeignKey(NivelEscolar)
    carrera = models.ForeignKey(Carrera, blank=True, null=True)
    cumple_servicio_social = models.BooleanField()
    folio_boleta = models.CharField(max_length=255, blank=True, null=True)
    ubicado = models.BooleanField()
    ubicacion = models.ForeignKey(Ubicacion, blank=True, null=True)
    # TODO: arreglar fecha de ubicacion
    fecha_ubicacion = models.DateTimeField(auto_now_add=True)
    organismo = models.ForeignKey(Organismo, blank=True, null=True)
    # AGREGAR LAS ACTIVIDADES DE TPCP
    entidad = models.ForeignKey(Entidad, blank=True, null=True)
    municipio_entidad = models.ForeignKey(Municipio, related_name='municipio_entidad_tm_oc_eo', blank=True, null=True)
    causa_no_ubicado = models.ForeignKey(CausalNoUbicado, blank=True, null=True)
    incorporado = models.ForeignKey(EstadoIncorporado, blank=True, null=True)
    fecha_baja = models.DateTimeField(blank=True, null=True)
    causa_baja = models.ForeignKey(CausalBaja, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def sexo_verbose(self):
        return dict(TMedioOCalificadoEOficio.ESTADOS_SEXO)[self.sexo]

    def ubicado_estado(self):
        if self.ubicado:
            return "Si"
        else:
            return "No"


def validacion_ci_menores(value):
    if not re.match(u'[0-9]{2}((0[1-9])|(1[0-2]))((0[1-9])|([1-2][0-9])|(3[0-1]))[0-9]{5}$', value):
        raise ValidationError(
            'CI incorrecto.')
    ci = int(value)
    fecha = ci / 100000
    anno = fecha / 10000
    mes = (fecha / 100) % 100
    dia = fecha % 100
    if str(mes) == '2':
        if anno % 4 == 0 and dia > 29:
            raise ValidationError('CI incorrecto.')
        if anno % 4 != 0 and dia > 28:
            raise ValidationError('CI incorrecto.')
    if obtener_edad(value) < 15:
        raise ValidationError('No se aceptan menores de 15 años.')
    if obtener_edad(value) > 16:
        raise ValidationError('No se aceptan mayores de 16 años.')


class HistorialMenores(models.Model):
    id_menor = models.IntegerField()
    municipio_solicita_empleo = models.ForeignKey(Municipio, related_name='mun_solicita_empleo_h_menor')
    ubicacion = models.ForeignKey(Ubicacion)
    fecha_ubicacion = models.DateTimeField(auto_now_add=True)
    organismo = models.ForeignKey(Organismo, blank=True, null=True)
    # AGREGAR LAS ACTIVIDADES DE TPCP
    entidad = models.ForeignKey(Entidad, blank=True, null=True)
    municipio_entidad = models.ForeignKey(Municipio, related_name='mun_entidad_h_menor', blank=True, null=True)


class Menores(models.Model):
    ESTADOS_SEXO = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]

    fuente_procedencia = models.ForeignKey(FuenteProcedencia)
    municipio_solicita_empleo = models.ForeignKey(Municipio, related_name='municipio_solicita_empleo_menor')
    nombre_apellidos = models.CharField(max_length=255)
    ci = models.CharField(max_length=11, unique=True, validators=[validacion_ci_menores])
    edad = models.IntegerField()
    sexo = models.CharField(max_length=20)
    municipio_residencia = models.ForeignKey(Municipio, related_name='municipio_residencia_menor')
    direccion_particular = models.CharField(max_length=255)
    nivel_escolar = models.ForeignKey(NivelEscolar)
    carrera = models.ForeignKey(Carrera, blank=True, null=True)
    # CAMBIAR LA FECHA DE AUTORIZO A UN FORMATO DE FECHA
    fecha_autorizo_dmt = models.CharField(max_length=255)
    ubicado = models.BooleanField()
    ubicacion = models.ForeignKey(Ubicacion, blank=True, null=True)
    # TODO: arreglar fecha de ubicacion
    fecha_ubicacion = models.DateTimeField(auto_now_add=True)
    organismo = models.ForeignKey(Organismo, blank=True, null=True)
    # AGREGAR LAS ACTIVIDADES DE TPCP
    entidad = models.ForeignKey(Entidad, blank=True, null=True)
    municipio_entidad = models.ForeignKey(Municipio, related_name='municipio_entidad_menor', blank=True, null=True)
    causa_no_ubicado = models.ForeignKey(CausalNoUbicado, blank=True, null=True)
    incorporado = models.ForeignKey(EstadoIncorporado, blank=True, null=True)
    fecha_baja = models.DateTimeField(blank=True, null=True)
    causa_baja = models.ForeignKey(CausalBaja, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def sexo_verbose(self):
        return dict(Menores.ESTADOS_SEXO)[self.sexo]

    def ubicado_estado(self):
        if self.ubicado:
            return "Si"
        else:
            return "No"


def validacion_ci_egresados_escuelas_especiales(value):
    if not re.match(u'[0-9]{2}((0[1-9])|(1[0-2]))((0[1-9])|([1-2][0-9])|(3[0-1]))[0-9]{5}$', value):
        raise ValidationError(
            'CI incorrecto.')
    ci = int(value)
    fecha = ci / 100000
    anno = fecha / 10000
    mes = (fecha / 100) % 100
    dia = fecha % 100
    if str(mes) == '2':
        if anno % 4 == 0 and dia > 29:
            raise ValidationError('CI incorrecto.')
        if anno % 4 != 0 and dia > 28:
            raise ValidationError('CI incorrecto.')
    if obtener_edad(value) < 15:
        raise ValidationError('No se aceptan menores de 15 años.')


class HistorialEgresadosEscuelasEspeciales(models.Model):
    id_egresado_escuela_especial = models.IntegerField()
    municipio_solicita_empleo = models.ForeignKey(Municipio,
                                                  related_name='mun_solicita_empleo_h_egresado_escuela_especial')
    ubicacion = models.ForeignKey(Ubicacion)
    fecha_ubicacion = models.DateTimeField(auto_now_add=True)
    organismo = models.ForeignKey(Organismo, blank=True, null=True)
    # AGREGAR LAS ACTIVIDADES DE TPCP
    entidad = models.ForeignKey(Entidad, blank=True, null=True)
    municipio_entidad = models.ForeignKey(Municipio, related_name='mun_entidad_h_egresado_escuela_especial', blank=True,
                                          null=True)


class EgresadosEscuelasEspeciales(models.Model):
    ESTADOS_SEXO = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]

    municipio_solicita_empleo = models.ForeignKey(Municipio,
                                                  related_name='municipio_solicita_empleo_egresado_escuela_especial')
    nombre_apellidos = models.CharField(max_length=255)
    ci = models.CharField(max_length=11, unique=True, validators=[validacion_ci_egresados_escuelas_especiales])
    edad = models.IntegerField()
    sexo = models.CharField(max_length=20)
    municipio_residencia = models.ForeignKey(Municipio, related_name='municipio_residencia_egresado_escuela_especial')
    direccion_particular = models.CharField(max_length=255)
    nivel_escolar = models.ForeignKey(NivelEscolar)
    carrera = models.ForeignKey(Carrera, blank=True, null=True)
    ubicado = models.BooleanField()
    ubicacion = models.ForeignKey(Ubicacion, blank=True, null=True)
    # TODO: arreglar fecha de ubicacion
    fecha_ubicacion = models.DateTimeField(auto_now_add=True)
    organismo = models.ForeignKey(Organismo, blank=True, null=True)
    entidad = models.ForeignKey(Entidad, blank=True, null=True)
    municipio_entidad = models.ForeignKey(Municipio, related_name='municipio_entidad_egresado_escuela_especial',
                                          blank=True, null=True)
    causa_no_ubicado = models.ForeignKey(CausalNoUbicado, blank=True, null=True)
    incorporado = models.ForeignKey(EstadoIncorporado, blank=True, null=True)
    fecha_baja = models.DateTimeField(blank=True, null=True)
    causa_baja = models.ForeignKey(CausalBaja, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def sexo_verbose(self):
        return dict(EgresadosEscuelasEspeciales.ESTADOS_SEXO)[self.sexo]

    def ubicado_estado(self):
        if self.ubicado:
            return "Si"
        else:
            return "No"


class HistorialEgresadosEscuelasConducta(models.Model):
    id_egresado_escuela_conducta = models.IntegerField()
    municipio_solicita_empleo = models.ForeignKey(Municipio,
                                                  related_name='mun_solicita_empleo_h_egresado_escuela_conducta')
    ubicacion = models.ForeignKey(Ubicacion)
    fecha_ubicacion = models.DateTimeField(auto_now_add=True)
    organismo = models.ForeignKey(Organismo, blank=True, null=True)
    # AGREGAR LAS ACTIVIDADES DE TPCP
    entidad = models.ForeignKey(Entidad, blank=True, null=True)
    municipio_entidad = models.ForeignKey(Municipio, related_name='mun_entidad_h_egresado_escuela_conducta', blank=True,
                                          null=True)


class EgresadosEscuelasConducta(models.Model):
    ESTADOS_SEXO = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]

    municipio_solicita_empleo = models.ForeignKey(Municipio,
                                                  related_name='municipio_solicita_empleo_egresado_escuela_conducta')
    nombre_apellidos = models.CharField(max_length=255)
    ci = models.CharField(max_length=11, unique=True, validators=[validacion_ci_menores])
    edad = models.IntegerField()
    sexo = models.CharField(max_length=20)
    municipio_residencia = models.ForeignKey(Municipio, related_name='municipio_residencia_egresado_escuela_conducta')
    direccion_particular = models.CharField(max_length=255)
    nivel_escolar = models.ForeignKey(NivelEscolar)
    carrera = models.ForeignKey(Carrera, blank=True, null=True)
    # CAMBIAR LA FECHA DE AUTORIZO A UN FORMATO DE FECHA
    fecha_autorizo_dmt = models.CharField(max_length=255)
    ubicado = models.BooleanField()
    ubicacion = models.ForeignKey(Ubicacion, blank=True, null=True)
    # TODO: arreglar fecha de ubicacion
    fecha_ubicacion = models.DateTimeField(auto_now_add=True)
    organismo = models.ForeignKey(Organismo, blank=True, null=True)
    # AGREGAR LAS ACTIVIDADES DE TPCP
    entidad = models.ForeignKey(Entidad, blank=True, null=True)
    municipio_entidad = models.ForeignKey(Municipio, related_name='municipio_entidad_egresado_escuela_conducta',
                                          blank=True,
                                          null=True)
    causa_no_ubicado = models.ForeignKey(CausalNoUbicado, blank=True, null=True)
    incorporado = models.ForeignKey(EstadoIncorporado, blank=True, null=True)
    fecha_baja = models.DateTimeField(blank=True, null=True)
    causa_baja = models.ForeignKey(CausalBaja, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def sexo_verbose(self):
        return dict(EgresadosEscuelasConducta.ESTADOS_SEXO)[self.sexo]

    def ubicado_estado(self):
        if self.ubicado:
            return "Si"
        else:
            return "No"


def validacion_ci_egresados_efi(value):
    if not re.match(u'[0-9]{2}((0[1-9])|(1[0-2]))((0[1-9])|([1-2][0-9])|(3[0-1]))[0-9]{5}$', value):
        raise ValidationError(
            'CI incorrecto.')
    ci = int(value)
    fecha = ci / 100000
    anno = fecha / 10000
    mes = (fecha / 100) % 100
    dia = fecha % 100
    if str(mes) == '2':
        if anno % 4 == 0 and dia > 29:
            raise ValidationError('CI incorrecto.')
        if anno % 4 != 0 and dia > 28:
            raise ValidationError('CI incorrecto.')
    if obtener_edad(value) < 15:
        raise ValidationError('No se aceptan menores de 15 años.')
    if obtener_edad(value) > 16:
        raise ValidationError('No se aceptan mayores de 16 años.')


class HistorialEgresadosEFI(models.Model):
    id_egresado_efi = models.IntegerField()
    municipio_solicita_empleo = models.ForeignKey(Municipio, related_name='mun_solicita_empleo_h_egresado_efi')
    ubicacion = models.ForeignKey(Ubicacion)
    fecha_ubicacion = models.DateTimeField(auto_now_add=True)
    organismo = models.ForeignKey(Organismo, blank=True, null=True)
    # AGREGAR LAS ACTIVIDADES DE TPCP
    entidad = models.ForeignKey(Entidad, blank=True, null=True)
    municipio_entidad = models.ForeignKey(Municipio, related_name='mun_entidad_h_egresado_efi', blank=True, null=True)


class EgresadosEFI(models.Model):
    ESTADOS_SEXO = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]

    municipio_solicita_empleo = models.ForeignKey(Municipio,
                                                  related_name='municipio_solicita_empleo_egresado_efi')
    nombre_apellidos = models.CharField(max_length=255)
    ci = models.CharField(max_length=11, unique=True, validators=[validacion_ci_egresados_efi])
    edad = models.IntegerField()
    sexo = models.CharField(max_length=20)
    municipio_residencia = models.ForeignKey(Municipio,
                                             related_name='municipio_residencia_egresado_efi')
    direccion_particular = models.CharField(max_length=255)
    nivel_escolar = models.ForeignKey(NivelEscolar)
    carrera = models.ForeignKey(Carrera, blank=True, null=True)
    # CAMBIAR LA FECHA DE AUTORIZO A UN FORMATO DE FECHA
    fecha_autorizo_dmt = models.CharField(max_length=255)
    ubicado = models.BooleanField()
    ubicacion = models.ForeignKey(Ubicacion, blank=True, null=True)
    # TODO: arreglar fecha de ubicacion
    fecha_ubicacion = models.DateTimeField(auto_now_add=True)
    organismo = models.ForeignKey(Organismo, blank=True, null=True)
    # AGREGAR LAS ACTIVIDADES DE TPCP
    entidad = models.ForeignKey(Entidad, blank=True, null=True)
    municipio_entidad = models.ForeignKey(Municipio, related_name='municipio_entidad_egresado_efi', blank=True,
                                          null=True)
    causa_no_ubicado = models.ForeignKey(CausalNoUbicado, blank=True, null=True)
    incorporado = models.ForeignKey(EstadoIncorporado, blank=True, null=True)
    fecha_baja = models.DateTimeField(blank=True, null=True)
    causa_baja = models.ForeignKey(CausalBaja, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def sexo_verbose(self):
        return dict(EgresadosEFI.ESTADOS_SEXO)[self.sexo]

    def ubicado_estado(self):
        if self.ubicado:
            return "Si"
        else:
            return "No"


def validacion_ci_discapacitados(value):
    if not re.match(u'[0-9]{2}((0[1-9])|(1[0-2]))((0[1-9])|([1-2][0-9])|(3[0-1]))[0-9]{5}$', value):
        raise ValidationError(
            'CI incorrecto.')
    ci = int(value)
    fecha = ci / 100000
    anno = fecha / 10000
    mes = (fecha / 100) % 100
    dia = fecha % 100
    if str(mes) == '2':
        if anno % 4 == 0 and dia > 29:
            raise ValidationError('CI incorrecto.')
        if anno % 4 != 0 and dia > 28:
            raise ValidationError('CI incorrecto.')
    if obtener_edad(value) < 17:
        raise ValidationError('No se aceptan menores de 17 años.')


class Asociacion(models.Model):
    nombre = models.CharField(max_length=255)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.nombre


class Discapacidad(models.Model):
    nombre = models.CharField(max_length=255)
    asociacion = models.ForeignKey(Asociacion, blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.nombre


class HistorialDiscapacitados(models.Model):
    id_discapacitado = models.IntegerField()
    municipio_solicita_empleo = models.ForeignKey(Municipio, related_name='mun_solicita_empleo_h_discapacitado')
    ubicacion = models.ForeignKey(Ubicacion)
    fecha_ubicacion = models.DateTimeField(auto_now_add=True)
    organismo = models.ForeignKey(Organismo, blank=True, null=True)
    # AGREGAR LAS ACTIVIDADES DE TPCP
    entidad = models.ForeignKey(Entidad, blank=True, null=True)
    municipio_entidad = models.ForeignKey(Municipio, related_name='mun_entidad_h_discapacitado', blank=True, null=True)


class Discapacitados(models.Model):
    ESTADOS_SEXO = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]

    municipio_solicita_empleo = models.ForeignKey(Municipio,
                                                  related_name='municipio_solicita_empleo_discapacitado')
    nombre_apellidos = models.CharField(max_length=255)
    ci = models.CharField(max_length=11, unique=True, validators=[validacion_ci_discapacitados])
    edad = models.IntegerField()
    sexo = models.CharField(max_length=20)
    municipio_residencia = models.ForeignKey(Municipio,
                                             related_name='municipio_residencia_discapacitado')
    direccion_particular = models.CharField(max_length=255)
    nivel_escolar = models.ForeignKey(NivelEscolar)
    carrera = models.ForeignKey(Carrera, blank=True, null=True)
    # CAMBIAR LA FECHA DE AUTORIZO A UN FORMATO DE FECHA
    tipo_discapacidad = models.ForeignKey(Discapacidad)
    ubicado = models.BooleanField()
    ubicacion = models.ForeignKey(Ubicacion, blank=True, null=True)
    # TODO: arreglar fecha de ubicacion
    fecha_ubicacion = models.DateTimeField(auto_now_add=True)
    organismo = models.ForeignKey(Organismo, blank=True, null=True)
    entidad = models.ForeignKey(Entidad, blank=True, null=True)
    municipio_entidad = models.ForeignKey(Municipio,
                                          related_name='municipio_entidad_discapacitado',
                                          blank=True,
                                          null=True)
    causa_no_ubicado = models.ForeignKey(CausalNoUbicado, blank=True, null=True)
    incorporado = models.ForeignKey(EstadoIncorporado, blank=True, null=True)
    fecha_baja = models.DateTimeField(blank=True, null=True)
    causa_baja = models.ForeignKey(CausalBaja, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def sexo_verbose(self):
        return dict(Discapacitados.ESTADOS_SEXO)[self.sexo]

    def ubicado_estado(self):
        if self.ubicado:
            return "Si"
        else:
            return "No"


class HistorialPersonasRiesgo(models.Model):
    id_persona_riesgo = models.IntegerField()
    municipio_solicita_empleo = models.ForeignKey(Municipio, related_name='mun_solicita_empleo_h_persona_riesgo')
    ubicacion = models.ForeignKey(Ubicacion)
    fecha_ubicacion = models.DateTimeField(auto_now_add=True)
    organismo = models.ForeignKey(Organismo, blank=True, null=True)
    # AGREGAR LAS ACTIVIDADES DE TPCP
    entidad = models.ForeignKey(Entidad, blank=True, null=True)
    municipio_entidad = models.ForeignKey(Municipio, related_name='mun_entidad_h_persona_riesgo', blank=True, null=True)


class PersonasRiesgo(models.Model):
    ESTADOS_SEXO = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]

    fuente_procedencia = models.ForeignKey(FuenteProcedencia)
    municipio_solicita_empleo = models.ForeignKey(Municipio, related_name='municipio_solicita_empleo_persona_riesgo')
    nombre_apellidos = models.CharField(max_length=255)
    ci = models.CharField(max_length=11, unique=True, validators=[validacion_ci_egresado_ep])
    edad = models.IntegerField()
    sexo = models.CharField(max_length=20)
    municipio_residencia = models.ForeignKey(Municipio, related_name='municipio_residencia_persona_riesgo')
    direccion_particular = models.CharField(max_length=255)
    nivel_escolar = models.ForeignKey(NivelEscolar)
    carrera = models.ForeignKey(Carrera, blank=True, null=True)
    ubicado = models.BooleanField()
    ubicacion = models.ForeignKey(Ubicacion, blank=True, null=True)
    # TODO: arreglar fecha de ubicacion
    fecha_ubicacion = models.DateTimeField(auto_now_add=True)
    organismo = models.ForeignKey(Organismo, blank=True, null=True)
    # AGREGAR LAS ACTIVIDADES DE TPCP
    entidad = models.ForeignKey(Entidad, blank=True, null=True)
    municipio_entidad = models.ForeignKey(Municipio, related_name='municipio_entidad_persona_riesgo', blank=True,
                                          null=True)
    causa_no_ubicado = models.ForeignKey(CausalNoUbicado, blank=True, null=True)
    incorporado = models.ForeignKey(EstadoIncorporado, blank=True, null=True)
    fecha_baja = models.DateTimeField(blank=True, null=True)
    causa_baja = models.ForeignKey(CausalBaja, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def sexo_verbose(self):
        return dict(PersonasRiesgo.ESTADOS_SEXO)[self.sexo]

    def ubicado_estado(self):
        if self.ubicado:
            return "Si"
        else:
            return "No"


class ActividadInterrupto(models.Model):
    actividad = models.CharField(max_length=255)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __unicode__(self):
        return self.actividad


class CausalInterrupcion(models.Model):
    causa = models.CharField(max_length=255)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __unicode__(self):
        return self.causa


class CausalNoReubicacion(models.Model):
    causa = models.CharField(max_length=255)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __unicode__(self):
        return self.causa


class OrganismosAutorizadosRegistrarInterrupto(models.Model):
    organismo = models.ForeignKey(Organismo)
    tiempo_inicia = models.CharField(max_length=20)
    fecha_registro = models.DateTimeField(default=datetime.today())

    class Meta:
        ordering = ["id"]

    def __unicode__(self):
        return self.organismo


class Interruptos(models.Model):
    municipio = models.ForeignKey(Municipio)
    organismo = models.ForeignKey(Organismo)
    entidad = models.ForeignKey(Entidad)
    aplica_proceso = models.CharField(max_length=1, choices=[
        ('S', 'Si'),
        ('N', 'No')
    ])
    causa_interrupcion = models.ManyToManyField(CausalInterrupcion)

    causa_interrupcion_rotura = models.IntegerField(default=0)
    causa_interrupcion_falta_piezas = models.IntegerField(default=0)
    causa_interrupcion_accion_lluvia = models.IntegerField(default=0)
    causa_interrupcion_falta_energia = models.IntegerField(default=0)
    causa_interrupcion_orden_paralizacion_temporal = models.IntegerField(default=0)
    causa_interrupcion_paralizacion_reparacion = models.IntegerField(default=0)
    causa_interrupcion_otras_causas = models.IntegerField(default=0)

    total_trabajadores_entidad = models.IntegerField(default=0)
    total_interruptos_entidad = models.IntegerField(default=0)

    actividad_nueva = models.ManyToManyField(ActividadInterrupto, related_name='actividad_nueva', blank=True)
    actividad_directos = models.IntegerField(default=0)
    actividad_indirectos = models.IntegerField(default=0)
    actividad_todos = models.IntegerField(default=0, blank=True, null=True)

    # actividad = models.ForeignKey(ActividadInterrupto)
    causal_no_reubicacion = models.ManyToManyField(CausalNoReubicacion, blank=True)
    otras_causas_no_reubicacion = models.CharField(max_length=255, blank=True, null=True)
    #                        TOTALES
    # hasta 30 dias
    hastatreintadias_reubicadostemporal_misma_entidad = models.IntegerField(default=0)
    hastatreintadias_reubicadostemporal_mismo_organismo = models.IntegerField(default=0)
    hastatreintadias_reubicadostemporal_otro_organismo = models.IntegerField(default=0)
    hastatreintadias_cobrandogarantiasalarial = models.IntegerField(default=0)
    hastatreintadias_singarantiasalarial = models.IntegerField(default=0)
    hastatreintadias_baja = models.IntegerField(default=0)
    hastatreintadias_propuestoadisponibles = models.IntegerField(default=0)
    # entre 30 y 60 dias
    entretreintaysesentadias_reubicadostemporal_misma_entidad = models.IntegerField(default=0)
    entretreintaysesentadias_reubicadostemporal_mismo_organismo = models.IntegerField(default=0)
    entretreintaysesentadias_reubicadostemporal_otro_organismo = models.IntegerField(default=0)
    entretreintaysesentadias_cobrandogarantiasalarial = models.IntegerField(default=0)
    entretreintaysesentadias_singarantiasalarial = models.IntegerField(default=0)
    entretreintaysesentadias_baja = models.IntegerField(default=0)
    entretreintaysesentadias_propuestoadisponibles = models.IntegerField(default=0)
    # mas de 60 dias y hasta 1 año
    masdesesentayunanno_reubicadostemporal_misma_entidad = models.IntegerField(default=0)
    masdesesentayunanno_reubicadostemporal_mismo_organismo = models.IntegerField(default=0)
    masdesesentayunanno_reubicadostemporal_otro_organismo = models.IntegerField(default=0)
    masdesesentayunanno_cobrandogarantiasalarial = models.IntegerField(default=0)
    masdesesentayunanno_singarantiasalarial = models.IntegerField(default=0)
    masdesesentayunanno_baja = models.IntegerField(default=0)
    masdesesentayunanno_propuestoadisponibles = models.IntegerField(default=0)
    # mas de un año
    masdeunanno_reubicadostemporal_misma_entidad = models.IntegerField(default=0)
    masdeunanno_reubicadostemporal_mismo_organismo = models.IntegerField(default=0)
    masdeunanno_reubicadostemporal_otro_organismo = models.IntegerField(default=0)
    masdeunanno_cobrandogarantiasalarial = models.IntegerField(default=0)
    masdeunanno_singarantiasalarial = models.IntegerField(default=0)
    masdeunanno_baja = models.IntegerField(default=0)
    masdeunanno_propuestoadisponibles = models.IntegerField(default=0)
    #                      TOTALES FEMENINOS
    # hasta 30 dias
    f_hastatreintadias_reubicadostemporal = models.IntegerField(default=0)
    f_hastatreintadias_cobrandogarantiasalarial = models.IntegerField(default=0)
    f_hastatreintadias_singarantiasalarial = models.IntegerField(default=0)
    f_hastatreintadias_baja = models.IntegerField(default=0)
    f_hastatreintadias_propuestoadisponibles = models.IntegerField(default=0)
    # entre 30 y 60 dias
    f_entretreintaysesentadias_reubicadostemporal = models.IntegerField(default=0)
    f_entretreintaysesentadias_cobrandogarantiasalarial = models.IntegerField(default=0)
    f_entretreintaysesentadias_singarantiasalarial = models.IntegerField(default=0)
    f_entretreintaysesentadias_baja = models.IntegerField(default=0)
    f_entretreintaysesentadias_propuestoadisponibles = models.IntegerField(default=0)
    # mas de 60 dias y hasta 1 año
    f_masdesesentayunanno_reubicadostemporal = models.IntegerField(default=0)
    f_masdesesentayunanno_cobrandogarantiasalarial = models.IntegerField(default=0)
    f_masdesesentayunanno_singarantiasalarial = models.IntegerField(default=0)
    f_masdesesentayunanno_baja = models.IntegerField(default=0)
    f_masdesesentayunanno_propuestoadisponibles = models.IntegerField(default=0)
    # mas de un año
    f_masdeunanno_reubicadostemporal = models.IntegerField(default=0)
    f_masdeunanno_cobrandogarantiasalarial = models.IntegerField(default=0)
    f_masdeunanno_singarantiasalarial = models.IntegerField(default=0)
    f_masdeunanno_baja = models.IntegerField(default=0)
    f_masdeunanno_propuestoadisponibles = models.IntegerField(default=0)
    #                      TOTALES JOVENES
    # hasta 30 dias
    jovenes_hastatreintadias_reubicadostemporal = models.IntegerField(default=0)
    jovenes_hastatreintadias_cobrandogarantiasalarial = models.IntegerField(default=0)
    jovenes_hastatreintadias_singarantiasalarial = models.IntegerField(default=0)
    jovenes_hastatreintadias_baja = models.IntegerField(default=0)
    jovenes_hastatreintadias_propuestoadisponibles = models.IntegerField(default=0)
    # entre 30 y 60 dias
    jovenes_entretreintaysesentadias_reubicadostemporal = models.IntegerField(default=0)
    jovenes_entretreintaysesentadias_cobrandogarantiasalarial = models.IntegerField(default=0)
    jovenes_entretreintaysesentadias_singarantiasalarial = models.IntegerField(default=0)
    jovenes_entretreintaysesentadias_baja = models.IntegerField(default=0)
    jovenes_entretreintaysesentadias_propuestoadisponibles = models.IntegerField(default=0)
    # mas de 60 dias y hasta 1 año
    jovenes_masdesesentayunanno_reubicadostemporal = models.IntegerField(default=0)
    jovenes_masdesesentayunanno_cobrandogarantiasalarial = models.IntegerField(default=0)
    jovenes_masdesesentayunanno_singarantiasalarial = models.IntegerField(default=0)
    jovenes_masdesesentayunanno_baja = models.IntegerField(default=0)
    jovenes_masdesesentayunanno_propuestoadisponibles = models.IntegerField(default=0)
    # mas de un año
    jovenes_masdeunanno_reubicadostemporal = models.IntegerField(default=0)
    jovenes_masdeunanno_cobrandogarantiasalarial = models.IntegerField(default=0)
    jovenes_masdeunanno_singarantiasalarial = models.IntegerField(default=0)
    jovenes_masdeunanno_baja = models.IntegerField(default=0)
    jovenes_masdeunanno_propuestoadisponibles = models.IntegerField(default=0)

    informe_valorativo = models.FileField(upload_to='uploads/informe_valorativo_interruptos/', null=True, blank=True)

    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["id"]


class CausalNoRequiereEmpleo(models.Model):
    causa = models.CharField(max_length=255)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.causa


def validacion_ci_joven_abandona_ns(value):
    if not re.match(u'[0-9]{2}((0[1-9])|(1[0-2]))((0[1-9])|([1-2][0-9])|(3[0-1]))[0-9]{5}$', value):
        raise ValidationError(
            'CI incorrecto.')
    ci = int(value)
    fecha = ci / 100000
    anno = fecha / 10000
    mes = (fecha / 100) % 100
    dia = fecha % 100
    if str(mes) == '2':
        if anno % 4 == 0 and dia > 29:
            raise ValidationError('CI incorrecto.')
        if anno % 4 != 0 and dia > 28:
            raise ValidationError('CI incorrecto.')


class CausalDesvinculacionNS(models.Model):
    causa = models.CharField(max_length=255)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.causa


class JovenAbandonanNS(models.Model):

    GET_SEXO = [
        ('m', 'Masculino'),
        ('f', 'Femenino'),
    ]

    GET_ANNO_ABANDONA = [
        (1, "Primero"),
        (2, "Segundo"),
        (3, "Tercero"),
        (4, "Cuarto"),
        (5, "Quinto"),
        (6, "Sexto")
    ]

    nombre_apellidos = models.CharField(max_length=255)
    ci = models.CharField(max_length=11, unique=True, validators=[validacion_ci_joven_abandona_ns])
    sexo = models.CharField(max_length=1)
    municipio_residencia = models.ForeignKey(Municipio, related_name='municipio_residencia_joven_abandona_ns')
    direccion_particular = models.CharField(max_length=255)
    nivel_escolar = models.ForeignKey(NivelEscolar)
    centro_estudio = models.ForeignKey(Centro_estudio)
    carrera_abandona = models.ForeignKey(Carrera)
    anno_abandona = models.IntegerField()
    causa_baja_ns = models.ForeignKey(CausalBaja)
    anno_baja = models.IntegerField()
    mes_baja = models.IntegerField()
    dia_baja = models.IntegerField()
    activo = models.BooleanField(default=True)

    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_modificado = models.DateTimeField(auto_now=True)

    def get_sexo(self):
        return dict(JovenAbandonanNS.GET_SEXO)[self.sexo]

    def get_anno_abandona(self):
        return dict(JovenAbandonanNS.GET_ANNO_ABANDONA)[self.anno_abandona]

    def __unicode__(self):
        return self.nombre_apellidos


class ProcesoTrabajadorSocialJANS(models.Model):

    REINCORPORADO_EDUCACION = [
        (0, 'Curso diurno'),
        (1, 'Curso por encuentro'),
        (2, 'Curso a distancia'),
    ]

    SI_NO = [
        ('S', 'Sí'),
        ('N', 'No'),
    ]

    joven_abandona = models.ForeignKey(JovenAbandonanNS)
    causa_desvinculacion = models.ForeignKey(CausalDesvinculacionNS)
    reincorporado_educacion = models.IntegerField()
    requiere_empleo = models.CharField(max_length=1, choices=SI_NO)
    oficio_conoce = models.ForeignKey(Carrera, blank=True, null=True)
    causa_no_requiere_empleo = models.ForeignKey(CausalNoRequiereEmpleo, blank=True, null=True)
    observaciones_empleo = models.CharField(max_length=255, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def reincorporado_edu(self):
        return dict(ProcesoTrabajadorSocialJANS.REINCORPORADO_EDUCACION)[self.reincorporado_educacion]

    def get_requiere_empleo(self):
        return dict(ProcesoTrabajadorSocialJANS.SI_NO)[self.requiere_empleo]


class ProcesoDireccionMEmpleoJANS(models.Model):

    SI_NO = [
        ('S', 'Sí'),
        ('N', 'No'),
    ]

    joven_abandona = models.ForeignKey(JovenAbandonanNS)
    ubicado = models.CharField(max_length=1, choices=SI_NO)
    ubicacion = models.ForeignKey(Ubicacion, blank=True, null=True)
    organismo = models.ForeignKey(Organismo, blank=True, null=True)
    municipio_entidad = models.ForeignKey(Municipio, blank=True, null=True)
    entidad = models.ForeignKey(Entidad, blank=True, null=True)
    causa_no_ubicacion = models.ForeignKey(CausalNoUbicado, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def get_ubicado(self):
        return dict(ProcesoDireccionMEmpleoJANS.SI_NO)[self.ubicado]


class ControlJovenAbandonanNS(models.Model):

    incorporado = models.ForeignKey(EstadoIncorporado, blank=True, null=True)
    ubicacion = models.ForeignKey(Ubicacion, blank=True, null=True)
    organismo = models.ForeignKey(Organismo, blank=True, null=True)
    entidad = models.ForeignKey(Entidad, blank=True, null=True)
    municipio = models.ForeignKey(Municipio, blank=True, null=True)
    causa_no_incorporado = models.ForeignKey(CausalNoIncorporado, blank=True, null=True)
    joven_abandona = models.ForeignKey(JovenAbandonanNS)
    fecha_registro = models.DateTimeField(auto_now_add=True)


class InterruptosCovid(models.Model):
    municipio = models.ForeignKey(Municipio, blank=True, null=True)  # municipio de la entidad???
    organismo = models.ForeignKey(Organismo)
    entidad = models.ForeignKey(Entidad)
    total_trabajadores_entidad = models.IntegerField()
    hospitalizados_covid = models.IntegerField()
    certificado_medico_covid = models.IntegerField()
    permanecen_entidad = models.IntegerField()
    trabajo_distancia = models.IntegerField()
    teletrabajo = models.IntegerField()
    interruptos = models.IntegerField()
    causa_interrupcion = models.ForeignKey(CausalInterrupcion)
    irma_misma_entidad = models.IntegerField()
    irma_otra_entidad_mismo_organismo = models.IntegerField()
    irma_otro_organismo = models.IntegerField()
    ircl_misma_entidad = models.IntegerField()
    ircl_otra_entidad_mismo_organismo = models.IntegerField()
    ircl_otro_organismo = models.IntegerField()
    vinculados_produccion_alimentos = models.IntegerField()
    garantia_salarial_100 = models.IntegerField()
    garantia_salarial_60 = models.IntegerField()
    locales_cerrados = models.IntegerField()
    total_locales = models.IntegerField()

    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_modificado = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.entidad

                    # ---------------codigo de daniel (FIN)---------------
