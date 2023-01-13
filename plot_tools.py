import csv

import pandas as pd
import pdfkit
from matplotlib import pyplot as plt
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

import text_tools


def dict_to_csv(fecha, dict, name):
    """
    Cambia el dictionario de datos a un archivo csv.

    Crea un archivo .csv nuevo con un nombre compuesto de el nombre
    proporcionado y la fecha del análisis. Dentro de este archivo,
    se va a llenar con los valores del diccionarios de datos que creo
    el bot para la publicación que analizó. También se va a registrar
    la frecuencia en la que aparecen estas palabras/frases.

    Parámetros
    ----------
    fecha : str
        Fecha en la que se realizo el análisis.
    dict : str
        El diccionario de datos que genero el bot.
    name : str
        El nombre del archivo.
    
    Retorna
    -------
    str
        Aviso de que se genero el archivo.
    
    Véase También
    -------------
    open : Abre un archivo especifico.
    csv.DictWriter : Crea un objeto que asigna los diccionarios a las filas de salida}
        del archivo .csv .
    csv.DictWriter.writeheader : Escribe la cabecera de una fila (indice).
    csv.DictWriter.writerow : Escribe el contenido de una fila.
    """
    with open(f"{name}_{fecha}.csv", "w", newline="", encoding="utf8") as csvfile:
        header_key = ["Valor", "Frecuencia"]
        new_val = csv.DictWriter(csvfile, fieldnames=header_key)
        new_val.writeheader()
        for new_k in dict:
            new_val.writerow({"Valor": new_k, "Frecuencia": dict[new_k]})
    return f"Archivo {name} generado"
    
def list_to_csv(fecha, data_list, name):
    fields = ["value"]
    rows = [data_list]
    with open(f"{name}_{fecha}.csv", "w", encoding="utf8") as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(rows)
    return f"{fecha}: Archivo {name} generado"

def get_pie_chart(fecha, name, dict):
    """
    Traza una gráfica de pastel.

    La gráfica de pastel emplea los datos que recopiló el bot para
    poder representar dicha información de forma visual, y así, sea
    fácil de interpretar.

    Parámetros
    ----------
    fecha : str
        Fecha en la que se realizo el análisis.
    name : str
        El nombre del archivo.
    dict : str
        El diccionario de datos que genero el bot.
    
    Retorna
    -------
    str
        Aviso de que el archivo ha sido generado.
    
    Véase También
    -------------
    plt.pie : Traza una gráfica de pastel.
    plt.axis : Configura los ejes de la gráfica.
    plt.savefig : Guarda la gráfica como una imagen.
    plt.close : Cierra la ventana que muestra la gráfica.
    """
    colors = ["#969899", "#767473", "#DCC8A6"]
    plt.pie(dict.values(), labels=dict.keys(), autopct="%0.1f %%", colors=colors)
    plt.axis("equal")
    # plt.title('Percentage by value')
    plt.savefig(f"{name}_{fecha}.png", bbox_inches="tight")
    plt.close()
    return f"Archivo {name} generado"


def get_barh_chart(fecha, name, dict):
    """
    Traza una gráfica de barras horizontales.

    La gráfica de barras emplea los datos que recopiló el bot para
    poder representar dicha información de forma visual, y así, sea
    fácil de interpretar.

    Parámetros
    ----------
    fecha : str
        Fecha en la que se realizo el análisis.
    name : str
        El nombre del archivo.
    dict : str
        El diccionario de datos que genero el bot.
    
    Retorna
    -------
    str
        Aviso de que el archivo ha sido generado.
    
    Véase También
    -------------
    list : Lista de elementos.
    plt.barh : Traza una gráfica de barras horizontales.
    plt.ylabel : Establece la etiqueta del eje y.
    plt.xlabel : Establece la etiqueta del eje x.
    plt.savefig : Guarda la gráfica como una imagen.
    plt.close : Cierra la ventana que muestra la gráfica.
    """
    dict_values = list(dict.values())[:10]
    dict_labels = list(dict.keys())[:10]
    eje_x = dict_labels
    eje_y = dict_values
    plt.barh(eje_x, eje_y, color="#265B4E")
    plt.ylabel("Values")
    plt.xlabel("Frequency")
    # plt.title('Frequency x Values')
    plt.savefig(f"{name}_{fecha}.png", bbox_inches="tight")
    plt.close()
    return f"Archivo {name} generado"


