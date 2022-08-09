# using flask_restful

from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from numpy import source
import spacy
import random,string
import es_core_news_md
from spacy.tokens import Span
import unidecode
import jellyfish
import re
from flask import Flask


# Crear la app Flask
app = Flask(__name__)
# Crear el objeto api
api = Api(app)


alphabets= "([A-Za-z])" 
prefixes = "(Sr|Lic|Ing|ante|contra|cuasi|en|entre|ex|extra)[.]" 
suffixes = "(SA|CV|Jr|Sr|azo|ito|logía|logia)" 
starters = "(Mr|Mrs|Ms|Dr|Lic|El|Ella|Esto|Ellos|Ellas|Aquellos|Nuestro|Nosotros|Pero|Como sea|Es|Donde sea|Como sea|Por lo que sea|si|no|porque|que|mientras )" 
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)" 
websites = "[.](com|net|org|io|gov)"




class NLP(Resource):

    def post(self):
        # cargar la libreria pequeña de spacy en español
        #eficiencia
        nlpspacy = es_core_news_md.load()
        nlp = spacy.load("./newmodels/models/output/model-last")
        nlp.add_pipe('sentencizer')
        #precision
        #nlp = spacy.load('es_dep_news_trf')
        #declarar elementos y objetos quer vamos a necesitar de la api para poder utilizarlos en el nlp
        diccionario_consulta_db = {}
        lista_de_id = {}
        request_json = request.get_json()
        keyword = request_json.get('keyword')
        lista = request_json.get('listado')
        #agregar la informacion a un listado
        diccionario_consulta_db = {}
        def split_into_sentences(text): 
            text = " " + text + " " 
            text = text.replace("\n"," ") 
            text = re.sub(prefixes,"\\1<prd>",text) 
            text = re.sub(websites,"<prd>\\1",text) 
            if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>") 
            text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text) 
            text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text) 
            text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text) 
            text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text) 
            text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text) 
            text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text) 
            text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text) 
            if "”" in text: text = text.replace(".”","”.") 
            if "\"" in text: text = text.replace(".\"","\".") 
            if "!" in text: text = text.replace("!\"","\"!") 
            if "?" in text: text = text.replace("?\"","\"?") 
            text = text.replace(".",".<stop>") 
            text = text.replace("?","?<stop>") 
            text = text.replace("!","!<stop>") 
            text = text.replace("<prd>",".") 
            sentences = text.split("<stop>") 
            sentences = sentences[:-1] 
            sentences = [s.strip() for s in sentences] 
            return sentences
        
        arregloX = []
        for a in range(len(lista)):
            keys = lista[a]["id"]
            value = lista[a]["source"]
            diccionario_consulta_db.update({keys:(value)})
        for x, y in diccionario_consulta_db.items():
            # Sin acentos el texto source
            unaccented_string = unidecode.unidecode(y).lower()
            #crear una lista de los enunciados donde puede existir la palabra ( buscarla )
            keywordparsed = unidecode.unidecode(keyword).strip().lower()

            arregloX.append((split_into_sentences(unaccented_string)))

            for y in arregloX:
                for sentence in y:
                    if(keywordparsed in sentence):
                        SpacySentence = nlp(sentence)
                        for ent in SpacySentence.ents:
                            entparsed =  unidecode.unidecode(ent.text) 
                            if(keywordparsed in entparsed):
                                similitud = jellyfish.jaro_distance(keyword, ent.text) 
                                print("1.- Agregada por entrenamiento Spacy - Apolo")
                                lista_de_id.update({f"{x}-{keywordparsed.lower()}": round(similitud,2)})     

                    
            salida = jsonify({'Keyword': keywordparsed ,  'Lista': lista_de_id  })
            return salida

api.add_resource(NLP, '/nlp')
app.run(debug=True)

## si aparece entrenado por nosotros => 0-1 RESULTADO FINAL
## si spacy lo tienen como entidad nos muestre el de spacy => 0.52 
## resultado 0 
## modelo spacy 