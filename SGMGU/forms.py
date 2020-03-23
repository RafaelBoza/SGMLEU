# -*- coding: utf-8 -*-
from django.template.context_processors import request

from SGMGU.views.utiles import obtener_mes

__author__ = 'Rolando.Morales'

from django import forms
from .models import *
import time


class EnviarCorreoForm(forms.Form):
    para = forms.CharField(
        label="Para",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el remitente del correo'
            }))

    asunto = forms.CharField(
        label="Asunto",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el asunto del correo'
            }))

    texto = forms.CharField(
        label="Texto",
        required=True,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el texto del correo',
                'rows': 5
            }))


class RegistroUserForm(forms.Form):
    username = forms.CharField(
        label="Usuario",
        required=True,
        min_length=5,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba su nombre de usuario'

            }))

    first_name = forms.CharField(
        label="Nombre",
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba su nombre (opcional)'
            }))

    last_name = forms.CharField(
        label="Apellidos",
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba sus apellidos (opcional)'
            }))

    email = forms.EmailField(
        label="Correo",
        required=False,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba su correo electrónico'
            }))

    password = forms.CharField(
        label="Contraseña",
        required=True,
        min_length=5,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Escriba su contraseña'

                   }
        ))

    password2 = forms.CharField(
        label="Confirmar Contraseña",
        min_length=5,
        required=True,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Confirme su contraseña'
                   }))

    telefono = forms.CharField(
        label="Teléfono",
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Escriba el teléfono (opcional)'
                   }))

    organismo = forms.ModelChoiceField(
        queryset=Organismo.objects.all().order_by("nombre"),
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control'

                   }))

    categoria = forms.ModelChoiceField(
        queryset=Categoria_usuario.objects.all().order_by("nombre"),
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control'
                   }))

    provincia = forms.ModelChoiceField(
        queryset=Provincia.objects.all().order_by("nombre"),
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'style': 'visibility:hidden',
                   }))
    municipio = forms.ModelChoiceField(
        queryset=Municipio.objects.all().order_by("nombre"),
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'style': 'visibility:hidden',
                   }))
    universidad = forms.ModelChoiceField(
        queryset=Centro_estudio.objects.all().order_by("nombre"),
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'style': 'visibility:hidden',
                   }))

    foto = forms.ImageField(required=False)

    def clean_username(self):
        """Comprueba que no exista un username igual en la db"""
        username = self.cleaned_data['username']
        if User.objects.filter(username=username):
            raise forms.ValidationError('Nombre de usuario ya registrado.')
        return username

    def clean_password2(self):
        """Comprueba que password y password2 sean iguales."""
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return password2


# Modificar datos del usuario-----------------------------------------------------------------------------

class ModificarUserPerfilForm(forms.ModelForm):
    telefono = forms.CharField(
        label="Télefono",
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba su télefono (opcional)'
            }))
    municipio = forms.ModelChoiceField(
        queryset=Municipio.objects.all().order_by("nombre"),
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'style': 'visibility:hidden',
                   }))

    class Meta:
        model = Perfil_usuario
        fields = ["organismo", "telefono", "foto", "categoria", "provincia", "municipio", "universidad"]
        widgets = {
            "organismo": forms.Select(attrs={"class": "form-control"}),
            "categoria": forms.Select(attrs={"class": "form-control"}),
            "provincia": forms.Select(attrs={"class": "form-control"}),
            "universidad": forms.Select(attrs={"class": "form-control"})
        }


class ModificarUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]

    username = forms.CharField(
        label="Usuario",
        required=True,
        min_length=5,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba su nombre de usuario'

            }))

    first_name = forms.CharField(
        label="Nombre",
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba su nombre'
            }))

    last_name = forms.CharField(
        label="Apellidos",
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba sus apellidos'
            }))

    email = forms.EmailField(
        label="Correo",
        required=False,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba su correo electrónico'
            }))

    def clean_username(self):
        """Comprueba que no exista un username igual en la db"""
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exclude(username=username):
            raise forms.ValidationError('Nombre de usuario ya registrado.')
        return username


# Usuario Actual------------------------------------------------------------------------------------------------

class ModificarUserPerfilFormActual(forms.ModelForm):
    telefono = forms.CharField(
        label="Télefono",
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba su télefono (opcional)'
            }))

    class Meta:
        model = Perfil_usuario
        fields = ["telefono", "foto"]


class ModificarUserFormActual(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]

    first_name = forms.CharField(
        label="Nombre",
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba su nombre'
            }))

    last_name = forms.CharField(
        label="Apellidos",
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba sus apellidos'
            }))

    email = forms.EmailField(
        label="Correo",
        required=False,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba su correo electrónico'
            }))


# ----Mario David------------------------------------------------------------------------

class CarreraForm(forms.ModelForm):
    class Meta:
        model = Carrera
        fields = ["codigo_mes", "nombre", "tipo"]
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'codigo_mes': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Escriba el código de la carrera'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba el nombre de la carrera'})
        }


class EntidadForm(forms.ModelForm):
    class Meta:
        model = Entidad
        fields = ['e_nombre', 'id_organismo_s','municipio']

    e_nombre = forms.CharField(
        label="Nombre de la entidad",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba aquí el nombre de la entidad'
            }))
#
#     direccion = forms.CharField(
#         label="Dirección de la entidad",
#         required=True,
#         widget=forms.TextInput(
#             attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Escriba aquí el nombre de la entidad'
#             }))

    id_organismo_s = forms.ModelChoiceField(
        label="Organismo al que pertenece",
        queryset=Organismo.objects.filter(activo=True),
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }))

    municipio = forms.ModelChoiceField(
        label="Municipio al que pertenece",
        queryset=MunicipioEntidad.objects.all(),
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }))
#
#     id_tipo = forms.ModelChoiceField(
#         label="Tipo de entidad",
#         required=True,
#         queryset=Tipo_Entidad.objects.filter(estado=True),
#         widget=forms.Select(
#             attrs={
#                 'class': 'form-control'
#
#             }))


class TipoEntidadForm(forms.ModelForm):
    class Meta:
        model = Tipo_Entidad
        fields = ['identificador', 'nombre_tipo']

    identificador = forms.CharField(
        label="Identificador del tipo de entidad",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba aquí el tipo de entidad'
            }))

    nombre_tipo = forms.CharField(
        label="Nombre del tipo de entidad",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba aquí el nombre del tipo de entidad'
            }))


# class DemandaForm(forms.ModelForm):
#     anno = int(time.strftime("%Y"))
#     mes = str(int(time.strftime("%m")))
#     dia = str(int(time.strftime("%d")))
#     hora = str(int(time.strftime("%H")))
#     minuto = str(int(time.strftime("%M")))
#     segundo = str(int(time.strftime("%S")))
#     milisegundo = str(int(round(time.time() * 1000)))
#     # ----------------------------------------
#     anno_menosdos = str(anno - 2)
#     anno_menosuno = str(anno - 1)
#     anno_masuno = str(anno + 1)
#     anno_masdos = str(anno + 2)
#     anno_mastres = str(anno + 3)
#     anno_mascuatro = str(anno + 4)
#     anno_mascinco = str(anno + 5)
#     anno_masseis = str(anno + 6)
#     anno_massiete = str(anno + 7)
#     anno_masocho = str(anno + 8)
#     anno_masnueve = str(anno + 9)
#     anno_masdiez = str(anno + 10)
#
#     anno = str(anno)
#
#     codigo = str(anno + mes + dia + hora + minuto + segundo + milisegundo)
#
#     class Meta:
#         model = DemandaGraduados
#         fields = ['organismo', 'entidad', 'municipio_entidad', 'carrera', 'anno_realizacion', 'anno_mas_uno',
#                   'anno_mas_dos', 'anno_mas_tres', 'anno_mas_cuatro', 'anno_mas_cinco', 'anno_mas_seis',
#                   'anno_mas_siete', 'anno_mas_ocho', 'anno_mas_nueve', 'anno_mas_diez']

    # codigo_demanda = forms.CharField(
    #     label="Codigo de la Demanda",
    #     required=True,
    #     widget= forms.TextInput(attrs={'class':'form-control','placeholder': 'Escriba aquí el codigo de la demanda'}))

    # codigo_demanda = forms.ChoiceField(
    #     label="Codigo de la Demanda",
    #     required=True,
    #     choices=[
    #         ('' + codigo, '' + codigo)
    #     ],
    #     widget=forms.Select(
    #         attrs={
    #             'class': 'form-control'
    #         }))


    # organismo = forms.ModelChoiceField(
    #     label="Organismo",
    #     required=True,
    #     queryset=Organismo.objects.filter(activo=True),
    #     widget=forms.Select(
    #         attrs={
    #             'class': 'form-control'
    #         }))
    #
    # entidad = forms.ModelChoiceField(
    #     label="Entidad",
    #     required=True,
    #     queryset=Entidad.objects.filter(estado=True),
    #     widget=forms.Select(
    #         attrs={
    #             'class': 'form-control'
    #         }))
    #
    # municipio_entidad = forms.ModelChoiceField(
    #     label="Municipio de la Entidad",
    #     required=True,
    #     queryset=Municipio.objects.all(),
    #     widget=forms.Select(
    #         attrs={
    #             'class': 'form-control'
    #         }))
    #
    # carrera = forms.ModelChoiceField(
    #     label="Carrera",
    #     required=True,
    #     queryset=Carrera.objects.filter(activo=True),
    #     widget=forms.Select(
    #         attrs={
    #             'class': 'form-control'
    #         }))
    #
    # anno_realizacion = forms.ChoiceField(
    #     label="Año de Realización",
    #     required=True,
    #     choices=[
    #         #               (''+anno_menosdos, ''+anno_menosdos),
    #         #               (''+anno_menosuno, ''+anno_menosuno),
    #         ('' + anno, '' + anno)
    #         #               (''+anno_masuno, ''+anno_masuno),
    #         #               (''+anno_masdos, ''+anno_masdos),
    #     ],
    #     widget=forms.Select(
    #         attrs={
    #             'class': 'form-control'
    #         }))
    #
    # anno_mas_uno = forms.CharField(
    #     label="" + anno_masuno,
    #     required=True,
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'form-control',
    #             'placeholder': 'Escriba aquí el valor.'
    #         }))
    #
    # anno_mas_dos = forms.CharField(
    #     label="" + anno_masdos,
    #     required=True,
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'form-control',
    #             'placeholder': 'Escriba aquí el valor.'
    #         }))
    #
    # anno_mas_tres = forms.CharField(
    #     label="" + anno_mastres,
    #     required=True,
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'form-control',
    #             'placeholder': 'Escriba aquí el valor.'
    #         }))
    #
    # anno_mas_cuatro = forms.CharField(
    #     label="" + anno_mascuatro,
    #     required=True,
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'form-control',
    #             'placeholder': 'Escriba aquí el valor.'
    #         }))
    #
    # anno_mas_cinco = forms.CharField(
    #     label="" + anno_mascinco,
    #     required=True,
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'form-control',
    #             'placeholder': 'Escriba aquí el valor.'
    #         }))
    #
    # anno_mas_seis = forms.CharField(
    #     label="" + anno_masseis,
    #     required=True,
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'form-control',
    #             'placeholder': 'Escriba aquí el valor.'
    #         }))
    #
    # anno_mas_siete = forms.CharField(
    #     label="" + anno_massiete,
    #     required=True,
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'form-control',
    #             'placeholder': 'Escriba aquí el valor.'
    #         }))
    #
    # anno_mas_ocho = forms.CharField(
    #     label="" + anno_masocho,
    #     required=True,
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'form-control',
    #             'placeholder': 'Escriba aquí el valor.'
    #         }))
    #
    # anno_mas_nueve = forms.CharField(
    #     label="" + anno_masnueve,
    #     required=True,
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'form-control',
    #             'placeholder': 'Escriba aquí el valor.'
    #         }))
    #
    # anno_mas_diez = forms.CharField(
    #     label="" + anno_masdiez,
    #     required=True,
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'form-control',
    #             'placeholder': 'Escriba aquí el valor.'
    #         }))


