# funciones de utilidad

cleaned_data = lambda x:{k:v for k,v in x.items() if k != 'csrfmiddlewaretoken'}