# -*- coding: utf-8 -*-
from SGMGU.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from SGMGU.views.utiles import *


@login_required
@permission_required(['administrador'])
def gestion_categorias_usuario(request):
    categorias_usuario = Categoria_usuario.objects.all()
    return render(request, "Nomencladores/CategoriaUsuario/gestion_categoria_usuario.html", locals())


@login_required
@permission_required(['administrador'])
def registrar_categoria_usuario(request):
    if request.method == 'POST':
        form = CategoriaUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "La categoría de usuario se ha registrado con éxito.")
            return redirect('/categorias_usuario')
    else:
        form = CategoriaUsuarioForm()
    context = {'form': form, 'nombre_form': "Registrar Categoría de usuario"}
    return render(request, "Nomencladores/CategoriaUsuario/registrar_categoria_usuario.html", context)


@login_required
@permission_required(['administrador'])
def modificar_categoria_usuario(request, id_categoria_usuario):
    categoria_usuario = Categoria_usuario.objects.get(id=id_categoria_usuario)
    if request.method == 'POST':
        form = CategoriaUsuarioForm(request.POST, instance=categoria_usuario)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "La categoría de usuario se ha modificado con éxito.")
            return redirect('/categorias_usuario')
    else:
        form = CategoriaUsuarioForm(instance=categoria_usuario)
    context = {'form': form}
    return render(request, "Nomencladores/CategoriaUsuario/modificar_categoria_usuario.html", context)


@login_required
@permission_required(['administrador'])
def eliminar_categoria_usuario(request, id_categoria_usuario):
    categoria_usuario = Categoria_usuario.objects.get(id=id_categoria_usuario)
    categoria_usuario.delete()
    messages.add_message(request, messages.SUCCESS, "La categoría de usuario se ha eliminado con éxito.")
    return redirect('/categorias_usuario')


# @login_required
# @permission_required(['administrador'])
# def activar_nivel_escolar(request, id_nivel_escolar):
#     nivel_escolar = NivelEscolar.objects.get(id=id_nivel_escolar)
#     nivel_escolar.activo = True
#     nivel_escolar.save()
#     messages.add_message(request, messages.SUCCESS, "El nivel escolar se ha activado con éxito.")
#     return redirect('/niveles_escolares')
