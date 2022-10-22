# using flask_restful

from time import process_time_ns
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from numpy import source
import spacy
from spacy.matcher import Matcher
import random,string
import es_core_news_md
from spacy.tokens import Span
import unidecode
from re import search
from flask import Flask
from spacy.matcher import PhraseMatcher
import nltk
from nameparser.parser import HumanName

# Crear la app Flask
app = Flask(__name__)
# Crear el objeto api
api = Api(app)



class NLPVersionTwo(Resource):

    def post(self):     
        # cargar la libreria pequeña de spacy en español
        #eficiencia
        nlpspacy = es_core_news_md.load()
        nlpspacyMatcher = es_core_news_md.load()
        nlp = spacy.load("./models/output/model-best")
        nlp.add_pipe('sentencizer')
        ruler2 = nlpspacyMatcher.add_pipe("entity_ruler")
        spacy.prefer_gpu() #siempre buscamos usar los nucleos de la gpu
    
        #declarar elementos y objetos quer vamos a necesitar de la api para poder utilizarlos en el nlp
        diccionario_consulta_db = {}
        lista_de_id = []
        request_json = request.get_json()
        keyword = request_json.get('keyword')
        lista = request_json.get('listado')

        keywordparsed = unidecode.unidecode(keyword).strip()
        keywordUPPER = keywordparsed.upper() 

             #patrones para empresas
        patterns = [{"label": "ORG", "pattern": "en"},
                                {"label": "ORG", "pattern": [{"LOWER": "en"}, {"TEXT": keywordparsed}]},
                                {"label": "ORG", "pattern": [{"LOWER": keywordparsed.upper()}]},
                                {"label": "ORG", "pattern": [{"LOWER": "la"}, {"TEXT": keywordparsed}]},
                                {"label": "ORG", "pattern": [{"LOWER": "la"}, {"LOWER": keywordparsed}]},
                                {"label": "ORG", "pattern": [{"LOWER": "empresa"}, {"TEXT": (keyword).upper()}]},
                                {"label": "ORG", "pattern": [ {"TEXT": keywordparsed}, {"LOWER": "de México"}]},
                                {"label": "ORG", "pattern": [ {"TEXT": keywordparsed}, {"LOWER": "SA DE CV"}]},
                                {"label": "ORG", "pattern": [ {"LOWER": "La empresa"}, {"ORTH": keywordUPPER}, {"LOWER": "de MEXICO S.A. de C.V"}]},
                                ]
        ruler2.add_patterns(patterns)
        matcher = Matcher(nlpspacyMatcher.vocab)
        #parece que tenemos problemas con las keywords compuestas: Si Vale
        
        trySplitKeywordparsed = keywordparsed.split(' ')

        if (len(trySplitKeywordparsed) == 2):
          
            patterns = [
                [{"TEXT": "empresa"}, {"TEXT": (trySplitKeywordparsed[0])} , {"TEXT": (trySplitKeywordparsed[1])}],
                [{"TEXT": "de"}, {"TEXT": (trySplitKeywordparsed[0])} , {"TEXT": (trySplitKeywordparsed[1])}],
                [{"TEXT": "DE"}, {"TEXT": (trySplitKeywordparsed[0]).upper()} , {"TEXT": (trySplitKeywordparsed[1]).upper()}],
                [{"TEXT": "DE"}, {"TEXT": (trySplitKeywordparsed[0]).upper()} , {"TEXT": (trySplitKeywordparsed[1]).upper()}],
                [{"TEXT": "la"}, {"TEXT": (trySplitKeywordparsed[0]).upper()} , {"TEXT": (trySplitKeywordparsed[1]).upper()}],
                [{"TEXT": "LA"}, {"TEXT": (trySplitKeywordparsed[0]).upper()} , {"TEXT": (trySplitKeywordparsed[1]).upper()}],
                [{"TEXT": "EL"}, {"TEXT": (trySplitKeywordparsed[0]).upper()} , {"TEXT": (trySplitKeywordparsed[1]).upper()}],
                [{"TEXT": "el"}, {"TEXT": (trySplitKeywordparsed[0]).upper()} , {"TEXT": (trySplitKeywordparsed[1]).upper()}],
                [{"LOWER": "empresa"}, {"TEXT": (trySplitKeywordparsed[0]).lower()} , {"TEXT": (trySplitKeywordparsed[1]).lower()}],
                [{"TEXT": "empresa"}, {"TEXT": (trySplitKeywordparsed[0]).upper()} , {"TEXT": (trySplitKeywordparsed[1]).upper()}],
                [{"TEXT": (trySplitKeywordparsed[0])} , {"TEXT": (trySplitKeywordparsed[1])}, {"LOWER": "de México"}],
                [{"TEXT": (trySplitKeywordparsed[0])} , {"TEXT": (trySplitKeywordparsed[1])}, {"LOWER": "Mexico"}],
                [{"TEXT": (trySplitKeywordparsed[0])} , {"TEXT": (trySplitKeywordparsed[1])}, {"LOWER": "S.A"}],
                [{"TEXT": (trySplitKeywordparsed[0]).upper()} , {"TEXT": (trySplitKeywordparsed[1])}, {"LOWER": "S.A"}],
                [{"TEXT": (trySplitKeywordparsed[0]).upper()} , {"TEXT": (trySplitKeywordparsed[1])}, {"TEXT": "S.A"}],
                [{"TEXT": (trySplitKeywordparsed[0]).upper()} , {"TEXT": (trySplitKeywordparsed[1]).upper()}, {"TEXT": "S.A"}],
                [{"TEXT": (trySplitKeywordparsed[0].upper())} , {"TEXT": (trySplitKeywordparsed[1]).upper()}, {"LOWER": "MEXICO"}],
                [{"TEXT": (trySplitKeywordparsed[0].upper())} , {"TEXT": (trySplitKeywordparsed[1]).upper()}, {"TEXT": "MEXICO"}],
                [{"TEXT": "abre"} , {"TEXT": (trySplitKeywordparsed[0].upper())} , {"TEXT": (trySplitKeywordparsed[1]).upper()} ],
                [{"TEXT": "abre"} , {"TEXT": (trySplitKeywordparsed[0])} , {"TEXT": (trySplitKeywordparsed[1])} ],
                [{"TEXT": "inagura"} , {"TEXT": (trySplitKeywordparsed[0].upper())} , {"TEXT": (trySplitKeywordparsed[1]).upper()}, ],
                [{"TEXT": "inagura"} , {"TEXT": (trySplitKeywordparsed[0])} , {"TEXT": (trySplitKeywordparsed[1])}, ],
                [{"TEXT": "cierra"} , {"TEXT": (trySplitKeywordparsed[0].upper())} , {"TEXT": (trySplitKeywordparsed[1]).upper()}, ],
                [{"TEXT": "cierra"} , {"TEXT": (trySplitKeywordparsed[0])} , {"TEXT": (trySplitKeywordparsed[1])}, ],
              
              
                ]
            matcher.add("patrones", patterns)

        elif (len(trySplitKeywordparsed) == 3):
            patterns = [
             [{"TEXT": "empresa"}, {"TEXT": (trySplitKeywordparsed[0])} , {"TEXT": (trySplitKeywordparsed[1])},{"TEXT": (trySplitKeywordparsed[2])}],
                [{"LOWER": "empresa"}, {"TEXT": (trySplitKeywordparsed[0]).lower()} , {"TEXT": (trySplitKeywordparsed[1]).lower()},{"TEXT": (trySplitKeywordparsed[2])}],
                [{"TEXT": "empresa"}, {"TEXT": (trySplitKeywordparsed[0]).upper()} , {"TEXT": (trySplitKeywordparsed[1]).upper()},{"TEXT": (trySplitKeywordparsed[2])}],
                [{"TEXT": (trySplitKeywordparsed[0])} , {"TEXT": (trySplitKeywordparsed[1])}, {"TEXT": (trySplitKeywordparsed[2])}, {"LOWER": "de México"}],
                [{"TEXT": (trySplitKeywordparsed[0])} , {"TEXT": (trySplitKeywordparsed[1])}, {"TEXT": (trySplitKeywordparsed[2])}, {"LOWER": "Mexico"}],
                 [{"TEXT": (trySplitKeywordparsed[0])} , {"TEXT": (trySplitKeywordparsed[1])}, {"TEXT": (trySplitKeywordparsed[2])}, {"LOWER": "SA"}],
                ]
            matcher.add("patrones", patterns)
        else:
            patterns = [
                [{"TEXT": "empresa"}, {"TEXT": (keyword)}],
                [{"LOWER": "empresa"}, {"LOWER": (keyword).lower()}],
                [{"TEXT": "empresa"}, {"TEXT": (keyword).upper()}],
                [{"LOWER": "empresa"}, {"TEXT": (keyword).lower()}],
                [{"TEXT": keywordparsed}, {"LOWER": "de Mexico"}],
                [{"TEXT": keywordparsed}, {"LOWER": "Mexico"}],
                [{"TEXT": "de"}, {"TEXT": (keyword).upper()}],
                [{"TEXT": "DE"}, {"TEXT": (keyword).upper()}],
                [{"TEXT": "DE"}, {"TEXT": (keyword).upper()}],
                [{"TEXT": "la"}, {"TEXT": (keyword).upper()}],
                [{"TEXT": "LA"}, {"TEXT": (keyword).upper()}],
                [{"TEXT": "EL"}, {"TEXT": (keyword).upper()}],
                [{"TEXT": "el"}, {"TEXT": (keyword).upper()}],
                ]
            matcher.add("patrones", patterns)

    

        #agregar la informacion a un listado
        diccionario_consulta_db = {}
        for a in range(len(lista)):
            keys = lista[a]["ConsolaSubId"]
            value = lista[a]["Source"]
            diccionario_consulta_db.update({keys:(value)})
        #ciclo a las diferentes alertas
        for x, y in diccionario_consulta_db.items():
            element = {
                "Id":x
            }
            # Sin acentos el texto source
            unaccented_string2 = unidecode.unidecode(y)       
            #crear una lista de los enunciados donde puede existir la palabra ( buscarla )
           

            if keywordparsed.lower() in unaccented_string2.lower():
                #dividir en enunciados y solo buscar en los textos que aparecen para no hacer tantas iteraciones
                #def obtener_entidades(keywordparsed,unaccented_string):

                if(keywordparsed.lower() in unaccented_string2.lower()):
                    element.update({"Percent": 0.5, "Message":"Keyword existe en el Código"}) 
                

                apolo = nlp(unaccented_string2)      
                for ent in apolo.ents:                     
                    entparsed =  unidecode.unidecode(ent.text)
                        
                #PRIMERA BUSQUEDA BUSQUEDA SPACY
                    if keywordparsed.title() in entparsed:
                        #si el texto tiene ya entidad definida arrojara un resultado de 1    
                        test = keywordparsed.title()                    
                        if(ent.label_ == "PER" or ent.label_ == "ORG" or ent.label_ == "MISC"):                            
                             element.update({"Percent": 0.75, "Message":"Keyword Reconocido como PER - ORG - MISC en Spacy"})
                                            
                segundo_intento = nlpspacy(unaccented_string2)
                for sent in segundo_intento.ents:
                #SEGUNDA BUSQUEDA - BUSQUEDA SPACY/APOLO
                    if keywordparsed in sent.text:          
                        element.update({"Percent": 1, "Message":"Keyword Reconocido como PER - ORG - MISC en entrenamiento Apolo"})
                    if keywordparsed.title() in sent.text:          
                        key_to_lookup = f"{x}-{keywordparsed}"
                        if not key_to_lookup in lista_de_id:
                            element.update({"Percent": 1, "Message":"Keyword Reconocido como PER - ORG - MISC en entrenamiento Apolo"})
                            
                #TERCERA BUSQUEDA - BUSQUEDA SPACY ENTS + MATCHER
                
                tercer_intento = nlpspacyMatcher(unaccented_string2)
                for sent in tercer_intento.ents:
                    if keywordparsed in sent.text:          
                            element.update({"Percent": 1, "Message":"Keyword Reconocido como PER - ORG - MISC en entrenamiento Apolo Matcher"})
                #CUARTA BUSQUEDA - BUSQUEDA  MATCHER
                
                cuarto_intento = nlpspacyMatcher(unaccented_string2)
                matches = matcher(cuarto_intento)
               
                for match_id, start, end in matches:
                    string_id = nlpspacyMatcher.vocab.strings[match_id]  # obtener la representacion de la cadena
                    span = cuarto_intento[start:end]  # El match del span
                    #print(match_id, string_id, start, end, span.text) 
                    if keywordparsed in span.text.lower():       
                        element.update({"Percent": 1, "Message":"Keyword encontrado por Apolo Matcher"})

                quintoIntento = nlpspacyMatcher(unaccented_string2.upper())
                matchesQuinto = matcher(quintoIntento)
               
                for match_id, start, end in matchesQuinto:
                    string_id = nlpspacyMatcher.vocab.strings[match_id]  # obtener la representacion de la cadena
                    span = quintoIntento[start:end]  # El match del span
                    #print(match_id, string_id, start, end, span.text) 
                    if keywordparsed.lower() in span.text.lower():       
                        element.update({"Percent": 0.75, "Message":"Keyword encontrado por Matcher Forzando su busqueda"})

                #QUINTA BUSQUEDA - BUSQUEDA NORMAL                                
            else:
                  element.update({"Percent": 0, "Message":"Keyword no se encontró en el documento"}) 

            if not element in lista_de_id:
                    lista_de_id.append(element)
        salida = jsonify({'Keyword': keywordparsed ,  'Lista': lista_de_id  })
        return salida


