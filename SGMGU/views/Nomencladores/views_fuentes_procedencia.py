# -*- coding: utf-8 -*-
from SGMGU.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from SGMGU.views.utiles import *


@login_required
@permission_required(['administrador'])
def gestion_fuentes_procedencia(request):
    fuetes_procedencia = FuenteProcedencia.objects.all()
    return render(request, "FuentesProcedencia/gestion_fuentes_procedencia.html", locals())


@login_required
@permission_required(['administrador'])
def registrar_fuente_procedencia(request):
    if request.method == 'POST':
        form = FuenteProcedenciaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "La fuente de procedencia se ha registrado con éxito.")
            return redirect('/fuentes_procedencia')
    else:
        form = FuenteProcedenciaForm()
    context = {'form': form, 'nombre_form': "Registrar Fuente Procedencia"}
    return render(request, "FuentesProcedencia/registrar_fuente_procedencia.html", context)


@login_required
@permission_required(['administrador'])
def modificar_fuente_procedencia(request, id_fuente_procedencia):
    fuentes_procedencia = FuenteProcedencia.objects.get(id=id_fuente_procedencia)
    if request.method == 'POST':
        form = FuenteProcedenciaForm(request.POST, instance=fuentes_procedencia)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "La fuente de procedencia se ha modificado con éxito.")
            return redirect('/fuentes_procedencia')
    else:
        form = FuenteProcedenciaForm(instance=fuentes_procedencia)
    context = {'form': form}
    return render(request, "FuentesProcedencia/modificar_fuente_procedencia.html", context)


@login_required
@permission_required(['administrador'])
def eliminar_fuente_procedencia(request, id_fuente_procedencia):
    fuente_procedencia = FuenteProcedencia.objects.get(id=id_fuente_procedencia)
    fuente_procedencia.activo = False
    fuente_procedencia.save()
    messages.add_message(request, messages.SUCCESS, "La fuente de procedencia se ha eliminado con éxito.")
    return redirect('/fuentes_procedencia')


# @login_required
# @permission_required(['administrador'])
# def activar_nivel_escolar(request, id_nivel_escolar):
#     nivel_escolar = NivelEscolar.objects.get(id=id_nivel_escolar)
#     nivel_escolar.activo = True
#     nivel_escolar.save()
#     messages.add_message(request, messages.SUCCESS, "El nivel escolar se ha activado con éxito.")
#     return redirect('/niveles_escolares')
