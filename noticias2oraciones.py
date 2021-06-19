import os
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
import datatable as dt

cwd = os.getcwd()
noticias = dt.fread(cwd + '/data/noticias.csv')
nlp = spacy.load("en_core_web_trf")

# config = {"punct_chars": None}
nlp.add_pipe('spacytextblob', 'sentencizer')

i = 0
textos = noticias[:, f.cuerpo].to_list()[0]

df = dt.Frame(noticia=[], medio=[], autor=[], titulo=[], fecha=[], lugar=[], oracion=[],
              sustantivos=[], adjetivos=[], verbos=[],
              personas=[], organizaciones=[], lugares=[], fechas=[], geopoliticos=[], eventos=[],
              polaridad=[], subjetividad=[])

total = str(len(textos))
for texto in textos:

    print(str(i) + ' de ' + total)

    oraciones = list(nlp(texto).sents)

    for oracion in oraciones:

        if len(oracion.text.strip()) is 0:
            continue

        noticia = noticias[i,0]
        medio = noticias[i,1]
        autor = noticias[i,2]
        titulo = noticias[i,3]
        fecha = str(noticias[i,4])
        lugar = noticias[i,5]

        sustantivos = ','.join([t.lemma_.lower() for t in oracion if t.pos_ is 'NOUN'])
        adjetivos = ','.join([t.lemma_.lower() for t in oracion if t.pos_ is 'ADJ'])
        verbos = ','.join([t.lemma_.lower() for t in oracion if t.pos_ is 'VERB'])

        personas = ','.join([e.text for e in oracion.ents if e.label_ is 'PERSON'])
        organizaciones = ','.join([e.text for e in oracion.ents if e.label_ is 'ORG'])
        lugares = ','.join([e.text for e in oracion.ents if e.label_ is 'LOC'])
        fechas = ','.join([e.text for e in oracion.ents if e.label_ is 'DATE'])
        geopoliticos = ','.join([e.text for e in oracion.ents if e.label_ is 'GPE'])
        eventos = ','.join([e.text for e in oracion.ents if e.label_ is 'EVENT'])

        polaridad = oracion._.polarity
        subjetividad = oracion._.subjectivity
        # palabras_subjetivas = oracion._.assessments[0][0]

        fila = dt.Frame({"noticia": [noticia], "medio": [medio], "autor": [autor], "titulo" : [titulo], "fecha" : [fecha], "lugar" : [lugar], "oracion" : [oracion.text.strip()],
                         "sustantivos" : [sustantivos], "adjetivos" : [adjetivos], "verbos" : [verbos],
                         "personas" : [personas], "organizaciones" : [organizaciones], "lugares" : [lugares], "fechas" : [fechas],"geopoliticos" : [geopoliticos], "eventos" : [eventos],
                         "polaridad" : [polaridad], "subjetividad" : [subjetividad]})

        df.rbind(fila)
    
    i += 1

# TODO: ver aca POR QUE no guarda: NotImplementedError: Cannot write values of stype obj64
df.to_csv(cwd + '/data/oraciones.csv')

