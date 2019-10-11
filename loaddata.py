import os

FIXTURES = [
    # 'NivelEscolar',
    # 'CausalNoIncorporado',
    # 'CausalNoAceptacion',
    # 'Ubicacion',
    # 'CausalNoUbicado',
    # 'CausalBaja',
    # 'FuenteProcedencia',
    # 'EstadoIncorporado',
    # 'MotivoEgreso',
    # 'Delito',
    # 'Asociacion',
    # 'Discapacidad',
    # 'CausalInterrupcion',
    'ActividadInterrupto',
    # 'CausalNoReubicacion',
]

for fixture in FIXTURES:
    os.system('python manage.py loaddata ' + fixture)