# class ExistenciaFotm(forms.ModelForm):
#     anno = int(time.strftime("%Y"))
#     anno = str(anno)
#
#     class Meta:
#         model = Existencia
#         fields = ['id_organismo', 'id_codigo_entidad', 'id_cod_carrera', 'id_municipio_ocupado', 'id_tipo_plaza',
#                   'id_rango_edad','cant_graduados', 'ano_realizacion']

    # id_ocupados = forms.CharField(
    #     label="Codigo de la Existencia",
    #     required=True,
    #     widget=forms.TextInput(
    #         attrs={'class': 'form-control', 'placeholder': 'Escriba aquí el codigo de la existencia'}))

    # id_organismo = forms.ModelChoiceField(
    #     label="Organismo",
    #     required=True,
    #     queryset=Organismo.objects.all(),
    #     widget=forms.Select(
    #         attrs={
    #             'class': 'form-control'
    #         }))
    #
    # id_codigo_entidad = forms.ModelChoiceField(
    #     label="Entidad",
    #     required=True,
    #     queryset=Entidad.objects.filter(estado=True),
    #     widget=forms.Select(
    #         attrs={
    #             'class': 'form-control'
    #         }))
    # id_cod_carrera = forms.ModelChoiceField(
    #     label="Carrera",
    #     required=True,
    #     queryset=Carrera.objects.filter(activo=True),
    #     widget=forms.Select(
    #         attrs={
    #             'class': 'form-control'
    #         }))
    # id_municipio_ocupado = forms.ModelChoiceField(
    #     label="Municipio",
    #     required=True,
    #     queryset=Municipio.objects.all(),
    #     widget=forms.Select(
    #         attrs={
    #             'class': 'form-control'
    #         }))

    # id_tipo_plaza = forms.Select(
    #     label = "Tipo de Plaza",
    #     required = True,
    #     widget = forms.Select(attrs={'class': 'form-control'}))
    #
    # id_rango_edad = forms.Select(
    #     label = "Rango de Edad",
    #     required = True,
    #     widget = forms.Select(attrs={'class': 'form-control'}))

    # widgets = {
    #     'id_tipo_plaza': forms.Select(attrs={"class": "form-control"}),
    #     'id_rango_edad': forms.Select(attrs={"class": "form-control"})
    # }
    # labels = {'id_tipo_plaza': 'Tipo de Plaza', 'id_rango_edad': 'Rango de Edad'}
    #
    # cant_graduados = forms.CharField(
    #     label="Cantidad de Graduados",
    #     required=True,
    #     widget=forms.TextInput(
    #         attrs={'class': 'form-control', 'placeholder': 'Escriba aquí la cantidad de trabajadores'}))
    #
    # ano_realizacion = forms.ChoiceField(
    #     label="Año de Realización",
    #     required=True,
    #     choices=[
    #         ('' + anno, '' + anno)
    #     ],
    #     widget=forms.Select(
    #         attrs={
    #             'class': 'form-control'
    #         }))


# class FluctuacionForm(forms.ModelForm):
#     anno = int(time.strftime("%Y"))
#     anno = str(anno)
#
#     class Meta:
#         model = Fluctuacion
#         fields = ['id_organismo', 'id_entidad', 'id_munic_entidad', 'id_causal', 'id_carrera', 'cantidad',
#                   'anno_realizacion']

    # id_fluctuacion = forms.CharField(
    #     label="Identificador",
    #     required=True,
    #     widget=forms.TextInput(
    #         attrs={'class': 'form-control', 'placeholder': 'Escriba aquí el identificador de la fluctuacion'}))

    # id_organismo = forms.ModelChoiceField(
    #     label="Organismo",
    #     required=True,
    #     queryset=Organismo.objects.all(),
    #     widget=forms.Select(
    #         attrs={
    #             'class': 'form-control'
    #         }))
    #
    # id_entidad = forms.ModelChoiceField(
    #     label="Entidad",
    #     required=True,
    #     queryset=Entidad.objects.filter(estado=True),
    #     widget=forms.Select(
    #         attrs={
    #             'class': 'form-control'
    #         }))
    #
    # id_munic_entidad = forms.ModelChoiceField(
    #     label="Municipio",
    #     required=True,
    #     queryset=Municipio.objects.all(),
    #     widget=forms.Select(
    #         attrs={
    #             'class': 'form-control'
    #         }))
    #
    # id_causal = forms.ModelChoiceField(
    #     label="Causal de fluctuación",
    #     required=True,
    #     queryset=Causal_movimiento.objects.filter(tipo='f'),
    #     widget=forms.Select(
    #         attrs={
    #             'class': 'form-control'
    #         }))
    #
    # id_carrera = forms.ModelChoiceField(
    #     label="Carrera",
    #     required=True,
    #     queryset=Carrera.objects.filter(activo=True),
    #     widget=forms.Select(
    #         attrs={
    #             'class': 'form-control'
    #         }))
    #
    # cantidad = forms.CharField(
    #     label="Cantidad",
    #     required=True,
    #     widget=forms.TextInput(
    #         attrs={'class': 'form-control', 'placeholder': 'Escriba aquí la cantidad de trabajadores que fluctuaron'}))
    #
    # anno_realizacion = forms.ChoiceField(
    #     label="Año de Realización",
    #     required=True,
    #     choices=[
    #         ('' + anno, '' + anno)
    #     ],
    #     widget=forms.Select(
    #         attrs={
    #             'class': 'form-control'
    #         }))


# --------------------------------------------------------------------------------------------
class RegistrarCentroEstudioForm(forms.ModelForm):
    class Meta:
        model = Centro_estudio
        fields = ["codigo_mes", "nombre", "siglas", "provincia"]
        widgets = {
            'provincia': forms.Select(
                attrs={
                    'class': 'form-control'

                })
        }

    codigo_mes = forms.CharField(
        label="Código Mes",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el código del centro de estudios'
            }))

    nombre = forms.CharField(
        label="Nombre",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el nombre del centro de estudios'
            }))

    siglas = forms.CharField(
        label="Siglas",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el nombre de la carrera'
            }))


# ---------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------
class ModificarContrasennaUserForm(forms.Form):
    password = forms.CharField(
        label="Contraseña",
        required=True,
        min_length=5,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Escriba su nueva contraseña'

                   }
        ))

    password2 = forms.CharField(
        label="Confirmar Contraseña",
        min_length=5,
        required=True,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Confirme su nueva contraseña'
                   }))

    def clean_password2(self):
        """Comprueba que password y password2 sean iguales."""
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return password2


# ----------------------------------------------------------------------------------------------------
from django.core.validators import RegexValidator


class RegistroExpedienteForm(forms.Form):
    nombre_graduado = forms.CharField(
        label="Nombre del graduado",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el nombre y apellidos del graduado '
            }))

    centro_estudio = forms.ModelChoiceField(
        label="Centro de estudio",
        queryset=Centro_estudio.objects.all(),
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control',

            }))

    carrera_graduado = forms.ModelChoiceField(
        label="Carrera del graduado",
        queryset=Carrera.objects.filter(tipo='ns'),
        required=True,

        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'placeholder': 'Seleccione la carrera del graduado'
            }))

    anno_graduacion = forms.CharField(
        label="Año de graduado",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el año de graduación del graduado'
            }))

    causal_movimiento = forms.ModelChoiceField(
        queryset=Causal_movimiento.objects.filter(activo=True, tipo='ml'),
        label="Causa del movimiento",
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control'

            }))

    sintesis_causal_movimiento = forms.CharField(
        label="Síntesis de la causa del movimiento",
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba una síntesis de la causa del movimiento',
                'rows': 2
            }))

    codigo_boleta = forms.CharField(
        label="Código de la boleta",
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el código de la boleta'
            }))

    imagen_boleta = forms.ImageField(label="Imagen de la boleta", required=False)

    ci = forms.CharField(
        validators=[RegexValidator(
            regex='^[0-9]{2}(0[1-9]|1[0-2])(31|30|(0[1-9]|[1-2][0-9]))[0-9]{5}$',
            message='Carnet de identidad incorrecto',
        )],
        label="Carnet de identidad del graduado",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el carnet de identidad del graduado '
            }))

    detalle_direccion_residencia = forms.CharField(
        label="Dirección de residencia",
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba la dirección de residencia del graduado'
            }))

    municipio_residencia = forms.ModelChoiceField(
        label="Municipio de residencia",
        queryset=Municipio.objects.all(),
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }))

    organismo_liberacion = forms.ModelChoiceField(
        label="Organismo que libera",
        queryset=Organismo.objects.all(),
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control'

            }))

    entidad_liberacion = forms.CharField(
        label="Entidad que lo libera",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el nombre de la entidad que lo libera',
            }))

    municipio_entidad_liberacion = forms.ModelChoiceField(
        label="Mun. Entidad que libera",
        queryset=Municipio.objects.all(),
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }))

    facultado_liberacion = forms.CharField(
        label="Facultado de liberación",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba nombre y apellidos del facultado que lo libera',
            }))

    organismo_aceptacion = forms.ModelChoiceField(
        label="Organismo que acepta",
        queryset=Organismo.objects.all(),
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control'

            }))

    entidad_aceptacion = forms.CharField(
        label="Entidad que lo acepta",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el nombre de la entidad que lo acepta',
            }))

    municipio_entidad_aceptacion = forms.ModelChoiceField(
        label="Mun. Entidad que acepta",
        queryset=Municipio.objects.all(),
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }))

    facultado_aceptacion = forms.CharField(
        label="Facultado de aceptación",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba nombre y apellidos del facultado que lo acepta',
            }))

    comprimido = forms.FileField(
        label="Comprimido (Documentos)",
        required=False
    )


# Registrar Movimiento interno


class RegistroMovimientoInternoForm(forms.Form):
    nombre_graduado = forms.CharField(
        label="Nombre del graduado",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el nombre y apellidos del graduado '
            }))

    centro_estudio = forms.ModelChoiceField(
        label="Centro de estudio",
        queryset=Centro_estudio.objects.all(),
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control',

            }))

    carrera_graduado = forms.ModelChoiceField(
        label="Carrera del graduado",
        queryset=Carrera.objects.filter(tipo='ns'),
        required=True,

        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'placeholder': 'Seleccione la carrera del graduado'
            }))

    anno_graduacion = forms.CharField(
        label="Año de graduado",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el año de graduación del graduado'
            }))

    causal_movimiento = forms.ModelChoiceField(
        queryset=Causal_movimiento.objects.filter(activo=True, tipo='ml'),
        label="Causa del movimiento",
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control'

            }))

    sintesis_causal_movimiento = forms.CharField(
        label="Síntesis de la causa del movimiento",
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba una síntesis de la causa del movimiento',
                'rows': 2

            }))

    codigo_boleta = forms.CharField(
        label="Código de la boleta",
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el código de la boleta'
            }))

    imagen_boleta = forms.ImageField(label="Imagen de la boleta", required=False)

    ci = forms.CharField(
        label="Carnet de identidad del graduado",
        required=False,
        validators=[RegexValidator(regex='^[0-9]{2}(0[1-9]|1[0-2])(31|30|(0[1-9]|[1-2][0-9]))[0-9]{5}$',
                                   message='CI incorrecto', )],
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el carnet de identidad del graduado '
            }))

    detalle_direccion_residencia = forms.CharField(
        label="Dirección de residencia",
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba la dirección de residencia del graduado'
            }))

    municipio_residencia = forms.ModelChoiceField(
        label="Municipio de residencia",
        queryset=Municipio.objects.all(),
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }))

    entidad_liberacion = forms.CharField(
        label="Entidad que lo libera",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el nombre de la entidad que lo libera',
            }))

    municipio_entidad_liberacion = forms.ModelChoiceField(
        label="Mun. Entidad que libera",
        queryset=Municipio.objects.all(),
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }))

    entidad_aceptacion = forms.CharField(
        label="Entidad que lo acepta",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el nombre de la entidad que lo acepta',
            }))

    municipio_entidad_aceptacion = forms.ModelChoiceField(
        label="Mun. Entidad que acepta",
        queryset=Municipio.objects.all(),
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }))

    aprobado = forms.CharField(
        label="Aprobado por",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba nombre y apellidos del facultado que lo aprueba',
            }))


# ------------------------------------------------------------------------------

class RegistrarOrganismoForm(forms.ModelForm):
    class Meta:
        model = Organismo
        fields = ["nombre", "siglas", "hijode"]

    nombre = forms.CharField(
        label="Nombre",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el nombre del organismo'
            }))

    siglas = forms.CharField(
        label="Siglas",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba las siglas del organismo'
            }))

    hijode = forms.ModelChoiceField(
        label="Org. Superior",
        queryset=Organismo.objects.filter(activo=True).order_by("nombre"),
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control'}))




class RegistrarCausalForm(forms.ModelForm):
    class Meta:
        model = Causal_movimiento
        fields = ["nombre", "tipo"]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'})
        }