def get_point_plot(fecha, name, data_list):
    """
    Traza una gráfica de puntos.

    La gráfica de puntos emplea los datos que recopiló el bot para
    poder representar dicha información de forma visual, y así, sea
    fácil de interpretar.

    Parámetros
    ----------
    fecha : str
        Fecha en la que se realizo el análisis.
    name : str
        El nombre del archivo.
    data_list : str
        Lista de datos Flesch Kincaid.
    
    Retorna
    -------
    str
        Aviso de que el archivo ha sido generado.
    
    Véase También
    -------------
    list : Lista de elementos.
    plt.plot : Trazar y versus x como líneas y/o marcadores.
    plt.ylabel : Establece la etiqueta del eje y.
    plt.xlabel : Establece la etiqueta del eje x.
    plt.savefig : Guarda la gráfica como una imagen.
    plt.close : Cierra la ventana que muestra la gráfica.
    """
    data_order = list(range(1, (len(data_list) + 1)))
    plt.plot(data_order, data_list, ":", color="b")
    plt.ylabel("Flesch Kincaid")
    plt.xlabel("History")
    # plt.title('Flesch Kincaid Historical')
    plt.savefig(f"{name}_{fecha}.png", bbox_inches="tight")
    plt.close()
    return f"Archivo {name} generado"


def read_csv(name):
    """
    Lee un archivo .csv y crea un marco de datos.

    El usuario da el nombre del archivo .csv que desea que esta función
    lea. A partir de dicho archivo, crea un marco de datos.

    Parámetros
    ----------
    name : str
        Nombre del archivo.
    
    Retorna
    -------
    DataFrame
        Marco de datos del archivo que se leyo.
    
    Véase También
    -------------
    pandas.read_csv : Leer un archivo .csv en DataFrame.
    """
    df = pd.read_csv(name, encoding="utf8")
    return df


def get_report_pdf(dict):
    """
    Crea el reporte del analisis en un archivo PDF.

    Utiliza lenguaje HTML para diseñar el archivo PDF. Los datos que se muestran
    en el archivo PDF son los que se obtuvieron del análisis de los post de
    Facebook.

    Parámetros
    ----------
    dict : str
        Diccionario de datos.
    
    Véase También
    -------------
    pdfkit.from_string : Crea un archivo PDF a partir de un ``string``.
    """
    kitoptions = {
        "enable-local-file-access": None,
        "margin-left": "0mm",
        "margin-right": "0mm",
        "margin-bottom": "0mm",
        "margin-top": "0mm",
    }

    pdfkit.from_string(
        f"""
<!doctype html>
<html lang="es">
    <title></title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    """
        + """<style>
        @import url('http://fonts.cdnfonts.com/css/montserrat');
        *{
            font-family: 'Montserrat', sans-serif;
            margin-left: 10px;
            margin-right: 10px;
        }
        body {
            background-repeat: no-repeat !important;
            background: -webkit-linear-gradient(top, rgba(245,240,231,1) 0%, rgba(255,255,255,1) 100%);
        }
        td {
            padding: 15px;
        }
        table td, table td * {
            vertical-align: top;

        }
        .table-info-general {
            border: 1px solid white;
            border-collapse: collapse;
            font-size: 24px !important;
       }
       .table-info-general-color{
            background-repeat: no-repeat !important;
            background: -webkit-linear-gradient(left, rgba(188,149,92,0.5) 0%, rgba(188,149,92,0.65) 30%, rgba(237,223,204,1) 100%);       }
        }
        .table-resultados {
            border: 0px !important;
        }
        .title {
            text-align: center;
            font-size: 60px;
            color: #767473;
            margin-top: 0px;
        }
        .table-fist-column {
            background-color: #9D2445;
            color: #fff;
            text-align: right;
        }
        .table-url {
            width: 1000px;
            word-wrap:break-word;
            display:inline-block;
        }
        .margin-top-color {
            background-color: #B89259;
            height: 2px;
        }
        p{
            font-size: 22px;
            text-align: justify;
        }
        h3{
            font-size: 32px;
            color: #852133;
        }
        h2 {
            color: #969899;
            font-weight: lighter;
            padding-top: 30px;
            margin-bottom: 0px;
        }
        hr {
            background-color: #B89259;
        }
        .img-footer, .footer {
            margin: 0px !important;
            width: 100%;
            height: 100px;
        }
    </style>"""
        + f"""</head>
    <body>
        <h2>Unidad de Planeación y Prospectiva</h2>
        <h1 class="title">Análisis de percepción ciudadana en redes</h1>
        <table width="100%" class="table-info-general">
            <tr>
                <td colspan="2" class="margin-top-color">
                </td>
            </tr>
            <tr class="table-info-general">
                <td class="table-info-general table-fist-column">Nombre publicación:</td>
                <td class="table-info-general table-info-general-color">{dict['titulo']}</td>
            </tr>
            <tr class="table-info-general">
                <td class="table-info-general table-fist-column">URL:</td>
                <td class="table-info-general table-info-general-color">
                    <span class="table-url">
                        {dict['textos'][0]}
                    </span>
                </td>
            </tr>
            <tr class="table-info-general">
                <td class="table-info-general table-fist-column">Comentarios:</td>
                <td class="table-info-general table-info-general-color">{dict['textos'][1]}</td>
            </tr>
        </table>
        <h3>Interpretación</h3>
        <hr/>
        <table class="table-resultados">
            <tr>
                <td width="50%">
                    <p>
                        {dict['textos_imagenes'][0]}
                    </p>
                    <div align="center" class="imgplot">
                        <img class="rounded" src="{dict['imagenes'][0]}">
                    </div>
                </td>
                <td width="50%">
                    <p>
                        {dict['textos_imagenes'][1]}
                    </p>
                    <div align="center" class="imgplot">
                        <img class="rounded" src="{dict['imagenes'][1]}">
                    </div>
                </td>
            </tr>
            <tr>
                <td width="50%">
                    <h3>Frecuencia de palabras clave</h3>
                    <hr/>
                    <p>
                        {dict['textos_imagenes'][2]}
                    </p>
                    <div align="center" class="imgplot">
                        <img class="rounded" src="{dict['imagenes'][2]}">
                    </div>
                </td>
                <td width="50%">
                    <h3>Análisis de sentimientos</h3>
                    <hr/>
                    <p>
                        {dict['textos_imagenes'][3]}
                    </p>
                    <div align="center" class="imgplot">
                        <img class="rounded" src="{dict['imagenes'][3]}">
                    </div>
                </td>
            </tr>
        </table>
        <div align="center" class="footer">
            
        </div>
    </body>
</html>
""",
        f"{dict['ruta']}/{text_tools.clear_alphanumeric_text(dict['autor'])}_{dict['fecha']}.pdf",
        verbose=True,
        options=kitoptions,
    )


