# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from SGMGU.views.utiles import *


@login_required()
@permission_required(['administrador', 'organismo', 'dpts', 'dpt_ee'])
def descargar_gforza(request):

    return render(request, "DescargarGFORZA/descargar_gforza.html")
