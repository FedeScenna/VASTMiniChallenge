import os
import re
import datetime
import datatable as dt

cwd = os.getcwd()
medios = os.listdir(cwd + '/data/News Articles')

df = dt.Frame(noticia=[], medio=[], autor=[], titulo=[], fecha=[], lugar=[], cuerpo=[])
fallidas = dt.Frame(medio=[], noticia=[], path=[])
for medio in medios:
    noticias = os.listdir(cwd + '/data/News Articles/' + medio)
    for noticia in noticias:

        # METER TRY EXCEPT EN CADA REGEX PARA EVITAR ERRORES CUANDO NO APARECE ALGUNO DE LOS CAMPOS

        print('medio: ' + medio + ' noticia: ' + noticia)
        texto = open(cwd + '/data/News Articles/' + medio + '/' + noticia, encoding='latin-1').read()
        try:
            title = re.search(r'TITLE:.*\n', texto)
            if title:
                titulo = re.search(r'TITLE:.*\n', texto).group()[7:-2]
            else:
                titulo = ''

            fecha = ''
            published = re.search(r'PUBLISHED:.*\n', texto)
            if published:
                try: 
                    fecha = datetime.datetime.strptime(re.search(r'PUBLISHED:.*\n', texto).group()[11:-1].strip(), '%Y/%m/%d')
                except:
                    fecha = datetime.datetime.strptime(re.search(r'PUBLISHED:.*\n', texto).group()[11:-1].strip(), '%d %B %Y')
            else:
                fecha = ''

            location = re.search(r'LOCATION:.*\n', texto)
            if location:
                lugar = location.group()[10:-2]
            else:
                lugar = ''

            author = re.search(r'AUTHOR:.*\n', texto)
            if author:
                autor = re.search(r'AUTHOR:.*\n', texto).group()[8:-2]
            else:
                autor = ''

            if location:
                inicio_cuerpo = re.search(r'LOCATION:.*\n', texto).span()[1] + 1
            else:
                inicio_cuerpo = re.search(r'PUBLISHED:.*\n', texto).span()[1] + 1

            cuerpo = texto[inicio_cuerpo:].strip()

            fila = dt.Frame({"noticia": [noticia], "medio": [medio], "autor": [autor], "titulo" : [titulo], "fecha" : [fecha.strftime('%Y%m%d')], "lugar" : [lugar], "cuerpo" : [cuerpo]})

            df.rbind(fila)

        except:
            fila = dt.Frame({"medio": [medio], "noticia" : [noticia], "path" : [(cwd + '/data/News Articles/' + medio + '/' + noticia)]})
            fallidas.rbind(fila)


df.to_csv(cwd + '/data/noticias.csv')
fallidas.to_csv(cwd + '/data/noticias-fallidas.csv')