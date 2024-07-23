### Import CSV y cargar datos para poblar db ###
import csv
from .models import Comuna

def cargar_data_import_regiones():
    with open('regiones-chile.csv', 'r') as file:
        data = csv.reader(file, delimiter=';')
        data = list(data)

    data.pop(0)

    for d in data:
        Comuna.objects.create(
            nombre_comuna = d[3],
            region = d[0]
        )

# funciones de utilidad

cleaned_data = lambda x:{k:v for k,v in x.items() if k != 'csrfmiddlewaretoken'}