def metodoSpacy(keyword,lista):
         # cargar la libreria pequeña de spacy en español
        #eficiencia
        nlpspacy = es_core_news_md.load()
        nlp = spacy.load("./models/output/model-best")
        nlp.add_pipe('sentencizer')
       
        spacy.prefer_gpu() #siempre buscamos usar los nucleos de la gpu
    
        #declarar elementos y objetos quer vamos a necesitar de la api para poder utilizarlos en el nlp
        diccionario_consulta_db = {}
        lista_de_id = []
       
        #agregar la informacion a un listado
        diccionario_consulta_db = {}
        for a in range(len(lista)):
            keys = lista[a]["ConsolaSubId"]
            value = lista[a]["Source"]
            diccionario_consulta_db.update({keys:(value)})
        #ciclo a las diferentes alertas
        for x, y in diccionario_consulta_db.items():
            element = {
                "Id":x
            }
            # Sin acentos el texto source
            unaccented_string2 = unidecode.unidecode(y)  
            keywordparsed = unidecode.unidecode(keyword).strip()
            if keywordparsed.lower() in unaccented_string2.lower():
                #dividir en enunciados y solo buscar en los textos que aparecen para no hacer tantas iteraciones
                #def obtener_entidades(keywordparsed,unaccented_string):

                if(keywordparsed.lower() in unaccented_string2.lower()):
                    key_to_lookup = f"{x}-{keywordparsed}"
                    if not key_to_lookup in lista_de_id:       
                        element.update({"Percent": 0.5, "Message":"Keyword existe en el Código"}) 

                apolo = nlp(unaccented_string2)      
                for ent in apolo.ents:                     
                    entparsed =  unidecode.unidecode(ent.text)
                        
                #PRIMERA BUSQUEDA BUSQUEDA SPACY
                    if keywordparsed.title() in entparsed:
                        #si el texto tiene ya entidad definida arrojara un resultado de 1    
                        test = keywordparsed.title()                    
                        if(ent.label_ == "PER" or ent.label_ == "ORG" or ent.label_ == "MISC"):                            
                             element.update({"Percent": 1, "Message":"Keyword Reconocido como PER - ORG - MISC en Spacy"})
                                            
                      
                #SEGUNDA BUSQUEDA - BUSQUEDA NORMAL        
                                                
            else:
                  element.update({"Percent": 0, "Message":"Keyword no se encontró en el documento"}) 

            if not element in lista_de_id:
                    lista_de_id.append(element)
        
        return lista_de_id

