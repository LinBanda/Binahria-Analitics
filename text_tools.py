import operator
import pytextrank
import spacy
import textstat
from hermetrics.levenshtein import Levenshtein
from pysentimiento import create_analyzer


def get_frecuency_key_words(text):
    """
    Obtiene la frecuencia de palabras clave.

    Emplea el procesamiento de lenguaje natural para determinar las
    palabras claves del post a analizar. Ya que se determinan las
    palabras claves, se determina la frecuencia en la que aparecen.
    Si dos palabras claves tienen un significado o conotación similar,
    se considera como el mismo y con ello aumenta el contador de
    frecuencia.

    Parámetros
    ----------
    text : str
        El texto a analizar.
    
    Retorna
    -------
    dict
        Diccionario de datos con la información recopilada.
    
    Véase También
    -------------
    spacy.load : Carga un modelo de procesamiento de lenguaje natural (NLP)
    string.split : Separa un string en varios segmentos por medio de un token.
    string.replace : Reemplaza un token por otro.
    string.strip : Eliminar los espacios al principio y al final del string.
    len : Retorna el número de elementos de un objeto o lista.
    list.append : Agrega un elemento al final de una lista
    dict.keys : Visualiza las claves contenidos en el diccionario de datos.
    Levenshtein.similarity : Evalua la similitud de dos palabras.
    """
    lev = Levenshtein()
    nlp = spacy.load("es_core_news_md")
    nlp.add_pipe("textrank")
    keywors_found = {}
    sentences = []
    words = []
    sentences = text.split("\n")
    sentences = [line.replace("\n", "") for line in sentences if line.strip()]
    for sentence in sentences:
        doc = nlp(sentence)
        for keyword in doc._.phrases[:1]:
            # doc.noun_chunks:
            keyword = keyword.text
            if len(keyword) > 1:
                # if len(keyword) > 4:
                #     keyword = str(keyword[:4]) + " ..."
                words.append(str(clear_alphanumeric_text(keyword)))
    for word in words:
        if word not in keywors_found:
            keywors_found[word] = 0
    for sentence in sentences:
        for k_word in keywors_found.keys():
            if k_word in sentence:
                keywors_found[k_word] += 1
    for k_word in list(keywors_found):
        for another_k_word in keywors_found.keys():
            if k_word != another_k_word:
                if lev.similarity(k_word, another_k_word) > 0.5:
                    keywors_found[another_k_word] += 1
                    del keywors_found[k_word]
                    break
    keywors_found_sort = dict(
        sorted(keywors_found.items(), key=operator.itemgetter(1), reverse=True)
    )
    return keywors_found_sort


def get_sentiment_analyze(text):
    """
    Realiza el análisis de sentimientos de un texto.

    Categoriza los sentimientos en 3 tipos: positivo, negativo y neutral.
    Lleva la cuenta de las frases que emulan cualquiera de los 3 tipos
    de sentimientos para su posterior graficación.

    Parámetros
    ----------
    text : str
        El texto a analizar.
    
    Retorna
    -------
    dict
        Diccionario de datos con la información recopilada.
    
    Véase También
    -------------
    string.split : Separa un string en varios segmentos por medio de un token.
    string.replace : Reemplaza un token por otro.
    string.strip : Eliminar los espacios al principio y al final del string.
    pysentimiento.create_analyzer : Crea un analizador para una tarea en específico.
    pysentimiento.predict : Predice el sentimiento que emula la frase analizada.
    """
    counter_sentiments = {"Positive": 0, "Negative": 0, "Neutral": 0}
    sentences = text.split("\n")
    sentences = [line.replace("\n", "") for line in sentences if line.strip()]
    analyzer = create_analyzer(task="sentiment", lang="es")
    for sentence in sentences:
        result_sentiment = analyzer.predict(sentence).output
        if result_sentiment == "NEG":
            counter_sentiments["Negative"] += 1
        elif result_sentiment == "POS":
            counter_sentiments["Positive"] += 1
        elif result_sentiment == "NEU":
            counter_sentiments["Neutral"] += 1
    return counter_sentiments