class ModificarDireccionTrabajo(forms.ModelForm):
    class Meta:
        model = Direccion_trabajo
        exclude = ["activo"]

    director = forms.CharField(
        label="Director",
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el nombre del director'
            }))

    sexo_director = forms.ChoiceField(
        label="Sexo director",
        required=False,
        choices=(("F", "Femenino"), ("M", "Masculino"),),
        widget=forms.Select(

            attrs={
                'class': 'form-control',
                'placeholder': 'Seleccione el sexo del director'
            }))

    correo_director = forms.CharField(
        label="Correo Director",
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el correo del director'
            }))

    especialista = forms.CharField(
        label="Especialista",
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el nombre del especialista'
            }))

    correo_especialista = forms.CharField(
        label="Correo Especialista",
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el correo del especialista'
            }))

    provincia = forms.ModelChoiceField(
        queryset=Provincia.objects.all().order_by("nombre"),
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control'}))


class Expedientes_segun_carrera_form(forms.Form):
    anno = forms.CharField(
        label="anno",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el año',
                'type': 'number'
            }))

    carrera = forms.ModelChoiceField(
        queryset=Carrera.objects.filter(activo=True, tipo='ns').order_by("nombre"),
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control'}))


class Expedientes_segun_causal_form(forms.Form):
    anno = forms.CharField(
        label="anno",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el año',
                'type': 'number'
            }))

    causal = forms.ModelChoiceField(
        queryset=Causal_movimiento.objects.filter(activo=True, tipo='ml').order_by("nombre"),
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control'}))


class UbicadoForm(forms.ModelForm):
    class Meta:
        model = UbicacionLaboral
        fields = ["nombre_apellidos", "boleta", "centro_estudio", "carrera", "ci", "cumple_servicio_social",
                  "organismo", "entidad", "municipio_residencia", "provincia_ubicacion", "sexo", "direccion_particular",
                  "estado_ubicacion"]
        widgets = {
            "nombre_apellidos": forms.TextInput(attrs={"class": "form-control"}),
            "boleta": forms.TextInput(attrs={"class": "form-control codigo_boleta_fade"}),
            "centro_estudio": forms.Select(attrs={"class": "form-control"}),
            "carrera": forms.Select(attrs={"class": "form-control"}),
            "ci": forms.TextInput(attrs={"class": "form-control"}),
            "cumple_servicio_social": forms.Select(attrs={"class": "form-control"}),
            "organismo": forms.Select(attrs={"class": "form-control"}),
            "entidad": forms.TextInput(attrs={"class": "form-control"}),
            "municipio_residencia": forms.Select(attrs={"class": "form-control"}),
            "provincia_ubicacion": forms.Select(attrs={"class": "form-control"}),
            "direccion_particular": forms.TextInput(attrs={"class": "form-control"}),
            "estado_ubicacion": forms.Select(
                attrs={"class": "form-control", 'onchange': 'Objeto.cambiar_estado_ubicacion()'}),
        }

    cumple_servicio_social = forms.ChoiceField(choices=((True, "Si"), (False, "No"),),
                                               widget=forms.Select(attrs={"class": "form-control"}))
    sexo = forms.ChoiceField(choices=(("F", "Femenino"), ("M", "Masculino"),),
                             widget=forms.Select(attrs={"class": "form-control"}))


class DisponibleForm(forms.ModelForm):
    class Meta:
        model = DisponibilidadGraduados
        fields = ["nombre_apellidos", "centro_estudio", "carrera", "ci", "municipio_residencia", "sexo",
                  "direccion_particular", 'cumple_servicio_social']
        widgets = {
            "nombre_apellidos": forms.TextInput(attrs={"class": "form-control"}),
            "centro_estudio": forms.Select(attrs={"class": "form-control"}),
            "carrera": forms.Select(attrs={"class": "form-control"}),
            "ci": forms.TextInput(attrs={"class": "form-control"}),
            "municipio_residencia": forms.Select(attrs={"class": "form-control"}),
            "direccion_particular": forms.TextInput(attrs={"class": "form-control"}),
        }

    sexo = forms.ChoiceField(choices=(("F", "Femenino"), ("M", "Masculino"),),
                             widget=forms.Select(attrs={"class": "form-control"}))
    cumple_servicio_social = forms.ChoiceField(choices=((True, "Si"), (False, "No"),),
                                               widget=forms.Select(attrs={"class": "form-control"}))


class ExportarUbicadosProvinciaForm(forms.Form):
    anno = forms.CharField(
        label="anno",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el año',
                'type': 'number'
            }))

    provincia = forms.ModelChoiceField(
        queryset=Provincia.objects.all(),
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control'}))


class ExportarUbicadosOrganismoForm(forms.Form):
    anno = forms.CharField(
        label="anno",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el año',
                'type': 'number'
            }))

    organismo = forms.ModelChoiceField(
        queryset=Organismo.objects.filter(activo=True),
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control'}))


class FormBuscarUbicadosCI(forms.Form):
    ci = forms.CharField(label="ci", required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Escriba el ci', 'type': 'number'}))


class FormBuscarUbicadosBoleta(forms.Form):
    boleta = forms.CharField(label="código boleta", required=True,
                             widget=forms.TextInput(
                                 attrs={'class': 'form-control', 'placeholder': 'Escriba el código de la boleta'}))


class FormBuscarUbicadosOrganismo(forms.Form):
    organismo = forms.ModelChoiceField(queryset=Organismo.objects.filter(activo=True), required=True,
                                       widget=forms.Select(attrs={'class': 'form-control'}))


class FormBuscarUbicadosCarrera(forms.Form):
    carrera = forms.ModelChoiceField(queryset=Carrera.objects.filter(activo=True).order_by("nombre"), required=True,
                                     widget=forms.Select(attrs={'class': 'form-control'}))


class FormBuscarUbicadosMunicipioResidencia(forms.Form):
    municipio_residencia = forms.ModelChoiceField(queryset=Municipio.objects.all(), required=True,
                                                  widget=forms.Select(attrs={'class': 'form-control'}))


class FormBuscarUbicadosProvinciaUbicacion(forms.Form):
    provincia_ubicacion = forms.ModelChoiceField(queryset=Provincia.objects.all(), required=True,
                                                 widget=forms.Select(attrs={'class': 'form-control'}))


class FormBuscarUbicadosProvinciaResidencia(forms.Form):
    provincia_residencia = forms.ModelChoiceField(queryset=Provincia.objects.all(), required=True,
                                                  widget=forms.Select(attrs={'class': 'form-control'}))


class FormBuscarUbicadosCentroEstudio(forms.Form):
    centro_estudio = forms.ModelChoiceField(queryset=Centro_estudio.objects.all(), required=True,
                                            widget=forms.Select(attrs={'class': 'form-control'}))


class FormFactory:
    @staticmethod
    def build(opcion):
        if opcion == "organismo":
            form = FormBuscarUbicadosOrganismo

        if opcion == "boleta":
            form = FormBuscarUbicadosBoleta

        elif opcion == "carrera":
            form = FormBuscarUbicadosCarrera

        elif opcion == "provincia_ubicacion":
            form = FormBuscarUbicadosProvinciaUbicacion

        elif opcion == "municipio_residencia":
            form = FormBuscarUbicadosMunicipioResidencia

        elif opcion == "provincia_residencia":
            form = FormBuscarUbicadosProvinciaResidencia

        elif opcion == "centro_estudio":
            form = FormBuscarUbicadosCentroEstudio

        return form


class ProcesoInhabilitacionForm(forms.ModelForm):
    numero_resolucion = forms.CharField(label="Número resolución", required=True, widget=forms.TextInput(
        attrs={'class': 'form-control'}))

    ubicado = forms.ChoiceField(choices=((True, "Sí"), (False, "No"),),
                                widget=forms.Select(attrs={"class": "form-control"}),
                                label='Se encuentra ubicado')

    causal = forms.ModelChoiceField(
        label="Causal",
        required=False,
        queryset=Causal_movimiento.objects.filter(activo=True, tipo='i'),
        widget=forms.Select(

            attrs={
                'class': 'form-control causal_inhabilitacion',
            }))

    proceso = forms.ChoiceField(
        label="Proceso",
        required=True,
        choices=[
            ('i', 'Inhabilitación'),
            ('s', 'Suspensión de la Inhabilitación'),
        ],
        widget=forms.Select(

            attrs={
                'class': 'form-control',
                'onchange': 'Objeto.cambiar_estado_inhabilitacion()'
            }))

    class Meta:
        model = GraduadoInhabilitacion
        fields = ["nombre_apellidos", "ci", "carrera", "nivel_educacional", "provincia", 'cumple_servicio_social',
                  'organismo']
        widgets = {
            "numero_resolucion": forms.TextInput(attrs={"class": "form-control"}),
            "nombre_apellidos": forms.TextInput(attrs={"class": "form-control"}),
            "ci": forms.TextInput(attrs={"class": "form-control"}),
            "nivel_educacional": forms.Select(attrs={"class": "form-control"}),
            "carrera": forms.Select(attrs={"class": "form-control"}),
            "provincia": forms.Select(attrs={"class": "form-control"}),
            "cumple_servicio_social": forms.Select(attrs={"class": "form-control"}),
            "organismo": forms.Select(attrs={"class": "form-control"})
        }


class IndicacionForm(forms.ModelForm):
    class Meta:
        model = Indicacion
        fields = ["titulo", "categoria", "texto", "fichero"]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "categoria": forms.Select(attrs={"class": "form-control"}),
            "texto": forms.Textarea(attrs={"class": "form-control"})
        }


class CategoriaIndicacionForm(forms.ModelForm):
    class Meta:
        model = CategoriaIndicacion
        fields = ["nombre"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
        }


# ---------------codigo de daniel (INICIO)------------


class LicenciadosSMAForm(forms.ModelForm):
    class Meta:
        model = LicenciadosSMA
        fields = [
            "nombre_apellidos", "ci", "municipio_residencia", "direccion_particular",
            "nivel_escolar", "carrera", "recibio_oferta", "acepto_oferta", "causa_no_aceptacion", "ubicacion",
            "organismo", "entidad", "municipio_entidad", "causa_no_ubicado", "incorporado",
        ]
        widgets = {
            "nombre_apellidos": forms.TextInput(attrs={"class": "form-control"}),
            "ci": forms.TextInput(attrs={"class": "form-control"}),
            "municipio_residencia": forms.Select(attrs={"class": "form-control"}),
            "direccion_particular": forms.Textarea(attrs={"class": "form-control", 'rows': 3}),
            "nivel_escolar": forms.Select(attrs={"class": "form-control"}),
            "carrera": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "causa_no_aceptacion": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled'}),
            "ubicacion": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "organismo": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "entidad": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "municipio_entidad": forms.Select(
                attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "causa_no_ubicado": forms.Select(
                attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "incorporado": forms.Select(
                attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
        }
        labels = {
            'municipio_residencia': 'Municipio de residencia',
            'nombre_apellidos': 'Nombre y apellidos',
            'ubicacion': 'Oferta seleccionada',
            'causa_no_aceptacion': 'Causa de no aceptación',
            'ci': 'Carnet de identidad',
            'direccion_particular': 'Dirección particular',
            'municipio_entidad': 'Municipio de la entidad',
            'causa_no_ubicado': 'Causa de no ubicación',
        }

    recibio_oferta = forms.ChoiceField(choices=((True, "Sí"), (False, "No"),),
                                       widget=forms.Select(attrs={"class": "form-control"}), label='Recibió oferta')

    acepto_oferta = forms.ChoiceField(choices=(("S", "Sí"), ("N", "No"),),
                                      widget=forms.Select(attrs={"class": "form-control", 'disabled': 'disabled'}),
                                      label='Aceptó oferta', required=False)

    def __init__(self, *args, **kwargs):
        super(LicenciadosSMAForm, self).__init__(*args, **kwargs)
        ids_nivel_escolar = [1, 2, 3, 4, 5, 6]
        self.fields['nivel_escolar'].queryset = NivelEscolar.objects.filter(activo=True, id__in=ids_nivel_escolar)
        ids_ubicacion = [1, 2, 3, 4]
        self.fields['ubicacion'].queryset = Ubicacion.objects.filter(activo=True, id__in=ids_ubicacion)


class HistorialLicenciadoSMAForm(forms.ModelForm):
    class Meta:
        model = HistorialLicenciadosSMA
        fields = ["municipio_solicita_empleo", "ubicacion", "organismo", "entidad", "municipio_entidad"]
        widgets = {
            "municipio_solicita_empleo": forms.Select(attrs={"class": "form-control"}),
            "ubicacion": forms.Select(attrs={"class": "form-control"}),
            "organismo": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "entidad": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "municipio_entidad": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
        }
        labels = {
            'municipio_solicita_empleo': 'Municipio donde solicita empleo',
            'ubicacion': 'Ubicación',
            'municipio_entidad': 'Municipio de la entidad'
        }


class DarBajaLicenciadosSMAForm(forms.ModelForm):
    class Meta:
        model = LicenciadosSMA
        fields = ["causa_baja"]
        causa_baja = forms.Select(attrs={"class": "form-control"})
        labels = {'causa_baja': 'Causa de baja'}

    def __init__(self, *args, **kwargs):
        super(DarBajaLicenciadosSMAForm, self).__init__(*args, **kwargs)
        ids_causa_baja = [1, 2, 3, 4, 5, 6, 7]
        self.fields['causa_baja'].queryset = CausalBaja.objects.filter(activo=True, id__in=ids_causa_baja)


class ControlLicenciadosSMAForm(forms.ModelForm):
    class Meta:
        model = ControlLicenciadosSMA
        fields = [
            "ubicacion", "organismo", "municipio", "entidad", "incorporado", "causa_no_ubicado",
        ]
        widgets = {
            "incorporado": forms.Select(attrs={"class": "form-control", 'required': 'required'}),
            "ubicacion": forms.Select(attrs={"class": "form-control", 'required': 'required'}),
            "organismo": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "entidad": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "municipio": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "causa_no_ubicado": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
        }
        labels = {
            'causa_no_ubicado': 'Causa de no incorporación',
            'ubicacion': 'Ubicación',
            'municipio': 'Municipio',
        }

    incorporado = forms.ChoiceField(choices=(('S', "Sí"), ('N', "No")),
                                    widget=forms.Select(attrs={"class": "form-control"}))

    def __init__(self, *args, **kwargs):
        super(ControlLicenciadosSMAForm, self).__init__(*args, **kwargs)
        ids_causa_no_ubicado = [1, 2, 3, 4, 5]
        self.fields['causa_no_ubicado'].queryset = CausalNoUbicado.objects.filter(activo=True, id__in=ids_causa_no_ubicado)


class CategoriaUsuarioForm(forms.ModelForm):
    class Meta:
        model = Categoria_usuario
        fields = ["nombre"]
        widgets = {
            'nombre': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Escriba el nombre de la categoría'}),
        }


class NivelEscolarForm(forms.ModelForm):
    class Meta:
        model = NivelEscolar
        fields = ["nombre"]
        widgets = {
            'nombre': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Escriba el nombre del nivel escolar'}),
        }


class CausalNoAceptacionForm(forms.ModelForm):
    class Meta:
        model = CausalNoAceptacion
        fields = ["causa"]
        widgets = {
            'causa': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Escriba la causa de no aceptación'}),
        }


class CausalNoIncorporacionForm(forms.ModelForm):
    class Meta:
        model = CausalNoIncorporado
        fields = ["causa"]
        widgets = {
            'causa': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Escriba la causa de no incorporación'}),
        }


class CausalBajaForm(forms.ModelForm):
    class Meta:
        model = CausalBaja
        fields = ["causa"]
        widgets = {
            'causa': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Escriba la causa de baja'}),
        }


class UbicacionForm(forms.ModelForm):
    class Meta:
        model = Ubicacion
        fields = ["ubicacion"]
        widgets = {
            'ubicacion': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Escriba el nombre de la ubicación'}),
        }


class FuenteProcedenciaForm(forms.ModelForm):
    class Meta:
        model = FuenteProcedencia
        fields = ["nombre"]
        widgets = {
            'nombre': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Escriba el nombre de la fuente de procedencia'}),
        }


class EgresadosEstablecimientosPenitenciariosForm(forms.ModelForm):
    class Meta:
        model = EgresadosEstablecimientosPenitenciarios
        fields = [
            "fuente_procedencia", "municipio_solicita_empleo", "nombre_apellidos", "ci", "municipio_residencia",
            "direccion_particular", "delito", "motivo_egreso", "nivel_escolar", "carrera", "ubicado", "ubicacion",
            "organismo", "entidad",
            "municipio_entidad", "causa_no_ubicado", "incorporado",
        ]
        widgets = {
            "fuente_procedencia": forms.Select(attrs={"class": "form-control"}),
            "municipio_solicita_empleo": forms.Select(attrs={"class": "form-control"}),
            "nombre_apellidos": forms.TextInput(attrs={"class": "form-control"}),
            "ci": forms.TextInput(attrs={"class": "form-control"}),
            "municipio_residencia": forms.Select(attrs={"class": "form-control"}),
            "direccion_particular": forms.Textarea(attrs={"class": "form-control", 'rows': 3}),
            "delito": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "motivo_egreso": forms.Select(
                attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "nivel_escolar": forms.Select(attrs={"class": "form-control"}),
            "carrera": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled'}),
            "ubicado": forms.Select(attrs={"class": "form-control"}),
            "ubicacion": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "organismo": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "entidad": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "municipio_entidad": forms.Select(
                attrs={"class": "form-control", 'disabled': 'disabled'}),
            "causa_no_ubicado": forms.Select(
                attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "incorporado": forms.Select(
                attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
        }
        labels = {
            'fuente_procedencia': 'Fuente de procedencia',
            'municipio_solicita_empleo': 'Municipio donde solicita empleo',
            'nombre_apellidos': 'Nombre y apellidos',
            'ci': 'Carnet de identidad',
            'municipio_residencia': 'Municipio de residencia',
            'direccion_particular': 'Direción particular',
            'motivo_egreso': 'Motivo de egreso',
            'nivel_escolar': 'Nivel escolar',
            'ubicacion': 'Ubicación',
            'municipio_entidad': 'Municipio de la entidad',
            'causa_no_ubicado': 'Causa de no ubicación',
        }

        ubicado = forms.ChoiceField(choices=((True, "Sí"), (False, "No"),),
                                    widget=forms.Select(attrs={"class": "form-control"}), label='Se encuentra ubicado')

    def __init__(self, *args, **kwargs):
        super(EgresadosEstablecimientosPenitenciariosForm, self).__init__(*args, **kwargs)
        ids = [2, 3]
        self.fields['fuente_procedencia'].queryset = FuenteProcedencia.objects.filter(activo=True, id__in=ids)


class HistorialEgresadosYSancionadosForm(forms.ModelForm):
    class Meta:
        model = HistorialEgresadosYSancionados
        fields = ["municipio_solicita_empleo", "ubicacion", "organismo", "entidad", "municipio_entidad"]
        widgets = {
            "municipio_solicita_empleo": forms.Select(attrs={"class": "form-control"}),
            "ubicacion": forms.Select(attrs={"class": "form-control"}),
            "organismo": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "entidad": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "municipio_entidad": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
        }
        labels = {
            'municipio_solicita_empleo': 'Municipio donde solicita empleo',
            'ubicacion': 'Ubicación',
            'municipio_entidad': 'Municipio de la entidad'
        }

    def __init__(self, *args, **kwargs):
        super(HistorialEgresadosYSancionadosForm, self).__init__(*args, **kwargs)
        ids_ubicacion = [1, 2, 3, 4]
        self.fields['ubicacion'].queryset = Ubicacion.objects.filter(activo=True, id__in=ids_ubicacion)


class DarBajaEgresadoEPForm(forms.ModelForm):
    class Meta:
        model = EgresadosEstablecimientosPenitenciarios
        fields = ["causa_baja"]
        causa_baja = forms.Select(attrs={"class": "form-control"})
        labels = {'causa_baja': 'Causa de baja'}


class CausalNoUbicacionForm(forms.ModelForm):
    class Meta:
        model = CausalNoUbicado
        fields = ["causa"]
        widgets = {
            'causa': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Escriba la causa de no ubicación'}),
        }


class EstadoIncorporadoForm(forms.ModelForm):
    class Meta:
        model = EstadoIncorporado
        fields = ["estado"]
        widgets = {
            'estado': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Escriba el estado de incorporado'}),
        }


class DelitoForm(forms.ModelForm):
    class Meta:
        model = Delito
        fields = ["nombre"]
        widgets = {
            'nombre': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Escriba el delito'}),
        }


class MotivoEgresoForm(forms.ModelForm):
    class Meta:
        model = MotivoEgreso
        fields = ["nombre"]
        widgets = {
            'nombre': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Escriba el motivo de egreso'}),
        }


class DiscapacidadForm(forms.ModelForm):
    class Meta:
        model = Discapacidad
        fields = ["nombre", "asociacion"]
        widgets = {
            'nombre': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Escriba la discapacidad'}),
            'asociacion': forms.Select(
                attrs={'class': 'form-control'}),
        }
        labels = {
            'asociacion': 'Asociación',
        }


class AsociacionForm(forms.ModelForm):
    class Meta:
        model = Asociacion
        fields = ["nombre"]
        widgets = {
            'nombre': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Escriba la asociación'}),
        }


class DesvinculadosForm(forms.ModelForm):
    class Meta:
        model = Desvinculado
        fields = ["municipio_solicita_empleo", "nombre_apellidos", "ci", "municipio_residencia",
                  "direccion_particular", "nivel_escolar", "carrera", "ubicado", "ubicacion",
                  "organismo", "entidad", "municipio_entidad", "causa_no_ubicado", "incorporado"]
        widgets = {
            "municipio_solicita_empleo": forms.Select(attrs={"class": "form-control"}),
            "nombre_apellidos": forms.TextInput(attrs={"class": "form-control"}),
            "ci": forms.TextInput(attrs={"class": "form-control"}),
            "municipio_residencia": forms.Select(attrs={"class": "form-control"}),
            "direccion_particular": forms.Textarea(attrs={"class": "form-control", 'rows': 3}),
            "nivel_escolar": forms.Select(attrs={"class": "form-control"}),
            "carrera": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled'}),
            "ubicado": forms.Select(attrs={"class": "form-control"}),
            "ubicacion": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "organismo": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "entidad": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "municipio_entidad": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled'}),
            "causa_no_ubicado": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "incorporado": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
        }
        labels = {
            'fuente_procedencia': 'Fuente de procedencia',
            'municipio_solicita_empleo': 'Municipio donde solicita empleo',
            'nombre_apellidos': 'Nombre y apellidos',
            'ci': 'Carnet de identidad',
            'municipio_residencia': 'Municipio de residencia',
            'direccion_particular': 'Direción particular',
            'nivel_escolar': 'Nivel escolar',
            'ubicacion': 'Ubicación',
            'municipio_entidad': 'Municipio de la entidad',
            'causa_no_ubicado': 'Causa de no ubicación',
        }

        ubicado = forms.ChoiceField(choices=((True, "Sí"), (False, "No"),),
                                    widget=forms.Select(attrs={"class": "form-control"}), label='Se encuentra ubicado')

    def __init__(self, *args, **kwargs):
        super(DesvinculadosForm, self).__init__(*args, **kwargs)
        ids = [1, 2, 3, 4, 5, 8]
        self.fields['causa_no_ubicado'].queryset = CausalNoUbicado.objects.filter(activo=True, id__in=ids)


class UbicarDesvinculadoForm(forms.ModelForm):
    class Meta:

        model = Desvinculado

        fields = [
            "ubicacion",
            "organismo",
            "municipio_entidad",
            "entidad",
        ]

        widgets = {
            "ubicacion": forms.Select(attrs={"class": "form-control", 'required': 'required'}),
            "organismo": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "municipio_entidad": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled'}),
            "entidad": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
        }

    def __init__(self, *args, **kwargs):
        super(UbicarDesvinculadoForm, self).__init__(*args, **kwargs)
        ids_ubicacion = [1, 2, 3, 4]
        self.fields['ubicacion'].queryset = Ubicacion.objects.filter(activo=True, id__in=ids_ubicacion)
        self.fields['organismo'].queryset = Organismo.objects.filter(activo=True)


class HistorialDesvinculadoForm(forms.ModelForm):
    class Meta:
        model = HistorialDesvinculado
        fields = ["municipio_solicita_empleo", "ubicacion", "organismo", "entidad", "municipio_entidad"]
        widgets = {
            "municipio_solicita_empleo": forms.Select(attrs={"class": "form-control"}),
            "ubicacion": forms.Select(attrs={"class": "form-control"}),
            "organismo": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "entidad": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "municipio_entidad": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
        }
        labels = {
            'municipio_solicita_empleo': 'Municipio donde solicita empleo',
            'ubicacion': 'Ubicación',
            'municipio_entidad': 'Municipio de la entidad'
        }

    def __init__(self, *args, **kwargs):
        super(HistorialDesvinculadoForm, self).__init__(*args, **kwargs)
        ids_ubicacion = [1, 2, 3, 4]
        self.fields['ubicacion'].queryset = Ubicacion.objects.filter(activo=True, id__in=ids_ubicacion)


class DarBajaDesvinculadoForm(forms.ModelForm):
    class Meta:
        model = Desvinculado
        fields = ["causa_baja"]
        causa_baja = forms.Select(attrs={"class": "form-control"})
        labels = {'causa_baja': 'Causa de baja'}

    def __init__(self, *args, **kwargs):
        super(DarBajaDesvinculadoForm, self).__init__(*args, **kwargs)
        ids = [1, 2, 3, 4, 5, 6, 7]
        self.fields['causa_baja'].queryset = CausalBaja.objects.filter(activo=True, id__in=ids)


class TMedioOCalificadoEOficioForm(forms.ModelForm):
    class Meta:
        model = TMedioOCalificadoEOficio
        fields = ["fuente_procedencia", "municipio_solicita_empleo", "nombre_apellidos", "ci", "municipio_residencia",
                  "direccion_particular", "nivel_escolar", "carrera", "cumple_servicio_social", "folio_boleta",
                  "ubicado", "ubicacion", "organismo", "entidad", "municipio_entidad", "causa_no_ubicado",
                  "incorporado"]
        widgets = {
            "fuente_procedencia": forms.Select(attrs={"class": "form-control"}),
            "municipio_solicita_empleo": forms.Select(attrs={"class": "form-control"}),
            "nombre_apellidos": forms.TextInput(attrs={"class": "form-control"}),
            "ci": forms.TextInput(attrs={"class": "form-control"}),
            "municipio_residencia": forms.Select(attrs={"class": "form-control"}),
            "direccion_particular": forms.Textarea(attrs={"class": "form-control", 'rows': 3}),
            "nivel_escolar": forms.Select(attrs={"class": "form-control"}),
            "carrera": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled'}),
            "cumple_servicio_social": forms.Select(attrs={"class": "form-control"}),
            "folio_boleta": forms.TextInput(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "ubicado": forms.Select(attrs={"class": "form-control"}),
            "ubicacion": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "organismo": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "entidad": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "municipio_entidad": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled'}),
            "causa_no_ubicado": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "incorporado": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
        }
        labels = {
            'fuente_procedencia': 'Fuente de procedencia',
            'municipio_solicita_empleo': 'Municipio donde solicita empleo',
            'nombre_apellidos': 'Nombre y apellidos',
            'ci': 'Carnet de identidad',
            'municipio_residencia': 'Municipio de residencia',
            'direccion_particular': 'Direción particular',
            'nivel_escolar': 'Nivel escolar',
            'folio_boleta': 'Folio de la boleta',
            'ubicacion': 'Ubicación',
            'municipio_entidad': 'Municipio de la entidad',
            'causa_no_ubicado': 'Causa de no ubicación',
        }

        cumple_servicio_social = forms.ChoiceField(choices=((True, "Sí"), (False, "No"),),
                                                   widget=forms.Select(attrs={"class": "form-control"}),
                                                   label='Cumple el servicio social')

        ubicado = forms.ChoiceField(choices=((True, "Sí"), (False, "No"),),
                                    widget=forms.Select(attrs={"class": "form-control"}),
                                    label='Se encuentra ubicado')

    def __init__(self, *args, **kwargs):
        super(TMedioOCalificadoEOficioForm, self).__init__(*args, **kwargs)
        ids_fuente_procedencia = [6, 7, 8]
        self.fields['fuente_procedencia'].queryset = FuenteProcedencia.objects.filter(activo=True, id__in=ids_fuente_procedencia)
        ids_niveles_escolares= [1, 2, 3, 6]
        self.fields['nivel_escolar'].queryset = NivelEscolar.objects.filter(activo=True,
                                                                                      id__in=ids_niveles_escolares)


class HistorialTMedioOCalificadoEOficioForm(forms.ModelForm):
    class Meta:
        model = HistorialTMedioOCalificadoEOficio
        fields = ["municipio_solicita_empleo", "ubicacion", "organismo", "entidad", "municipio_entidad"]
        widgets = {
            "municipio_solicita_empleo": forms.Select(attrs={"class": "form-control"}),
            "ubicacion": forms.Select(attrs={"class": "form-control"}),
            "organismo": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "entidad": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "municipio_entidad": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
        }
        labels = {
            'municipio_solicita_empleo': 'Municipio donde solicita empleo',
            'ubicacion': 'Ubicación',
            'municipio_entidad': 'Municipio de la entidad'
        }

    def __init__(self, *args, **kwargs):
        super(HistorialTMedioOCalificadoEOficioForm, self).__init__(*args, **kwargs)
        ids_ubicacion = [1, 2, 3, 4]
        self.fields['ubicacion'].queryset = Ubicacion.objects.filter(activo=True, id__in=ids_ubicacion)


class DarBajaTMedioOCalificadoEOficioForm(forms.ModelForm):
    class Meta:
        model = TMedioOCalificadoEOficio
        fields = ["causa_baja"]
        causa_baja = forms.Select(attrs={"class": "form-control"})
        labels = {'causa_baja': 'Causa de baja'}

    def __init__(self, *args, **kwargs):
        super(DarBajaTMedioOCalificadoEOficioForm, self).__init__(*args, **kwargs)
        ids_causa_baja = [1, 2, 3, 4, 5, 6, 7]
        self.fields['causa_baja'].queryset = CausalBaja.objects.filter(activo=True, id__in=ids_causa_baja)


class MenoresForm(forms.ModelForm):
    class Meta:
        model = Menores
        fields = ["fuente_procedencia", "municipio_solicita_empleo", "nombre_apellidos", "ci",
                  "municipio_residencia", "direccion_particular", "nivel_escolar", "carrera", "fecha_autorizo_dmt",
                  "ubicado", "ubicacion", "organismo", "entidad", "municipio_entidad", "causa_no_ubicado",
                  "incorporado"]
        widgets = {
            "fuente_procedencia": forms.Select(attrs={"class": "form-control"}),
            "municipio_solicita_empleo": forms.Select(attrs={"class": "form-control"}),
            "nombre_apellidos": forms.TextInput(attrs={"class": "form-control"}),
            "ci": forms.TextInput(attrs={"class": "form-control"}),
            "municipio_residencia": forms.Select(attrs={"class": "form-control"}),
            "direccion_particular": forms.Textarea(attrs={"class": "form-control", 'rows': 3}),
            "nivel_escolar": forms.Select(attrs={"class": "form-control"}),
            "carrera": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled'}),
            "fecha_autorizo_dmt": forms.TextInput(attrs={"class": "form-control", "placeholder": "d/m/a"}),
            "ubicado": forms.Select(attrs={"class": "form-control", 'required': 'required'}),
            "ubicacion": forms.Select(
                attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "organismo": forms.Select(
                attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "entidad": forms.Select(
                attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "municipio_entidad": forms.Select(
                attrs={"class": "form-control", 'disabled': 'disabled'}),
            "causa_no_ubicado": forms.Select(
                attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "incorporado": forms.Select(
                attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
        }
        labels = {
            'fuente_procedencia': 'Fuente de procedencia',
            'municipio_solicita_empleo': 'Municipio donde solicita empleo',
            'nombre_apellidos': 'Nombre y apellidos',
            'ci': 'Carnet de identidad',
            'municipio_residencia': 'Municipio de residencia',
            'fecha_autorizo_dmt': 'Fecha de autorizo por el Director Municipal de Trabajo',
            'direccion_particular': 'Direción particular',
            'nivel_escolar': 'Nivel escolar',
            'ubicacion': 'Ubicación',
            'municipio_entidad': 'Municipio de la entidad',
            'causa_no_ubicado': 'Causa de no ubicación',
        }

        ubicado = forms.ChoiceField(choices=((True, "Sí"), (False, "No"),),
                                    widget=forms.Select(attrs={"class": "form-control"}),
                                    label='Se encuentra ubicado')

    def __init__(self, *args, **kwargs):
        super(MenoresForm, self).__init__(*args, **kwargs)
        ids_fuente_procedencia = [12, 13, 14]
        self.fields['fuente_procedencia'].queryset = FuenteProcedencia.objects.filter(activo=True,
                                                                                      id__in=ids_fuente_procedencia)
        ids_causas_no_ubicado = [1, 2, 3, 4, 7, 8]
        self.fields['causa_no_ubicado'].queryset = CausalNoUbicado.objects.filter(activo=True,
                                                                                  id__in=ids_causas_no_ubicado)
        ids_niveles_escolares = [1, 2, 3]
        self.fields['nivel_escolar'].queryset = NivelEscolar.objects.filter(activo=True,
                                                                            id__in=ids_niveles_escolares)


class HistorialMenoresForm(forms.ModelForm):
    class Meta:
        model = HistorialMenores
        fields = ["municipio_solicita_empleo", "ubicacion", "organismo", "entidad", "municipio_entidad"]
        widgets = {
            "municipio_solicita_empleo": forms.Select(attrs={"class": "form-control"}),
            "ubicacion": forms.Select(attrs={"class": "form-control"}),
            "organismo": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "entidad": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "municipio_entidad": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
        }
        labels = {
            'municipio_solicita_empleo': 'Municipio donde solicita empleo',
            'ubicacion': 'Ubicación',
            'municipio_entidad': 'Municipio de la entidad'
        }

    def __init__(self, *args, **kwargs):
        super(HistorialMenoresForm, self).__init__(*args, **kwargs)
        ids_ubicacion = [1, 2, 3, 4]
        self.fields['ubicacion'].queryset = Ubicacion.objects.filter(activo=True, id__in=ids_ubicacion)


class DarBajaMenorForm(forms.ModelForm):
    class Meta:
        model = Menores
        fields = ["causa_baja"]
        causa_baja = forms.Select(attrs={"class": "form-control"})
        labels = {'causa_baja': 'Causa de baja'}

    def __init__(self, *args, **kwargs):
        super(DarBajaMenorForm, self).__init__(*args, **kwargs)
        ids_causa_baja = [1, 2, 3, 4, 5, 6, 7]
        self.fields['causa_baja'].queryset = CausalBaja.objects.filter(activo=True, id__in=ids_causa_baja)


class EgresadosEscuelasEspecialesForm(forms.ModelForm):
    class Meta:
        model = EgresadosEscuelasEspeciales
        fields = ["municipio_solicita_empleo", "nombre_apellidos", "ci",
                  "municipio_residencia", "direccion_particular", "nivel_escolar",
                  "ubicado", "ubicacion", "organismo", "entidad", "municipio_entidad", "causa_no_ubicado",
                  "incorporado"]
        widgets = {
            "municipio_solicita_empleo": forms.Select(attrs={"class": "form-control"}),
            "nombre_apellidos": forms.TextInput(attrs={"class": "form-control"}),
            "ci": forms.TextInput(attrs={"class": "form-control"}),
            "municipio_residencia": forms.Select(attrs={"class": "form-control"}),
            "direccion_particular": forms.Textarea(attrs={"class": "form-control", 'rows': 3}),
            "nivel_escolar": forms.Select(attrs={"class": "form-control"}),
            "ubicado": forms.Select(attrs={"class": "form-control"}),
            "ubicacion": forms.Select(
                attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "organismo": forms.Select(
                attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "entidad": forms.Select(
                attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "municipio_entidad": forms.Select(
                attrs={"class": "form-control", 'disabled': 'disabled'}),
            "causa_no_ubicado": forms.Select(
                attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "incorporado": forms.Select(
                attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
        }
        labels = {
            'municipio_solicita_empleo': 'Municipio donde solicita empleo',
            'nombre_apellidos': 'Nombre y apellidos',
            'ci': 'Carnet de identidad',
            'municipio_residencia': 'Municipio de residencia',
            'direccion_particular': 'Direción particular',
            'nivel_escolar': 'Nivel escolar',
            'ubicacion': 'Ubicación',
            'municipio_entidad': 'Municipio de la entidad',
            'causa_no_ubicado': 'Causa de no ubicación',
        }

        ubicado = forms.ChoiceField(choices=((True, "Sí"), (False, "No"),),
                                    widget=forms.Select(attrs={"class": "form-control"}))

    def __init__(self, *args, **kwargs):
        super(EgresadosEscuelasEspecialesForm, self).__init__(*args, **kwargs)
        self.fields['nivel_escolar'].queryset = NivelEscolar.objects.filter(activo=True, id=3)
        ids_causas_no_ubicacion = [1, 2, 3, 4, 7, 8]
        self.fields['causa_no_ubicado'].queryset = CausalNoUbicado.objects.filter(activo=True, id__in=ids_causas_no_ubicacion)


class HistorialEgresadosEscuelasEspecialesForm(forms.ModelForm):
    class Meta:
        model = HistorialEgresadosEscuelasEspeciales
        fields = ["municipio_solicita_empleo", "ubicacion", "organismo", "entidad", "municipio_entidad"]
        widgets = {
            "municipio_solicita_empleo": forms.Select(attrs={"class": "form-control"}),
            "ubicacion": forms.Select(attrs={"class": "form-control"}),
            "organismo": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "entidad": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "municipio_entidad": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
        }
        labels = {
            'municipio_solicita_empleo': 'Municipio donde solicita empleo',
            'ubicacion': 'Ubicación',
            'municipio_entidad': 'Municipio de la entidad'
        }

    def __init__(self, *args, **kwargs):
        super(HistorialEgresadosEscuelasEspecialesForm, self).__init__(*args, **kwargs)
        ids_ubicacion = [1, 2, 3, 4]
        self.fields['ubicacion'].queryset = Ubicacion.objects.filter(activo=True, id__in=ids_ubicacion)


class DarBajaEgresadosEscuelasEspecialesForm(forms.ModelForm):
    class Meta:
        model = EgresadosEscuelasEspeciales
        fields = ["causa_baja"]
        causa_baja = forms.Select(attrs={"class": "form-control"})
        labels = {'causa_baja': 'Causa de baja'}

    def __init__(self, *args, **kwargs):
        super(DarBajaEgresadosEscuelasEspecialesForm, self).__init__(*args, **kwargs)
        ids_causa_baja = [1, 2, 3, 4, 5, 6, 7]
        self.fields['causa_baja'].queryset = CausalBaja.objects.filter(activo=True, id__in=ids_causa_baja)


class EgresadosEscuelasConductaForm(forms.ModelForm):
    class Meta:
        model = EgresadosEscuelasConducta
        fields = ["municipio_solicita_empleo", "nombre_apellidos", "ci",
                  "municipio_residencia", "direccion_particular", "nivel_escolar", "carrera",
                  "fecha_autorizo_dmt", "ubicado", "ubicacion", "organismo", "entidad", "municipio_entidad",
                  "causa_no_ubicado", "incorporado"]
        widgets = {
            "municipio_solicita_empleo": forms.Select(attrs={"class": "form-control"}),
            "nombre_apellidos": forms.TextInput(attrs={"class": "form-control"}),
            "ci": forms.TextInput(attrs={"class": "form-control"}),
            "municipio_residencia": forms.Select(attrs={"class": "form-control"}),
            "direccion_particular": forms.Textarea(attrs={"class": "form-control", 'rows': 3}),
            "nivel_escolar": forms.Select(attrs={"class": "form-control"}),
            "carrera": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled'}),
            "fecha_autorizo_dmt": forms.TextInput(attrs={"class": "form-control", "placeholder": "d/m/a"}),
            "ubicado": forms.Select(attrs={"class": "form-control"}),
            "ubicacion": forms.Select(
                attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "organismo": forms.Select(
                attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "entidad": forms.Select(
                attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "municipio_entidad": forms.Select(
                attrs={"class": "form-control", 'disabled': 'disabled'}),
            "causa_no_ubicado": forms.Select(
                attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "incorporado": forms.Select(
                attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
        }
        labels = {
            'municipio_solicita_empleo': 'Municipio donde solicita empleo',
            'nombre_apellidos': 'Nombre y apellidos',
            'ci': 'Carnet de identidad',
            'municipio_residencia': 'Municipio de residencia',
            'fecha_autorizo_dmt': 'Fecha de autorizo por el Director Municipal de Trabajo',
            'direccion_particular': 'Direción particular',
            'nivel_escolar': 'Nivel escolar',
            'ubicacion': 'Ubicación',
            'municipio_entidad': 'Municipio de la entidad',
            'causa_no_ubicado': 'Causa de no ubicación',
        }

        ubicado = forms.ChoiceField(choices=((True, "Sí"), (False, "No"),),
                                    widget=forms.Select(attrs={"class": "form-control"}))

    def __init__(self, *args, **kwargs):
        super(EgresadosEscuelasConductaForm, self).__init__(*args, **kwargs)
        ids_nivel_escolar = [2, 3]
        self.fields['nivel_escolar'].queryset = NivelEscolar.objects.filter(activo=True,
                                                                            id__in=ids_nivel_escolar)
        ids_causas_no_ubicado = [1, 2, 3, 4, 8]
        self.fields['causa_no_ubicado'].queryset = CausalNoUbicado.objects.filter(activo=True,
                                                                            id__in=ids_causas_no_ubicado)


class HistorialEgresadosEscuelasConductaForm(forms.ModelForm):
    class Meta:
        model = HistorialEgresadosEscuelasConducta
        fields = ["municipio_solicita_empleo", "ubicacion", "organismo", "entidad", "municipio_entidad"]
        widgets = {
            "municipio_solicita_empleo": forms.Select(attrs={"class": "form-control"}),
            "ubicacion": forms.Select(attrs={"class": "form-control"}),
            "organismo": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "entidad": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "municipio_entidad": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
        }
        labels = {
            'municipio_solicita_empleo': 'Municipio donde solicita empleo',
            'ubicacion': 'Ubicación',
            'municipio_entidad': 'Municipio de la entidad'
        }

    def __init__(self, *args, **kwargs):
        super(HistorialEgresadosEscuelasConductaForm, self).__init__(*args, **kwargs)
        ids_ubicacion = [1, 2, 3, 4]
        self.fields['ubicacion'].queryset = Ubicacion.objects.filter(activo=True, id__in=ids_ubicacion)


class DarBajaEgresadosEscuelasConductaForm(forms.ModelForm):
    class Meta:
        model = EgresadosEscuelasConducta
        fields = ["causa_baja"]
        causa_baja = forms.Select(attrs={"class": "form-control"})
        labels = {'causa_baja': 'Causa de baja'}

    def __init__(self, *args, **kwargs):
        super(DarBajaEgresadosEscuelasConductaForm, self).__init__(*args, **kwargs)
        ids_causa_baja = [1, 2, 3, 4, 5, 6, 7]
        self.fields['causa_baja'].queryset = CausalBaja.objects.filter(activo=True, id__in=ids_causa_baja)


class EgresadosEFIForm(forms.ModelForm):
    class Meta:
        model = EgresadosEFI
        fields = ["municipio_solicita_empleo", "nombre_apellidos", "ci",
                  "municipio_residencia", "direccion_particular", "nivel_escolar", "carrera",
                  "fecha_autorizo_dmt", "ubicado", "ubicacion", "organismo", "entidad", "municipio_entidad",
                  "causa_no_ubicado", "incorporado"]
        widgets = {
            "municipio_solicita_empleo": forms.Select(attrs={"class": "form-control"}),
            "nombre_apellidos": forms.TextInput(attrs={"class": "form-control"}),
            "ci": forms.TextInput(attrs={"class": "form-control"}),
            "municipio_residencia": forms.Select(attrs={"class": "form-control"}),
            "direccion_particular": forms.Textarea(attrs={"class": "form-control", 'rows': 3}),
            "nivel_escolar": forms.Select(attrs={"class": "form-control"}),
            "carrera": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled'}),
            "fecha_autorizo_dmt": forms.TextInput(attrs={"class": "form-control", "placeholder": "d/m/a"}),
            "ubicado": forms.Select(attrs={"class": "form-control"}),
            "ubicacion": forms.Select(
                attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "organismo": forms.Select(
                attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "entidad": forms.Select(
                attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "municipio_entidad": forms.Select(
                attrs={"class": "form-control", 'disabled': 'disabled'}),
            "causa_no_ubicado": forms.Select(
                attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "incorporado": forms.Select(
                attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
        }
        labels = {
            'municipio_solicita_empleo': 'Municipio donde solicita empleo',
            'nombre_apellidos': 'Nombre y apellidos',
            'ci': 'Carnet de identidad',
            'municipio_residencia': 'Municipio de residencia',
            'fecha_autorizo_dmt': 'Fecha de autorizo por el Director Municipal de Trabajo',
            'direccion_particular': 'Direción particular',
            'nivel_escolar': 'Nivel escolar',
            'ubicacion': 'Ubicación',
            'municipio_entidad': 'Municipio de la entidad',
            'causa_no_ubicado': 'Causa de no ubicación',
        }

        ubicado = forms.ChoiceField(choices=((True, "Sí"), (False, "No"),),
                                    widget=forms.Select(attrs={"class": "form-control"}))

    def __init__(self, *args, **kwargs):
        super(EgresadosEFIForm, self).__init__(*args, **kwargs)
        ids_nivel_escolar = [2, 3]
        self.fields['nivel_escolar'].queryset = NivelEscolar.objects.filter(activo=True,
                                                                            id__in=ids_nivel_escolar)
        ids_causas_no_ubicado = [1, 2, 3, 4, 8]
        self.fields['causa_no_ubicado'].queryset = CausalNoUbicado.objects.filter(activo=True,
                                                                                  id__in=ids_causas_no_ubicado)


class HistorialEgresadosEFIForm(forms.ModelForm):
    class Meta:
        model = HistorialEgresadosEFI
        fields = ["municipio_solicita_empleo", "ubicacion", "organismo", "entidad", "municipio_entidad"]
        widgets = {
            "municipio_solicita_empleo": forms.Select(attrs={"class": "form-control"}),
            "ubicacion": forms.Select(attrs={"class": "form-control"}),
            "organismo": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "entidad": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "municipio_entidad": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
        }
        labels = {
            'municipio_solicita_empleo': 'Municipio donde solicita empleo',
            'ubicacion': 'Ubicación',
            'municipio_entidad': 'Municipio de la entidad'
        }

    def __init__(self, *args, **kwargs):
        super(HistorialEgresadosEFIForm, self).__init__(*args, **kwargs)
        ids_ubicacion = [1, 2, 3, 4]
        self.fields['ubicacion'].queryset = Ubicacion.objects.filter(activo=True, id__in=ids_ubicacion)


class DarBajaEgresadosEFIForm(forms.ModelForm):
    class Meta:
        model = EgresadosEFI
        fields = ["causa_baja"]
        causa_baja = forms.Select(attrs={"class": "form-control"})
        labels = {'causa_baja': 'Causa de baja'}

    def __init__(self, *args, **kwargs):
        super(DarBajaEgresadosEFIForm, self).__init__(*args, **kwargs)
        ids_causa_baja = [1, 2, 3, 4, 5, 6, 7]
        self.fields['causa_baja'].queryset = CausalBaja.objects.filter(activo=True, id__in=ids_causa_baja)


class DiscapacitadosForm(forms.ModelForm):
    class Meta:
        model = Discapacitados
        fields = ["municipio_solicita_empleo", "nombre_apellidos", "ci",
                  "municipio_residencia", "direccion_particular", "nivel_escolar", "carrera",
                  "tipo_discapacidad","ubicado", "ubicacion", "organismo", "entidad", "municipio_entidad",
                  "causa_no_ubicado", "incorporado"]
        widgets = {
            "municipio_solicita_empleo": forms.Select(attrs={"class": "form-control"}),
            "nombre_apellidos": forms.TextInput(attrs={"class": "form-control"}),
            "ci": forms.TextInput(attrs={"class": "form-control"}),
            "municipio_residencia": forms.Select(attrs={"class": "form-control"}),
            "direccion_particular": forms.Textarea(attrs={"class": "form-control", 'rows': 3}),
            "nivel_escolar": forms.Select(attrs={"class": "form-control"}),
            "carrera": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled'}),
            "tipo_discapacidad": forms.Select(attrs={"class": "form-control"}),
            "ubicado": forms.Select(attrs={"class": "form-control"}),
            "ubicacion": forms.Select(
                attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "organismo": forms.Select(
                attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "entidad": forms.Select(
                attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "municipio_entidad": forms.Select(
                attrs={"class": "form-control", 'disabled': 'disabled'}),
            "causa_no_ubicado": forms.Select(
                attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "incorporado": forms.Select(
                attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
        }
        labels = {
            'municipio_solicita_empleo': 'Municipio donde solicita empleo',
            'nombre_apellidos': 'Nombre y apellidos',
            'ci': 'Carnet de identidad',
            'municipio_residencia': 'Municipio de residencia',
            'direccion_particular': 'Direción particular',
            'nivel_escolar': 'Nivel escolar',
            'tipo_discapacidad': 'Tipo de discapacidad',
            'ubicacion': 'Ubicación',
            'municipio_entidad': 'Municipio de la entidad',
            'causa_no_ubicado': 'Causa de no ubicación',
        }

        ubicado = forms.ChoiceField(choices=((True, "Sí"), (False, "No"),),
                                    widget=forms.Select(attrs={"class": "form-control"}))

    def __init__(self, *args, **kwargs):
        super(DiscapacitadosForm, self).__init__(*args, **kwargs)
        ids_causa_no_ubicado = [1, 2, 3, 4, 5, 8, 9]
        self.fields['causa_no_ubicado'].queryset = CausalNoUbicado.objects.filter(activo=True,
                                                                                  id__in=ids_causa_no_ubicado)


class HistorialDiscapacitadoForm(forms.ModelForm):
    class Meta:
        model = HistorialDiscapacitados
        fields = ["municipio_solicita_empleo", "ubicacion", "organismo", "entidad", "municipio_entidad"]
        widgets = {
            "municipio_solicita_empleo": forms.Select(attrs={"class": "form-control"}),
            "ubicacion": forms.Select(attrs={"class": "form-control"}),
            "organismo": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "entidad": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "municipio_entidad": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
        }
        labels = {
            'municipio_solicita_empleo': 'Municipio donde solicita empleo',
            'ubicacion': 'Ubicación',
            'municipio_entidad': 'Municipio de la entidad'
        }

    def __init__(self, *args, **kwargs):
        super(HistorialDiscapacitadoForm, self).__init__(*args, **kwargs)
        ids_ubicacion = [1, 2, 3, 4]
        self.fields['ubicacion'].queryset = Ubicacion.objects.filter(activo=True, id__in=ids_ubicacion)


class DarBajaDiscapacitadosForm(forms.ModelForm):
    class Meta:
        model = Discapacitados
        fields = ["causa_baja"]
        causa_baja = forms.Select(attrs={"class": "form-control"})
        labels = {'causa_baja': 'Causa de baja'}

    def __init__(self, *args, **kwargs):
        super(DarBajaDiscapacitadosForm, self).__init__(*args, **kwargs)
        ids_causa_baja = [1, 2, 3, 4, 5, 6, 7, 8]
        self.fields['causa_baja'].queryset = CausalBaja.objects.filter(activo=True, id__in=ids_causa_baja)


class PersonasRiesgoForm(forms.ModelForm):
    class Meta:
        model = PersonasRiesgo
        fields = ["fuente_procedencia", "municipio_solicita_empleo", "nombre_apellidos", "ci",
                  "municipio_residencia", "direccion_particular", "nivel_escolar", "carrera",
                  "ubicado", "ubicacion", "organismo", "entidad", "municipio_entidad", "causa_no_ubicado",
                  "incorporado"]
        widgets = {
            "fuente_procedencia": forms.Select(attrs={"class": "form-control"}),
            "municipio_solicita_empleo": forms.Select(attrs={"class": "form-control"}),
            "nombre_apellidos": forms.TextInput(attrs={"class": "form-control"}),
            "ci": forms.TextInput(attrs={"class": "form-control"}),
            "municipio_residencia": forms.Select(attrs={"class": "form-control"}),
            "direccion_particular": forms.Textarea(attrs={"class": "form-control", 'rows': 3}),
            "nivel_escolar": forms.Select(attrs={"class": "form-control"}),
            "carrera": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "ubicado": forms.Select(attrs={"class": "form-control"}),
            "ubicacion": forms.Select(
                attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "organismo": forms.Select(
                attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "entidad": forms.Select(
                attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "municipio_entidad": forms.Select(
                attrs={"class": "form-control", 'disabled': 'disabled'}),
            "causa_no_ubicado": forms.Select(
                attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "incorporado": forms.Select(
                attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
        }
        labels = {
            'fuente_procedencia': 'Fuente de procedencia',
            'municipio_solicita_empleo': 'Municipio donde solicita empleo',
            'nombre_apellidos': 'Nombre y apellidos',
            'ci': 'Carnet de identidad',
            'municipio_residencia': 'Municipio de residencia',
            'direccion_particular': 'Direción particular',
            'nivel_escolar': 'Nivel escolar',
            'ubicacion': 'Ubicación',
            'municipio_entidad': 'Municipio de la entidad',
            'causa_no_ubicado': 'Causa de no ubicación',
        }

        ubicado = forms.ChoiceField(choices=((True, "Sí"), (False, "No"),),
                                    widget=forms.Select(attrs={"class": "form-control"}),
                                    label='Se encuentra ubicado')

    def __init__(self, *args, **kwargs):
        super(PersonasRiesgoForm, self).__init__(*args, **kwargs)
        ids_fuente_procedencia = [16, 17, 18, 19]
        self.fields['fuente_procedencia'].queryset = FuenteProcedencia.objects.filter(activo=True,
                                                                                      id__in=ids_fuente_procedencia)
        ids_causa_no_ubicado= [1, 2, 3, 4, 5, 6, 8, 11]
        self.fields['causa_no_ubicado'].queryset = CausalNoUbicado.objects.filter(activo=True,
                                                                                      id__in=ids_causa_no_ubicado)


class HistorialPersonaRiesgoForm(forms.ModelForm):
    class Meta:
        model = HistorialPersonasRiesgo
        fields = ["municipio_solicita_empleo", "ubicacion", "organismo", "entidad", "municipio_entidad"]
        widgets = {
            "municipio_solicita_empleo": forms.Select(attrs={"class": "form-control"}),
            "ubicacion": forms.Select(attrs={"class": "form-control"}),
            "organismo": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "entidad": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
            "municipio_entidad": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled', 'required': 'required'}),
        }
        labels = {
            'municipio_solicita_empleo': 'Municipio donde solicita empleo',
            'ubicacion': 'Ubicación',
            'municipio_entidad': 'Municipio de la entidad'
        }

    def __init__(self, *args, **kwargs):
        super(HistorialPersonaRiesgoForm, self).__init__(*args, **kwargs)
        ids_ubicacion = [1, 2, 3, 4]
        self.fields['ubicacion'].queryset = Ubicacion.objects.filter(activo=True, id__in=ids_ubicacion)


class DarBajaPersonasRiesgoForm(forms.ModelForm):
    class Meta:
        model = PersonasRiesgo
        fields = ["causa_baja"]
        causa_baja = forms.Select(attrs={"class": "form-control"})
        labels = {'causa_baja': 'Causa de baja'}

    def __init__(self, *args, **kwargs):
        super(DarBajaPersonasRiesgoForm, self).__init__(*args, **kwargs)
        ids_causa_baja = [1, 2, 3, 4, 5, 6, 7]
        self.fields['causa_baja'].queryset = CausalBaja.objects.filter(activo=True, id__in=ids_causa_baja)


class CausalInterrupcionForm(forms.ModelForm):
    class Meta:
        model = CausalInterrupcion
        fields = ["causa"]
        widgets = {
            'causa': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Escriba la causa de interrupción'}),
        }


class CausalNoReubicacionForm(forms.ModelForm):
    class Meta:
        model = CausalNoReubicacion
        fields = ["causa"]
        widgets = {
            'causa': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Escriba la causa de no reubicación'}),
        }


class ActividadInterruptoForm(forms.ModelForm):
    class Meta:
        model = ActividadInterrupto
        fields = ["actividad"]
        widgets = {
            'actividad': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Escriba la actividad'}),
        }


class OrganismosAutorizadosRegistrarInterruptoForm(forms.ModelForm):
    class Meta:
        model = OrganismosAutorizadosRegistrarInterrupto
        fields = ["organismo"]
        widgets = {
            'organismo': forms.Select(
                attrs={'class': 'form-control', 'required': True}),
        }


class InterruptosForm(forms.ModelForm):
    class Meta:
        model = Interruptos
        fields = [
            "municipio",
            "organismo",
            "entidad",
            "aplica_proceso",
            "causa_interrupcion",
            "causa_interrupcion_rotura",
            "causa_interrupcion_falta_piezas",
            "causa_interrupcion_accion_lluvia",
            "causa_interrupcion_falta_energia",
            "causa_interrupcion_orden_paralizacion_temporal",
            "causa_interrupcion_paralizacion_reparacion",
            "causa_interrupcion_otras_causas",
            "total_trabajadores_entidad",
            "total_interruptos_entidad",
            "actividad_nueva",
            "actividad_directos",
            "actividad_indirectos",
            "causal_no_reubicacion",
            "otras_causas_no_reubicacion",
            #                        TOTALES
            # Hasta 30 dias
            "hastatreintadias_reubicadostemporal_misma_entidad",
            "hastatreintadias_reubicadostemporal_mismo_organismo",
            "hastatreintadias_reubicadostemporal_otro_organismo",
            "hastatreintadias_cobrandogarantiasalarial",
            "hastatreintadias_singarantiasalarial",
            "hastatreintadias_baja",
            "hastatreintadias_propuestoadisponibles",
            # entre 30 y 60 dias
            "entretreintaysesentadias_reubicadostemporal_misma_entidad",
            "entretreintaysesentadias_reubicadostemporal_mismo_organismo",
            "entretreintaysesentadias_reubicadostemporal_otro_organismo",
            "entretreintaysesentadias_cobrandogarantiasalarial",
            "entretreintaysesentadias_singarantiasalarial",
            "entretreintaysesentadias_baja",
            "entretreintaysesentadias_propuestoadisponibles",
            # mas de 60 dias y hasta 1 año
            "masdesesentayunanno_reubicadostemporal_misma_entidad",
            "masdesesentayunanno_reubicadostemporal_mismo_organismo",
            "masdesesentayunanno_reubicadostemporal_otro_organismo",
            "masdesesentayunanno_cobrandogarantiasalarial",
            "masdesesentayunanno_singarantiasalarial",
            "masdesesentayunanno_baja",
            "masdesesentayunanno_propuestoadisponibles",
            # mas de un año
            "masdeunanno_reubicadostemporal_misma_entidad",
            "masdeunanno_reubicadostemporal_mismo_organismo",
            "masdeunanno_reubicadostemporal_otro_organismo",
            "masdeunanno_cobrandogarantiasalarial",
            "masdeunanno_singarantiasalarial",
            "masdeunanno_baja",
            "masdeunanno_propuestoadisponibles",
            #                      TOTALES FEMENINOS
            # hasta 30 dias
            "f_hastatreintadias_reubicadostemporal",
            "f_hastatreintadias_cobrandogarantiasalarial",
            "f_hastatreintadias_singarantiasalarial",
            "f_hastatreintadias_baja",
            "f_hastatreintadias_propuestoadisponibles",
            # entre 30 y 60 dias
            "f_entretreintaysesentadias_reubicadostemporal",
            "f_entretreintaysesentadias_cobrandogarantiasalarial",
            "f_entretreintaysesentadias_singarantiasalarial",
            "f_entretreintaysesentadias_baja",
            "f_entretreintaysesentadias_propuestoadisponibles",
            # mas de 60 dias y hasta 1 año
            "f_masdesesentayunanno_reubicadostemporal",
            "f_masdesesentayunanno_cobrandogarantiasalarial",
            "f_masdesesentayunanno_singarantiasalarial",
            "f_masdesesentayunanno_baja",
            "f_masdesesentayunanno_propuestoadisponibles",
            # mas de un año
            "f_masdeunanno_reubicadostemporal",
            "f_masdeunanno_cobrandogarantiasalarial",
            "f_masdeunanno_singarantiasalarial",
            "f_masdeunanno_baja",
            "f_masdeunanno_propuestoadisponibles",
            #                      TOTALES JOVENES
            # hasta 30 dias
            "jovenes_hastatreintadias_reubicadostemporal",
            "jovenes_hastatreintadias_cobrandogarantiasalarial",
            "jovenes_hastatreintadias_singarantiasalarial",
            "jovenes_hastatreintadias_baja",
            "jovenes_hastatreintadias_propuestoadisponibles",
            # entre 30 y 60 dias
            "jovenes_entretreintaysesentadias_reubicadostemporal",
            "jovenes_entretreintaysesentadias_cobrandogarantiasalarial",
            "jovenes_entretreintaysesentadias_singarantiasalarial",
            "jovenes_entretreintaysesentadias_baja",
            "jovenes_entretreintaysesentadias_propuestoadisponibles",
            # mas de 60 dias y hasta 1 año
            "jovenes_masdesesentayunanno_reubicadostemporal",
            "jovenes_masdesesentayunanno_cobrandogarantiasalarial",
            "jovenes_masdesesentayunanno_singarantiasalarial",
            "jovenes_masdesesentayunanno_baja",
            "jovenes_masdesesentayunanno_propuestoadisponibles",
            # mas de un año
            "jovenes_masdeunanno_reubicadostemporal",
            "jovenes_masdeunanno_cobrandogarantiasalarial",
            "jovenes_masdeunanno_singarantiasalarial",
            "jovenes_masdeunanno_baja",
            "jovenes_masdeunanno_propuestoadisponibles",
        ]
        widgets = {

            "municipio": forms.Select(attrs={"class": "form-control", 'required': 'required'}),
            "organismo": forms.Select(attrs={"class": "form-control"}),
            "entidad": forms.Select(attrs={"class": "form-control", 'required': 'required'}),
            "causa_interrupcion": forms.SelectMultiple(
                attrs={"class": "form-control", 'required': True, 'multiple': True}),
            # ---------------------------------------------------------------------------------------------------

            "causa_interrupcion_rotura": forms.TextInput(attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "causa_interrupcion_falta_piezas": forms.TextInput(attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "causa_interrupcion_accion_lluvia": forms.TextInput(attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "causa_interrupcion_falta_energia": forms.TextInput(attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "causa_interrupcion_orden_paralizacion_temporal": forms.TextInput(attrs={"class": "form-control", 'type': 'number'}),
            "causa_interrupcion_paralizacion_reparacion": forms.TextInput(attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "causa_interrupcion_otras_causas": forms.TextInput(attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "total_trabajadores_entidad": forms.TextInput(attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "total_interruptos_entidad": forms.TextInput(attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "actividad_nueva": forms.SelectMultiple(attrs={"class": "form-control", 'multiple': True}),
            "actividad_directos": forms.TextInput(attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "actividad_indirectos": forms.TextInput(attrs={"class": "form-control", 'type': 'number', 'min': 0}),

            # ---------------------------------------------------------------------------------------------------
            "causal_no_reubicacion": forms.SelectMultiple(
                attrs={"class": "form-control", 'multiple': True}),
            "otras_causas_no_reubicacion": forms.Textarea(attrs={"class": "form-control", 'rows': 3}),
            #                        TOTALES
            # Hasta 30 dias
            "hastatreintadias_reubicadostemporal_misma_entidad": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "hastatreintadias_reubicadostemporal_mismo_organismo": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "hastatreintadias_reubicadostemporal_otro_organismo": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "hastatreintadias_cobrandogarantiasalarial": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "hastatreintadias_singarantiasalarial": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "hastatreintadias_baja": forms.TextInput(attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "hastatreintadias_propuestoadisponibles": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number'}),
            # entre 30 y 60 dias
            "entretreintaysesentadias_reubicadostemporal_misma_entidad": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "entretreintaysesentadias_reubicadostemporal_mismo_organismo": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "entretreintaysesentadias_reubicadostemporal_otro_organismo": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "entretreintaysesentadias_cobrandogarantiasalarial": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "entretreintaysesentadias_singarantiasalarial": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "entretreintaysesentadias_baja": forms.TextInput(attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "entretreintaysesentadias_propuestoadisponibles": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            # mas de 60 dias y hasta 1 año
            "masdesesentayunanno_reubicadostemporal_misma_entidad": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "masdesesentayunanno_reubicadostemporal_mismo_organismo": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "masdesesentayunanno_reubicadostemporal_otro_organismo": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "masdesesentayunanno_cobrandogarantiasalarial": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "masdesesentayunanno_singarantiasalarial": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "masdesesentayunanno_baja": forms.TextInput(attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "masdesesentayunanno_propuestoadisponibles": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            # Mas de 1 año
            "masdeunanno_reubicadostemporal_misma_entidad": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "masdeunanno_reubicadostemporal_mismo_organismo": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "masdeunanno_reubicadostemporal_otro_organismo": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "masdeunanno_cobrandogarantiasalarial": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "masdeunanno_singarantiasalarial": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "masdeunanno_baja": forms.TextInput(attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "masdeunanno_propuestoadisponibles": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            #                      TOTALES FEMENINOS
            # hasta 30 dias
            "f_hastatreintadias_reubicadostemporal": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "f_hastatreintadias_cobrandogarantiasalarial": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "f_hastatreintadias_singarantiasalarial": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "f_hastatreintadias_baja": forms.TextInput(attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "f_hastatreintadias_propuestoadisponibles": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            # entre 30 y 60 dias
            "f_entretreintaysesentadias_reubicadostemporal": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "f_entretreintaysesentadias_cobrandogarantiasalarial": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "f_entretreintaysesentadias_singarantiasalarial": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "f_entretreintaysesentadias_baja": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "f_entretreintaysesentadias_propuestoadisponibles": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            # mas de 60 dias y hasta 1 año
            "f_masdesesentayunanno_reubicadostemporal": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "f_masdesesentayunanno_cobrandogarantiasalarial": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "f_masdesesentayunanno_singarantiasalarial": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "f_masdesesentayunanno_baja": forms.TextInput(attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "f_masdesesentayunanno_propuestoadisponibles": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            # mas de un año
            "f_masdeunanno_reubicadostemporal": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "f_masdeunanno_cobrandogarantiasalarial": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "f_masdeunanno_singarantiasalarial": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "f_masdeunanno_baja": forms.TextInput(attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "f_masdeunanno_propuestoadisponibles": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            #                      TOTALES JOVENES
            # hasta 30 dias
            "jovenes_hastatreintadias_reubicadostemporal": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "jovenes_hastatreintadias_cobrandogarantiasalarial": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "jovenes_hastatreintadias_singarantiasalarial": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "jovenes_hastatreintadias_baja": forms.TextInput(attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "jovenes_hastatreintadias_propuestoadisponibles": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            # entre 30 y 60 dias
            "jovenes_entretreintaysesentadias_reubicadostemporal": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "jovenes_entretreintaysesentadias_cobrandogarantiasalarial": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "jovenes_entretreintaysesentadias_singarantiasalarial": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "jovenes_entretreintaysesentadias_baja": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "jovenes_entretreintaysesentadias_propuestoadisponibles": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            # mas de 60 dias y hasta 1 año
            "jovenes_masdesesentayunanno_reubicadostemporal": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "jovenes_masdesesentayunanno_cobrandogarantiasalarial": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "jovenes_masdesesentayunanno_singarantiasalarial": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "jovenes_masdesesentayunanno_baja": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "jovenes_masdesesentayunanno_propuestoadisponibles": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            # mas de un año
            "jovenes_masdeunanno_reubicadostemporal": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "jovenes_masdeunanno_cobrandogarantiasalarial": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "jovenes_masdeunanno_singarantiasalarial": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "jovenes_masdeunanno_baja": forms.TextInput(attrs={"class": "form-control", 'type': 'number', 'min': 0}),
            "jovenes_masdeunanno_propuestoadisponibles": forms.TextInput(
                attrs={"class": "form-control", 'type': 'number', 'min': 0}),

            # "causa_no_aceptacion": forms.Select(attrs={"class": "form-control", 'disabled': 'disabled'}),
        }
        labels = {
            'causa_interrupcion': 'Causa de interrupción',
            'causal_no_reubicacion': 'Causa(s) de no reubicación',
            'otras_causas_no_reubicacion': 'Otra(s) causa(s) de no reubicación',
            'total_trabajadores_entidad': 'Total de trabajadores (entidad)',
            'total_interruptos_entidad': 'Total de interruptos (entidad)',
            'actividad_nueva': 'Actividades de interrupción',
        }

    informe_valorativo = forms.FileField(label="Informe valorativo", required=False)

    aplica_proceso = forms.ChoiceField(choices=(("S", "Sí"), ("N", "No"),), widget=forms.Select(
        attrs={"class": "form-control"}), label='Aplica proceso', required=True)

    def __init__(self, *args, **kwargs):
        super(InterruptosForm, self).__init__(*args, **kwargs)
        self.fields['causa_interrupcion'].queryset = CausalInterrupcion.objects.filter(activo=True)
        self.fields['actividad_nueva'].queryset = ActividadInterrupto.objects.filter(activo=True)
        # self.fields['actividad'].queryset = ActividadInterrupto.objects.filter(activo=True)
        self.fields['causal_no_reubicacion'].queryset = CausalNoReubicacion.objects.filter(activo=True)


class JovenAbandonanNSForm(forms.ModelForm):
    class Meta:
        model = JovenAbandonanNS
        fields = [
            "nombre_apellidos",
            "ci",
            "sexo",
            "municipio_residencia",
            "direccion_particular",
            "nivel_escolar",
            "carrera_abandona",
            "centro_estudio",
            "anno_abandona",
            "causa_baja_ns",
            "anno_baja",
            "mes_baja",
            "dia_baja",
        ]
        widgets = {
            "nombre_apellidos": forms.TextInput(attrs={"class": "form-control"}),
            "ci": forms.TextInput(attrs={"class": "form-control"}),
            'municipio_residencia': forms.Select(attrs={'class': 'form-control'}),
            "direccion_particular": forms.Textarea(attrs={"class": "form-control", 'rows': 3}),
            'nivel_escolar': forms.Select(attrs={'class': 'form-control'}),
            'carrera_abandona': forms.Select(attrs={'class': 'form-control'}),
            'centro_estudio': forms.Select(attrs={'class': 'form-control'}),
            'causa_baja_ns': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            "carrera_abandona": "Carrera que abandona",
            "centro_estudio": "Centro de estudio",
            "causa_baja_ns": "Causa de baja del nivel superior"
        }

    sexo = forms.ChoiceField(choices=(
                                ("", "---------"),
                                ("m", "Masculino"),
                                ("f", "Femenino")),
                             widget=forms.Select(
                             attrs={"class": "form-control"}), label='Sexo', required=True)

    anno_abandona = forms.ChoiceField(choices=(
                                            ("", "---------"),
                                            (1, "Primero"),
                                            (2, "Segundo"),
                                            (3, "Tercero"),
                                            (4, "Cuarto"),
                                            (5, "Quinto"),
                                            (6, "Sexto")),
                                      widget=forms.Select(attrs={"class": "form-control"}),
                                      label='Año en que abandona')

    ANNOS_BAJA = (("", "---------"),)
    for anno in range(2000, datetime.today().year + 1):
        ANNOS_BAJA = ANNOS_BAJA + ((anno, anno),)

    anno_baja = forms.ChoiceField(choices=ANNOS_BAJA,
                                  widget=forms.Select(attrs={"class": "form-control"}),
                                  label='Año de baja')

    MESES_BAJA = (("", "---------"),)
    for mes in range(1, 13):
        MESES_BAJA = MESES_BAJA + ((mes, obtener_mes(mes)),)

    mes_baja = forms.ChoiceField(choices=MESES_BAJA,
                                 widget=forms.Select(attrs={"class": "form-control"}),
                                 label='Mes de baja')

    DIAS_BAJA = (("", "---------"),)
    for dia in range(1, 32):
        DIAS_BAJA = DIAS_BAJA + ((dia, dia),)

    dia_baja = forms.ChoiceField(choices=DIAS_BAJA,
                                 widget=forms.Select(attrs={"class": "form-control"}),
                                 label='Día de baja')

    def __init__(self, *args, **kwargs):
        super(JovenAbandonanNSForm, self).__init__(*args, **kwargs)
        self.fields['nivel_escolar'].queryset = NivelEscolar.objects.filter(activo=True, id__in=[4, 6])
        self.fields['carrera_abandona'].queryset = Carrera.objects.filter(activo=True, tipo='ns')
        self.fields['causa_baja_ns'].queryset = CausalBaja.objects.filter(activo=True, id__in=[11, 12, 13, 14, 15, 16, 17])


class ProcesoTrabajadorSocialJANSForm(forms.ModelForm):
    class Meta:
        model = ProcesoTrabajadorSocialJANS
        fields = [
            'causa_desvinculacion',
            "reincorporado_educacion",
            'requiere_empleo',
            'oficio_conoce',
            'causa_no_requiere_empleo',
            'observaciones_empleo'
        ]
        widgets = {
            'causa_desvinculacion': forms.Select(attrs={'class': 'form-control'}),
            'oficio_conoce': forms.Select(attrs={'class': 'form-control'}),
            'causa_no_requiere_empleo': forms.Select(attrs={'class': 'form-control'}),
            "observaciones_empleo": forms.Textarea(attrs={"class": "form-control", 'rows': 3}),
        }
        labels = {
            "causa_desvinculacion": "Causa de la desvinculación del nivel superior",
            "oficio_conoce": "Oficio que conoce",
            'causa_no_requiere_empleo': "Causa no requiere empleo",
            'observaciones_empleo': "Observaciones para el empleo"
        }

    reincorporado_educacion = forms.ChoiceField(choices=(
                                               ("", "---------"),
                                               (0, "Curso diurno"),
                                               (1, "Curso por encuentro"),
                                               (2, "Curso a distancia")),
                                               widget=forms.Select(
                                               attrs={"class": "form-control"}),
                                               label='Reincorporado a educación superior',
                                               required=True)

    requiere_empleo = forms.ChoiceField(choices=(
                            ("", "---------"),
                            ("S", "Sí"),
                            ("N", "No")),
                             widget=forms.Select(
                             attrs={"class": "form-control"}), label='Requiere empleo', required=True)

    def __init__(self, *args, **kwargs):
        super(ProcesoTrabajadorSocialJANSForm, self).__init__(*args, **kwargs)
        self.fields['causa_desvinculacion'].queryset = CausalDesvinculacionNS.objects.filter(activo=True, id__in=[1,2,3,4,5,6])
        self.fields['oficio_conoce'].queryset = Carrera.objects.filter(activo=True, tipo__in=['oc', 'nm'])
        self.fields['causa_no_requiere_empleo'].queryset = CausalNoRequiereEmpleo.objects.filter(activo=True,  id__in=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])


class ProcesoDireccionMEmpleoJANSForm(forms.ModelForm):
    class Meta:
        model = ProcesoDireccionMEmpleoJANS
        fields = [
            'ubicado',
            'ubicacion',
            'organismo',
            'municipio_entidad',
            'entidad',
            'causa_no_ubicacion'
        ]
        widgets = {
            'ubicacion': forms.Select(attrs={'class': 'form-control'}),
            'organismo': forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'municipio_entidad': forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'entidad': forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'causa_no_ubicacion': forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),

        }
        labels = {
            "ubicacion": "Ubicación",
            "municipio_entidad": "Municipio de la entidad",
            'causa_no_ubicacion': "Causa no ubicación",
        }

    ubicado = forms.ChoiceField(choices=(("S", "Sí"), ("N", "No")),
                                         widget=forms.Select(
                                         attrs={"class": "form-control"}), label='Ubicado', required=True)

    def __init__(self, *args, **kwargs):
        super(ProcesoDireccionMEmpleoJANSForm, self).__init__(*args, **kwargs)
        self.fields['ubicacion'].queryset = Ubicacion.objects.filter(activo=True)
        self.fields['organismo'].queryset = Organismo.objects.filter(activo=True)
        self.fields['entidad'].queryset = Entidad.objects.filter(estado=True)
        self.fields['causa_no_ubicacion'].queryset = CausalNoUbicado.objects.filter(activo=True, id__in=[1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12])


class ControlJovenAbandonanNSForm(forms.ModelForm):
    class Meta:
        model = ControlJovenAbandonanNS
        fields = [
            'incorporado',
            'ubicacion',
            'organismo',
            'municipio',
            'entidad',
            'causa_no_incorporado'
        ]
        widgets = {
            'incorporado': forms.Select(attrs={'class': 'form-control'}),
            'ubicacion': forms.Select(attrs={'class': 'form-control'}),
            'organismo': forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'municipio': forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'entidad': forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'causa_no_incorporado': forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),

        }
        labels = {
            "ubicacion": "Ubicación",
            "municipio": "Municipio de la entidad",
            'causa_no_incorporado': "Causa no incorporado",
        }

    def __init__(self, *args, **kwargs):
        super(ControlJovenAbandonanNSForm, self).__init__(*args, **kwargs)
        self.fields['incorporado'].queryset = EstadoIncorporado.objects.filter(activo=True, id__in=[1, 2])
        self.fields['ubicacion'].queryset = Ubicacion.objects.filter(activo=True)
        self.fields['organismo'].queryset = Organismo.objects.filter(activo=True)
        self.fields['entidad'].queryset = Entidad.objects.filter(estado=True)
        self.fields['causa_no_incorporado'].queryset = CausalNoIncorporado.objects.filter(activo=True, id__in=[1, 2, 3, 4, 5, 6, 7, 8, 9])


class CausalNoRequiereEmpleoForm(forms.ModelForm):
    class Meta:
        model = CausalNoRequiereEmpleo
        fields = ["causa"]
        widgets = {
            'causa': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Escriba la causa'}),
        }


class CausalDesvinculacionNSForm(forms.ModelForm):
    class Meta:
        model = CausalDesvinculacionNS
        fields = ["causa"]
        widgets = {
            'causa': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Escriba la causa de desvinculación'}),
        }


                # ----------------codigo de daniel (FIN)--------------