def metodoSpacyFisicas(keyword,texto):
    # cargar la libreria pequeña de spacy en español
    #eficiencia
    nlpspacy = es_core_news_md.load()

    a = []
    #ciclo a las diferentes alertas
    # Sin acentos el texto source
    unaccented_string2 = unidecode.unidecode(texto)  
    keywordparsed = unidecode.unidecode(keyword).strip()
    
   
            #dividir en enunciados y solo buscar en los textos que aparecen para no hacer tantas iteraciones
            #def obtener_entidades(keywordparsed,unaccented_string):
    apolo = nlpspacy(unaccented_string2)      
    for ent in apolo.ents:                     
        entparsed =  unidecode.unidecode(ent.text)               
        #PRIMERA BUSQUEDA BUSQUEDA SPACY
         
                           
        if(ent.label_ == "PER" or ent.label_ == "ORG" or ent.label_ == "MISC"):
                a.append(ent.text)
    return  a


class NLPPersonasFisicas(Resource):
  
    def post(self):  
            request_json = request.get_json()   
            keyword = request_json.get('keyword')
            lista = request_json.get('listado')      
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------- Filtrar Nombres ------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
            keywordparsed = unidecode.unidecode(keyword).strip().title()
            trySplitKeywordparsed = keywordparsed.split(' ')

            if(len(trySplitKeywordparsed) == 1):
                #este es un nombre,apellido simple
                metodoSpacy(keyword,lista)
                valorA = trySplitKeywordparsed[0]
                #a = metodoSpacy(valorA,lista) 
                nombres =  [valorA] 
                salida = jsonify({'Keyword': keywordparsed, 'Lista': nombres})
                return salida

            if(len(trySplitKeywordparsed) == 2):
                #este es un nombre con apellido o dos nombres
                #dividir uno y dos
                valorA = trySplitKeywordparsed[0]
                valorB = trySplitKeywordparsed[1]

                posibilidad1 = valorA+ " " +valorB
                posibilidad2 = valorB+ " " +valorA

                #a = metodoSpacy(posibilidad1,lista)
                #b = metodoSpacy(posibilidad2,lista)

                nombres =  [posibilidad1, posibilidad2] 
                salida = jsonify({'Keyword': keywordparsed, 'Lista': nombres})
                return salida

            if(len(trySplitKeywordparsed) == 3):
                #este es un nombre con apellidos o dos nombres y un apellido
                valorA = trySplitKeywordparsed[0]
                valorB = trySplitKeywordparsed[1]
                valorC = trySplitKeywordparsed[2]

                posibilidad1 = valorA+ " " + valorB + " " + valorC
                posibilidad2 = valorA+ " " + valorC + " " + valorB

                #a = metodoSpacy(posibilidad1,lista)
                #b = metodoSpacy(posibilidad2,lista)

                nombres =  [posibilidad1, posibilidad2] 
                salida = jsonify({'Keyword': keywordparsed, 'Lista': nombres})

                return salida

            if(len(trySplitKeywordparsed) == 4):
                #este es un nombre completo con dos nombres y dos apellidos
                valorA = trySplitKeywordparsed[0]
                valorB = trySplitKeywordparsed[1]
                valorC = trySplitKeywordparsed[1]
                valorD = trySplitKeywordparsed[1]

                posibilidad1 = valorA+ " " +valorB + " " + valorC + " " + valorD
                posibilidad2 = valorA+ " " +valorC + " " + valorB + " " + valorD
                posibilidad3 = valorA+ " " +valorC + " " + valorD + " " + valorB
                posibilidad4 = valorB+ " " +valorA + " " + valorC + " " + valorD
                posibilidad5 = valorB+ " " +valorA + " " + valorD + " " + valorC

                #a = metodoSpacy(posibilidad1,lista)
                #b = metodoSpacy(posibilidad2,lista)
                #c = metodoSpacy(posibilidad3,lista)
                #d = metodoSpacy(posibilidad4,lista)
                #e = metodoSpacy(posibilidad5,lista)


                nombres =  [posibilidad1, posibilidad2, posibilidad3, posibilidad4, posibilidad5] 
                salida = jsonify({'Keyword': keywordparsed, 'Lista': nombres})

                return salida

            if(len(trySplitKeywordparsed) >= 5):
                #este es un nombre compuesto , fuera de lo convencional 
                a = metodoSpacy(keyword,lista)
                salida = jsonify({'Keyword': keywordparsed, 'Lista': a})
                return salida


