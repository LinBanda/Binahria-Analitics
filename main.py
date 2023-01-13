from twitter_scraper_selenium import get_profile_details
from twitter_scraper_selenium import scrape_keyword_with_api
from datetime import datetime
import plot_tools, text_tools
import json
import pathlib
import pandas as pd
import collections
import numpy as np
import nltk
from nltk.corpus import stopwords
nltk.download("stopwords")
from wordcloud import WordCloud 
stopwords = set(stopwords.words('spanish', 'english')) 
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from matplotlib import rcParams
stopwords.update([ "http", "https"])

# twitter_username = "LaloMedecigoMR"
# filename = "twitter_api_data"
# get_profile_details(twitter_username=twitter_username, filename=filename)
df = pd.read_csv('resultados_hashtags.csv', encoding="latin1")
mas_tuiteado = df["mas_tuiteado"].values.tolist()
mas_duradero = df["mas_duradero"].values.tolist()
lista_final = mas_tuiteado + mas_duradero
lista_final = ["#Reforma", "#reforma#PlanB"]

for tema in lista_final:
    query = tema
    tweets_count = 50
    output_filename = f"{query[1:]}"
    scrape_keyword_with_api(query=query, tweets_count=tweets_count, output_filename=output_filename)

    f = open(f'{output_filename}.json', encoding="latin1")
    try:
        data = json.load(f)
    except json.decoder.JSONDecodeError:
        continue
    f.close()
    now = datetime.now()
    fecha = now.strftime(f"%d_%m_%Y__%H_%M_%S")
    contentido_texto = ""
    for index in data:
        contentido_texto += data[index]["tweet_details"]["full_text"]

    resultados_palabras = text_tools.get_frecuency_key_words(contentido_texto)
    plot_tools.dict_to_csv(
        fecha, resultados_palabras, "./resultados/palabras_extraidas"
    )
    plot_tools.dict_to_csv(
        fecha, resultados_palabras, "./resultados/palabras_extraidas"
    )
    resultados_sentimientos = text_tools.get_sentiment_analyze(contentido_texto)
    plot_tools.dict_to_csv(
        fecha,
        resultados_sentimientos,
        "./resultados/sentimientos_extraidos",
    )
    resultados_sentimientos_detalle = text_tools.get_sentiment_detail(
        contentido_texto
    )
    plot_tools.dict_to_csv(
        fecha,
        resultados_sentimientos_detalle,
        "./resultados/sentimientos_extraidos_detalle",
    )
    resultados_flesch_Kincaid = text_tools.get_flesch_kincaid_test(contentido_texto)
    plot_tools.list_to_csv(
        fecha,
        resultados_flesch_Kincaid,
        "./resultados/resultados_flesch_Kincaid",
    )
    plot_tools.get_pie_chart(
        fecha, "./graficas/sentimentos_grafica", resultados_sentimientos
    )
    plot_tools.get_barh_chart(
        fecha, "./graficas/palabras_grafica", resultados_palabras
    )
    plot_tools.get_point_plot(
        fecha,
        "./graficas/flesch_kincaid_grafica",
        resultados_flesch_Kincaid,
    )
    # Reporte
    ruta = str(pathlib.Path(__file__).parent.absolute()).replace("\\", "/")
    data = {
        "fecha": fecha,
        "ruta": "./reportes",
        "titulo": query,
        "autor": "UNIDAD PLANEACIÓN Y P.",
        "imagenes": [
            f"file:///{ruta}/media/Flesch_Tabla.png",
            f"file:///{ruta}/graficas/flesch_kincaid_grafica_{fecha}.png",
            f"file:///{ruta}/graficas/palabras_grafica_{fecha}.png",
            f"file:///{ruta}/graficas/sentimentos_grafica_{fecha}.png",
            f"file:///{ruta}/media/footer.png",
        ],
        "textos_imagenes": [
            "En la prueba de facilidad de lectura de Flesch, las puntuaciones más altas indican material que es más fácil de leer; los números más bajos marcan pasajes que son más difíciles de leer",
            "Los resultados para está prueba se muestran cronológicamente como se presentaron los comentarios en la publicación.",
            "Se muestran la frecuencia de las 10 principales ideas obtenidas en el análisis de los comentarios",
            "Cada idea tiene una orientación emocional que pude ser; positiva, negativa o neutra dependiendo de la intención dentro de cada comentario, a continuación se muestra el porcentaje obtenida por cada catgoría",
        ],
        "textos": [
            f"Twitter",
            f"10",
        ],
    }
    plot_tools.get_report_pdf(data)
    wordcloud = WordCloud(stopwords=stopwords, background_color="white", max_words=1000).generate(contentido_texto)
    rcParams['figure.figsize'] = 10, 20
    plt.imshow(wordcloud)
    plt.axis("off")
    # plt.show()
    plt.savefig(f"{tema}_{fecha}.png", bbox_inches="tight")
    plt.close()