def make_report(dict):
    """
    Ingresa la información del análisis al archivo PDF.

    Agrega la información del análisis de los post de Facebook al archivo PDF
    que se creo en la función ``def get_report_pdf``.

    Parámetros
    ----------
    dict : str
        Diccionario de datos.
    Retorna
    -------
    str
        Aviso de que el reporte ha sido generado.
    """
    fileName = f"{dict['ruta']}/{dict['titulo']}_{dict['fecha']}.pdf"
    documentTitle = dict["titulo"]
    title = dict["titulo"]
    subTitle = f"Por {dict['autor']}"
    images = dict["imagenes"]
    images_text = dict["textos_imagenes"]
    textLines = dict["textos"]
    pdf = canvas.Canvas(fileName)
    pdf.setTitle(documentTitle)
    pdfmetrics.registerFont(TTFont("abc", "./bin/SakBunderan.ttf"))
    pdf.setFont("abc", 36)
    pdf.drawCentredString(300, 770, title)
    pdf.setFillColorRGB(0, 0, 255)
    pdf.setFont("Courier-Bold", 24)
    pdf.drawCentredString(290, 720, subTitle)
    pdf.line(30, 710, 550, 710)
    text = pdf.beginText(40, 680)
    text.setFont("Courier", 10)
    text.setFillColor(colors.red)
    for line in textLines:
        text.textLine(line)
    text_images = pdf.beginText(40, 420)
    text_images.setFont("Courier", 6)
    text_images.setFillColor(colors.black)
    y_image = 600
    y_text = 750
    pdf.drawInlineImage(images[0], 170, 350, width=250, height=200)
    for line in images_text[0]:
        text.textLine(line)
    pdf.drawText(text)
    pdf.showPage()
    for count, image in enumerate(images):
        if count != 0:
            pdf.drawInlineImage(image, 170, y_image, width=250, height=200)
            text_images = pdf.beginText(40, y_image + 220)
            for line in images_text[count]:
                text_images.textLine(line)
            pdf.drawText(text_images)
            y_text -= 250
            y_image -= 230
    pdf.save()
    return f"Reporte de {title} generado"