def get_flesch_kincaid_test(text):
    """
    Realiza la prueba Flesch Kincaid.

    Analiza el texto dado para saber el nivel de legibilidad que posee,
    es decir, la facilidad que se tiene para entender el mensaje que quiere
    transmitir.

    Parámetros
    ----------
    text : str
        El texto a analizar.
    
    Retorna
    -------
    list
        Conjunto de frases y su legibilidad.
    
    Véase También
    -------------
    textstat.set_lang : Establece el idioma de las frases a analizar.
    string.split : Separa un string en varios segmentos por medio de un token.
    string.replace : Reemplaza un token por otro.
    string.strip : Eliminar los espacios al principio y al final del string.
    textstat.flesch_reading_ease : Analiza la legibilidad de una frase.
    """
    textstat.set_lang("es")
    result_list = []
    sentences = text.split("\n")
    sentences = [line.replace("\n", "") for line in sentences if line.strip()]
    result_list = [textstat.flesch_reading_ease(sentence) for sentence in sentences]
    return result_list


def get_sentiment_detail(text):
    """
    Obtiene información más detallada de los sentimientos que emula un texto.

    Separa las oraciones de un texto por el sentimiento que más transmite.

    Parámetros
    ----------
    text : str
        El texto a analizar.
    
    Retorna
    -------
    dict
        Diccionario de datos con la información recopilada.
    
    Véase También
    -------------
    string.split : Separa un string en varios segmentos por medio de un token.
    string.replace : Reemplaza un token por otro.
    string.strip : Eliminar los espacios al principio y al final del string.
    pysentimiento.create_analyzer : Crea un analizador para una tarea en específico.
    pysentimiento.predict : Predice el sentimiento que emula la frase analizada.
    """
    counter_sentiments = {}
    sentences = text.split("\n")
    sentences = [line.replace("\n", "") for line in sentences if line.strip()]
    analyzer = create_analyzer(task="sentiment", lang="es")
    for sentence in sentences:
        result_sentiment = analyzer.predict(sentence).output
        if result_sentiment == "NEG":
            counter_sentiments[sentence] = "NEG"
        elif result_sentiment == "POS":
            counter_sentiments[sentence] = "POS"
        elif result_sentiment == "NEU":
            counter_sentiments[sentence] = "NEU"
    return counter_sentiments


def clear_alphanumeric_text(text):
    """
    Elimina carácteres que no son alfanuméricos.

    Depura el texto a analizar al borrar los carácteres que no son
    alfanuméricos dentro del mismo.

    Parámetros
    ----------
    text : str
        El texto a depurar.
    
    Retorna
    -------
    str
        El texto depurado.
    
    Véase También
    -------------
    string.replace : Reemplaza un token por otro.
    """
    items_to_delete = [
        '"',
        "+",
        "-",
        "!",
        "¡",
        "/",
        "&",
        "%",
        "#",
        "}",
        "{",
        "_",
        "-",
        "*",
    ]
    new_text = text
    for item in items_to_delete:
        str(new_text).replace(item, "")
    return new_text


def delete_keys_from_dict(list_keys, dict):
    """
    Borra claves especificas del diccionario de datos.

    Elimina claves del diccionario de datos que no son necesarios.

    Parámetros
    ----------
    list_keys : list
        Lista de claves a borrar del diccionario de datos.
    dict : dict
        El diccionario de datos a depurar.
    
    Retorna
    -------
    dict 
        Diccionario de datos depurado.
    
    Véase También
    -------------
    dict.keys : Visualiza las claves contenidos en el diccionario de datos.
    """
    for item_key in list_keys:
        if item_key in dict.keys():
            del dict[item_key]
    return dict