def get_human_names(text):
    tokens = nltk.tokenize.word_tokenize(text)
    pos = nltk.pos_tag(tokens)
    sentt = nltk.ne_chunk(pos, binary = False)
    person_list = []
    person = []
    name = ""
    for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
        for leaf in subtree.leaves():
            person.append(leaf[0])
        if len(person) > 1: #avoid grabbing lone surnames
            for part in person:
                name += part + ' '
            if name[:-1] not in person_list:
                person_list.append(name[:-1])
            name = ''
        person = []
    return person_list


class PersonasFisicasEndpoint(Resource):
    def post(self):  
            #Obtenemos la informacion necesaria
            request_json = request.get_json()   
            keyword = request_json.get('keyword')
            keywordparsed = unidecode.unidecode(keyword).strip().title()
            lista = request_json.get('listado')
            diccionario_consulta_db = {}         
            diccionario_salida = {}
            lista_salida = []
        
            #agregar la informacion a un diccionario
            diccionario_consulta_db = {}
            for a in range(len(lista)):
                keys = lista[a]["ConsolaSubId"]
                value = lista[a]["Source"]
                diccionario_consulta_db.update({keys:(value)})
                #ciclo a las diferentes alertas
           
            #iteramos el diccionario en busqueda de nombres           
            for x, y in diccionario_consulta_db.items():
                lista_de_id = []
                unaccented_string2 = unidecode.unidecode(y)  
                names = get_human_names(unaccented_string2)
                namesapolo = metodoSpacyFisicas(keyword,unaccented_string2)
                namesapolo2 = metodoSpacyFisicas(keyword,unaccented_string2.title())
                listado_extra = []
                for name in names: 
                    last_first =  HumanName(name).first + ' ' + HumanName(name).last
                    listado_extra.append(last_first)
                for name in namesapolo: 
                    listado_extra.append(name)
                for name2 in namesapolo2: 
                    listado_extra.append(name2)

                print(listado_extra)

                #procesamos la keyword
               
                trySplitKeywordparsed = keywordparsed.split(' ')
                print(keywordparsed)
                if(len(trySplitKeywordparsed) == 1):

                #este es un nombre,apellido simple
                    valorA = trySplitKeywordparsed[0]

                    #iteramos todos nombres encontrados en busqueda del substring dentro del texto
                    for test in listado_extra:                        
                        if search(valorA, test):
                            str_match1 = keywordparsed
                            nombres =  [str_match1]
                            if(nombres != None):
                                lista_de_id.append(nombres)
                    for iden in range(len(lista_de_id)):
                    #agregar la informacion a un listado
                        keys_salida = x
                        value_salida = lista_de_id[iden]
                        diccionario_salida.update({keys_salida:(value_salida)})
                        lista_salida.append(f"ID-{keys_salida} Nombre encontrado {value_salida} -> keyword {keywordparsed}")     

                      


                if(len(trySplitKeywordparsed) == 2):
                    #este es un nombre con apellido o dos nombres
                    #dividir uno y dos
                   
                    valorA = trySplitKeywordparsed[0]
                    valorB = trySplitKeywordparsed[1]

                    posibilidad1 = valorA+ " " +valorB
                    posibilidad2 = valorB+ " " +valorA

                    for test in listado_extra:                       
                        if search(posibilidad1, test):
                            str_match1 = posibilidad1
                            nombres =  [str_match1]
                            if(nombres != None):
                                lista_de_id.append(nombres)
                            
                        elif search(posibilidad2, test):
                            str_match2 = posibilidad2
                            nombres =  [str_match2]
                            if(nombres != None):
                                lista_de_id.append(nombres)
                    for iden in range(len(lista_de_id)):
                    #agregar la informacion a un listado
                        keys_salida = x
                        value_salida = lista_de_id[iden]
                        diccionario_salida.update({keys_salida:(value_salida)})
                        lista_salida.append(f"ID-{keys_salida} Nombre encontrado {value_salida} -> keyword {keywordparsed}")     

                
                if(len(trySplitKeywordparsed) == 3):
                    valorA = trySplitKeywordparsed[0]
                    valorB = trySplitKeywordparsed[1]
                    valorC = trySplitKeywordparsed[2]

                    posibilidad1 = valorA+ " " + valorB + " " + valorC
                    posibilidad2 = valorA+ " " + valorC + " " + valorB
                    posibilidad3 = valorC+ " " + valorA + " " + valorB
                    posibilidad4 = valorA+ " " + valorB 
                    posibilidad5 = valorB+ " " + valorC 

                    for test in listado_extra:                       
                        if search(posibilidad1, test):
                            str_match1 = posibilidad1
                            nombres =  [str_match1]
                            if(nombres != None):
                                lista_de_id.append(nombres)
                            
                        elif search(posibilidad2, test):
                            str_match2 = posibilidad2
                            nombres =  [str_match2]
                            if(nombres != None):
                                lista_de_id.append(nombres)
                        elif search(posibilidad3, test):
                            str_match2 = posibilidad3
                            nombres =  [str_match2]
                            if(nombres != None):
                                lista_de_id.append(nombres)
                        elif search(posibilidad4, test):
                            str_match2 = posibilidad4
                            nombres =  [str_match2]
                            if(nombres != None):
                                lista_de_id.append(nombres)
                        elif search(posibilidad5, test):
                            str_match2 = posibilidad5
                            nombres =  [str_match2]
                            if(nombres != None):
                                lista_de_id.append(nombres)
                    for iden in range(len(lista_de_id)):
                    #agregar la informacion a un listado
                        keys_salida = x
                        value_salida = lista_de_id[iden]
                        diccionario_salida.update({keys_salida:(value_salida)})
                        lista_salida.append(f"ID-{keys_salida} Nombre encontrado {value_salida} -> keyword {keywordparsed}")     


                    #salida = jsonify({ 'ConsolaSubId' : x  , 'Keyword': keywordparsed, 'Lista': nombres})
                if(len(trySplitKeywordparsed) == 4):
                #este es un nombre completo con dos nombres y dos apellidos
                    valorA = trySplitKeywordparsed[0]
                    valorB = trySplitKeywordparsed[1]
                    valorC = trySplitKeywordparsed[2]
                    valorD = trySplitKeywordparsed[3]

                    posibilidad1 = valorA+ " " +valorB + " " + valorC + " " + valorD
                    posibilidad2 = valorA+ " " +valorC + " " + valorB + " " + valorD
                    posibilidad3 = valorA+ " " +valorC + " " + valorD + " " + valorB
                    posibilidad4 = valorB+ " " +valorA + " " + valorC + " " + valorD
                    posibilidad5 = valorB+ " " +valorA + " " + valorD + " " + valorC
                    posibilidad6 = valorD+ " " +valorA + " " + valorB + " " + valorC

                    #DE LA TORRE MICHEL
                    #MICHEL DE LA TORRE
                    #3 0 1 2


                    for test in listado_extra:                       
                        if search(posibilidad1, test):
                            str_match1 = posibilidad1
                            nombres =  [str_match1]
                            if(nombres != None):
                                lista_de_id.append(nombres)
                            
                        elif search(posibilidad2, test):
                            str_match2 = posibilidad2
                            nombres =  [str_match2]
                            if(nombres != None):
                                lista_de_id.append(nombres)
                        elif search(posibilidad3, test):
                            str_match2 = posibilidad3
                            nombres =  [str_match2]
                            if(nombres != None):
                                lista_de_id.append(nombres)
                        elif search(posibilidad4, test):
                            str_match2 = posibilidad4
                            nombres =  [str_match2]
                            if(nombres != None):
                                lista_de_id.append(nombres)
                        elif search(posibilidad5, test):
                            str_match2 = posibilidad5
                            nombres =  [str_match2]
                            if(nombres != None):
                                lista_de_id.append(nombres)
                        elif search(posibilidad6, test):
                            str_match2 = posibilidad6
                            nombres =  [str_match2]
                            if(nombres != None):
                                lista_de_id.append(nombres)

                    

                    for iden in range(len(lista_de_id)):
                    #agregar la informacion a un listado
                        keys_salida = x
                        value_salida = lista_de_id[iden]
                        diccionario_salida.update({keys_salida:(value_salida)})
                        lista_salida.append(f"ID-{keys_salida} Nombre encontrado {value_salida} -> keyword {keywordparsed}")     


            salida = jsonify({'Keyword': keyword, 'Lista': lista_salida})
            return salida
            

api.add_resource(NLPVersionTwo, '/nlp/empresas')
api.add_resource(NLPPersonasFisicas, '/nlp/personas')
api.add_resource(PersonasFisicasEndpoint, '/nlp/personasFisicas')
# driver function


app.run(debug=False)


## si aparece entrenado por nosotros => 0-1 RESULTADO FINAL
## si spacy lo tienen como entidad nos muestre el de spacy => 0.52 
## resultado 0 
## modelo spacy 