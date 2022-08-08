### NER con Spacy Español

Este programa ya trae cargado un modelo previamente entrenado para poder consumir la busqueda de entidades PERSON y ORG , en español.

Para probarlo es necesario mandar keyword por parametro en algun cliente REST 

#### Ejemplo:

```json
{
    "keyword" : "foo" , 
    "listado" : [
        {
            "id": 1 , "source": "lorem ipsum"
        },
        {
            "id": 2 , "source": "lorem ipsum"
        }
    ]
}
```

#### Instalacion:
Instalar cada uno de los paquetes como son los siguientes:


```python 
pip install spacy
pip install flask
pip install numpy
```


- Desarrollado por Adolfo Huerta 