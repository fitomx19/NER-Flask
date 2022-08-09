# using flask_restful
from ast import keyword
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


class NLP(Resource):
    def post(self):
        # cargar la libreria pequeña de spacy en español
        #eficiencia
        nlpspacy = spacy.load('es_core_news_md')
        nlp = spacy.load("../models/output/newModel/model-best")
        
        #precision
        #nlp = spacy.load('es_dep_news_trf')
        spacy.prefer_gpu() #siempre buscamos usar los nucleos de la gpu
    
        #declarar elementos y objetos quer vamos a necesitar de la api para poder utilizarlos en el nlp
        diccionario_consulta_db = {}
        conteo = 0
        lista_de_id = {}
        

        request_json = request.get_json()
        keyword = request_json.get('keyword')
        lista = request_json.get('listado')

        diccionario_consulta_db = {}
        for a in range(len(lista)):
            keys = lista[a]["id"]
            value = lista[a]["source"]
            diccionario_consulta_db.update({keys:(value)})
        #print(diccionario_consulta_db)
        def get_random_string(length):
            # choose from all lowercase letter
            letters = string.ascii_lowercase
            result_str = ''.join(random.choice(letters) for i in range(length))
            return result_str
   #def agregar_keywords():
            diccionario_nlp = {'Mercadotecnia Mexico': 2} #diccionario de keywords dificiles
            # print(diccionario)
            #asignamos un label de entidad a estas keywords para poder utilizarlas despues
            for key in diccionario_nlp:
                docAdd = nlp(f'{key} es una organizacion')
                ORG = doc.vocab.strings[u'ORG'] #para organizaciones
                #PER = doc.vocab.strings[u'PER'] para personas
                new_ent = Span(docAdd, 0, diccionario_nlp[key], label=ORG)
                try:
                    doc.ents = list(doc.ents) + [new_ent]
                    #print("palabras agregadas")
                except ValueError: #Este error surge cuando ya fueron previamente cargadas las keywords
                    continue 

        for x, y in diccionario_consulta_db.items():
            # Sin acentos
            unaccented_string = unidecode.unidecode(y)
            doc = nlp(unaccented_string)        
            #keywordnlp = nlp(keyword)   
            #agregar_keywords()                
            if doc.ents:   
               
                print("------")
                #print(len(doc.ents))    
                for ent in doc.ents: 
                    #print(len(ent))   
                    keywordparsed  = keyword.replace(" ", "").replace("\n","")      
                    re.sub(r'[^a-zA-Z]', '', keywordparsed)  
                    entparsed =  ent.text   
                    re.sub(r'[^a-zA-Z]', '', keywordparsed)  
                    if keywordparsed in entparsed:
                        similitud = jellyfish.jaro_distance(keyword, ent.text)
                        print(f"{keyword} -> {ent.text} - {ent.label_} - {similitud}")                       
                        if ent.label_ == "ORG" or ent.label_ == "PER" or "MISC":                         
                                                                      
                        #lista_de_id.append(x)
                            rdstring = get_random_string(8)
                        #0.89629629629629637 
                            lista_de_id.update({f"{rdstring}-{x} - {keyword} - {ent.text} - {ent.label_} ": round(similitud,2)})
                            conteo += 1
                        #similitud_spacy =  keywordnlp.similarity(ent)
                        #lista_de_id_spacy.update({f"id-{rdstring}-{x} -  {keyword.lower()} - {ent.text.lower()} - {ent.label_} - spacy ": similitud_spacy})
                        #print("Similarity:", token1.similarity(token2))
                    
                                                                                   
            else:
                print(f"No hay entidades en este documento alerta:  {x}")
      
        salida = jsonify({'Keyword': keyword , 'Total_Alertas': conteo , 'Lista': lista_de_id  })
        return salida
class NLPTest(Resource):
    def post(self):
        request_json = request.get_json()
        lista = request_json.get('listado')
        keyword = request_json.get('keyword')
        #print(lista)
        diccionario_consulta_db = {}
        
        

        for a in range(len(lista)):
                keys = lista[a]["id"]
                value = lista[a]["source"]
                diccionario_consulta_db.update({keys: str(value)})
        
        return jsonify({"keyword":  keyword , "listado": diccionario_consulta_db , "longitud": len(lista)})
class NLPVersionTwo(Resource):

    def post(self):     
        # cargar la libreria pequeña de spacy en español
        #eficiencia
        nlpspacy = es_core_news_md.load()
        nlp = spacy.load("./newmodels/models/output/model-best")
        nlp.add_pipe('sentencizer')
       
        spacy.prefer_gpu() #siempre buscamos usar los nucleos de la gpu
    
        #declarar elementos y objetos quer vamos a necesitar de la api para poder utilizarlos en el nlp
        diccionario_consulta_db = {}
        lista_de_id = {}
        request_json = request.get_json()
        keyword = request_json.get('keyword')
        lista = request_json.get('listado')
                
        #agregar la informacion a un listado
        diccionario_consulta_db = {}
        for a in range(len(lista)):
            keys = lista[a]["id"]
            value = lista[a]["source"]
            diccionario_consulta_db.update({keys:(value)})
        #ciclo a las diferentes alertas
        for x, y in diccionario_consulta_db.items():
            # Sin acentos el texto source
            unaccented_string2 = unidecode.unidecode(y)       
            #crear una lista de los enunciados donde puede existir la palabra ( buscarla )
            keywordparsed = unidecode.unidecode(keyword).strip()
            if keywordparsed in unaccented_string2:
                #dividir en enunciados y solo buscar en los textos que aparecen para no hacer tantas iteraciones
                #def obtener_entidades(keywordparsed,unaccented_string):
                             
                      
                for ent in unaccented_string2.ents:                     
                    entparsed =  unidecode.unidecode(ent.text)
                        
                #PRIMERA BUSQUEDA BUSQUEDA SPACY
                    if keywordparsed in entparsed:
                        #si el texto tiene ya entidad definida arrojara un resultado de 1                        
                        if(ent.label_ == "PER" or ent.label_ == "ORG" or ent.label_ == "MISC"):                            
                            lista_de_id.update({f"{x}-{keywordparsed}": 0.75})       
                                            
                segundo_intento = nlpspacy(unaccented_string2)
                for sent in segundo_intento.ents:
                #SEGUNDA BUSQUEDA - BUSQUEDA SPACY/APOLO
                    if keywordparsed in sent.text:          
                        key_to_lookup = f"{x}-{keywordparsed}"
                        if not key_to_lookup in lista_de_id:
                            lista_de_id.update({key_to_lookup: 1})
                            
                #TERCERA BUSQUEDA - BUSQUEDA NORMAL        
                if(keywordparsed in unaccented_string2):
                    key_to_lookup = f"{x}-{keywordparsed}"
                    if not key_to_lookup in lista_de_id:       
                        lista_de_id.update({key_to_lookup: 0.5})                                   
            else:
                  print("5.-No se encontro")    

        salida = jsonify({'Keyword': keywordparsed ,  'Lista': lista_de_id  })
        return salida
api.add_resource(NLP, '/nlp')
api.add_resource(NLPTest, '/pln')
api.add_resource(NLPVersionTwo, '/nlp/two')
# driver function


app.run(debug=True)


## si aparece entrenado por nosotros => 0-1 RESULTADO FINAL
## si spacy lo tienen como entidad nos muestre el de spacy => 0.52 
## resultado 0 
## modelo spacy 