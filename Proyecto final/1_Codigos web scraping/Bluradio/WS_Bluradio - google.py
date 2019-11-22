# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 20:00:34 2019

@author: JCSR
"""

# from googlesearch import search
# conda install git


# pip install git+https://github.com/abenassi/Google-Search-API
# import os
# os.chdir("D:/juanca/Anaconda_dir/google/Google-Search-API-master")
# from google import google
# pip install --upgrade google-api-python-client
from requests import get
from bs4 import BeautifulSoup as soup
# import requests
import pandas as pd
import time
import re
from IPython.core.display import clear_output
from random import randint
from googleapiclient.discovery import build
import smtplib, ssl


print("\nWeb scraping - Bluradio\n")

inicio = 2010
fin = 2018
num_art = 10
count = 0
start_time = time.time()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0)\
 Gecko/20100101 Firefox/69.0'}


# Define parameters for google search
# Use this sets of keys: Max 836 queries (76 * 11)
my_api_key1 = 'AIzaSyCzaKFRVms75E0BxXDkWpgdQxua4EHXfFY'
my_api_key2 = 'AIzaSyD1H0oxSEgPuIFSBqkcjd4g4COqrbe1w04'
my_api_key3 = 'AIzaSyBtuwqLlac_IsoTRaZWw5uwpn9r6WzAAAs'
my_api_key4 = 'AIzaSyCyw7j6z1V53hanAloj49estCif_rJ0U10'
my_api_key5 = 'AIzaSyCucU97qP-cO-aZPL9JGevtki2oxEWTnHE'
my_api_key6 = 'AIzaSyAqJB9r1fCqjqAKG0obR6rKBeNmMV-mQog'
my_api_key7 = 'AIzaSyCjBMlUijHQ-3VD7Dh9VcuriLxTLww8z-I'
my_api_key8 = 'AIzaSyCdtwgGtft_kPwIe20cr_MLbQc6noSIYc8'
my_api_key9 = 'AIzaSyA7v3oRgCsVtsxS4-tpVv4N-A88B743NPY'
my_api_key10 = 'AIzaSyBUraDUJaV3w5d3dXEdElj5jNFShYJj_Bs'
my_api_key11 = 'AIzaSyDArzuCsT-ibo0WsBlRsq7wejXTKivb_sg'

keys = [my_api_key1, my_api_key2, my_api_key3, my_api_key4, my_api_key5, my_api_key6,
        my_api_key7, my_api_key8, my_api_key9, my_api_key10, my_api_key11]

# Count for number of times the key is used
count_keys = [0 for x in range(len(keys))]

# Define key_index as list: to modify it in a function
key_index = [0]


my_cse_id = "008462511346546009877:elv6ulxknj1"

# Define function *standard* to search google results in the cse
def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

def get_results(a_buscar, my_cse_id, results, key_index, keys, count_keys):
    try:
        pages = [x for x in range(11, 71, 10)]
        my_api_key = keys[key_index[0]]
        result_temp = google_search(a_buscar, my_api_key, my_cse_id, num = num_art)
        count_keys[key_index[0]] = count_keys[key_index[0]] + 1
        # 76 is the max requests per key (google limit is 100)
        # (76 because the condition '> 75' is true if 76)
        if count_keys[key_index[0]] > 75:
            key_index[0] = key_index[0] + 1
            if key_index[0] > len(keys) - 1:
                print("Se usaron todas las llaves. Error.")
        results.extend(result_temp)
        for i in pages:
            result_temp = google_search(a_buscar, my_api_key, my_cse_id, 
                                        num = num_art, start = i)
            count_keys[key_index[0]] = count_keys[key_index[0]] + 1
            if count_keys[key_index[0]] > 75:
                key_index[0] = key_index[0] + 1
                if key_index[0] > len(keys) - 1:
                    print("Se usaron todas las llaves. Error.")
            results.extend(result_temp)
    except:
        print('No encontro mas articulos')

def get_link(results, urls_buscados): 
    for i in range(len(results)):
        urls_buscados.append(results[i]['link'])



palabras = ['Seguridad bogotá','Homicidio bogotá','Hurto bogotá','Seguridad ciudadana bogotá',
            'Orden público bogotá','Violencia bogotá','Asesinato bogotá','Matar bogotá',
            'Robo bogotá','Atraco bogotá','Fleteo bogotá','Orden público bogotá',
            'Disturbio bogotá','Riña bogotá','Abuso sexual bogotá','Acoso sexual bogotá',
            'Acoso infantil bogotá','Golpiza bogotá','Linchamiento bogotá',
            'Policía Nacional bogotá','Dar de baja bogotá',
            'Violencia sexual bogotá', 'Lesiones personales bogotá',
            'Vandalismo bogotá',
            'Policía de Bogotá','Inseguridad bogotá','Percepción de seguridad bogotá',
            'Percepción de inseguridad bogotá']



# Creacion de vectores para llenar con la informacion del scraping
titles_tot = []
links_tot  = []
contents_tot  = []
dates_tot  = []
urls_tot  = []
pal_buscada_tot  = []
loop_anio_tot = []
pal_err = []
year_err = []
link_err = []
anios_vacios = []
pal_vacias = []


start_time = time.time()
requests = 0
count = 0


# loop para iterar por distintas palabtas
for pal in palabras:
    
    # loop para buscar 'pal' dentro de los años 'inicio' y 'fin'
    for year in range(inicio, fin+1):
        
        try:
        
            # Se crean los vectores acá porque cada anio la búsqueda de urls cambia
            titles = []
            links = []
            contents = []
            dates = []
            urls = []
            pal_buscada = []
            loop_anio = []
            
            a_buscar = pal + " before:" + str(year) + \
            "-12-31 after:" + str(year) + "-1-01"
            
            results = []
            get_results(a_buscar, my_cse_id, results, key_index, keys, count_keys)
            
            # Llenar vector con links buscados
            urls_buscados = []
            get_link(results, urls_buscados)

            
            # Continuar el loop si no se encontraron resultados para esta
            # 'pal' y 'year'. Guardar esos resultados
            if not urls_buscados:
                pal_vacias.append(pal)
                anios_vacios.append(year)
                continue
                
            for url in urls_buscados:
                # 'if' para eliminar duplicados respecto al url
                if url in urls_tot:
                    continue
                urls.append(url)
                urls_tot.append(url)
            
            print('Total urls: ', len(urls), 'Año: ', year, 'Pal:', pal)
            print('')
            requests = 0
            
            
            for url in urls:                
                
                # Extraccion del codigo html de cada url
                link = ''
                link = get("https://www.bluradio.com/bogota/estos-hechos-no-pueden-quedar-impunes-distrito-sobre-golpiza-alejandro-vargas-66252", headers = headers)
                linksoup = soup(link.content,'html5lib')
                time.sleep(randint(2,4))
                requests += 1
                elapsed_time_1 = time.time() - start_time
                print('Articulo: {} de {}; Pal: {}; Total time: {} min'.format(requests, year, pal, 
                      round(elapsed_time_1/60, 3)))
                print("")
                clear_output(wait = True) 
                print(url)
                print("")
                count += 1
                print('Total articulos', count)
                print("")
                
                # Extraccion del titulo
                try:    
                    titulo = linksoup.find('h1', attrs = {'class':'titulo ng-binding ng-scope'})
                    for tit in titulo:
                        title = tit.text
                except:
                    title = '**Especial**'
                    
                # Extraccion de fecha
                # Se hace de dos formas: 'try': la extrae desde el link; 'except' 
                # desde el articulo mismo
                try:
                    try:
                        date = re.search("[0-9]+/[0-9]+/[0-9]+", url).group(0)
                        
                    except:
                        fecha = linksoup.find_all('time')
                        # Este 'if': Hay pags que tienen varias categorias 'time'. Segun el caso, se 
                        # extrae la fecha
                        # de dos formas. De lo contrario, se llena con '**Especial**'
                        if len(fecha) == 1:
                            for fe in fecha:
                                date = fe.text
                            # 'if' porque hay fechas que no están registradas
                            if 'none' in date:
                                date = '**Especial**'
                            else:
                                # Extrayendo la fecha correcta [sin la hora]
                                date = re.search("[0-9]+/[0-9]+/[0-9]+", date).group()
                except:
                    date = '**Especial**'
                    """
                    else:
                        date = fecha[0].getText()
                        if 'none' in date:
                            date = '**Especial**'
                        else:
                            date = re.search("\n(.*),", date).group(1)
                            """
                    
                # Extracción del texto del articulo
                try:
                    articulo_total = linksoup.find('div', attrs = {'class':'cuerpo'})
                    articulo_txt = articulo_total.find_all('p')
                    texto = ''
                    for i in range(len(articulo_txt)):
                        texto = texto + " " + articulo_txt[i].getText()
                except:
                    texto = '**Especial**'
                    
                    
                # Llenar vectores de variables
                
                titles.append(title)
                dates.append(date)
                contents.append(texto)
                links.append(url)
                pal_buscada.append(pal)
                loop_anio .append(year)
                test_df=pd.DataFrame({'Titulo':titles,
                              'Fecha':dates,
                              'Contenido':contents,
                              'Link':links,
                              'Palabra buscada':pal_buscada,
                              'Año buscado':loop_anio})
        except:
            titles = []
            links = []
            contents = []
            dates = []
            urls = []
            pal_buscada = []
            loop_anio = []
            pal_err.append(pal)
            year_err.append(year)
            a_buscar2 = 'site:caracol.com.co ' + a_buscar
            link_err.append(a_buscar2)
            print('\nError en el loop')

        ## Dataframe con toda la informacion
        titles_tot.extend(titles)
        dates_tot.extend(dates)
        contents_tot.extend(contents)
        links_tot.extend(links)
        pal_buscada_tot.extend(pal_buscada)
        loop_anio_tot.extend(loop_anio)
        test_df_tot=pd.DataFrame({'Titulo':titles_tot,
                      'Fecha':dates_tot,
                      'Contenido':contents_tot,
                      'Link':links_tot,
                      'Palabra buscada':pal_buscada_tot,
                      'Año buscado':loop_anio_tot})
    
        ## Dataframe de los errores
        errores = pd.DataFrame(
                {'Palabra no recopilada':pal_err,
                 'Anio no recopilado':year_err,
                 'Link buscado':link_err}
                )
        
        ## Dataframe con palabras y anios vacios
        vacios = pd.DataFrame(
                {'Palabra sin resultados':pal_vacias,
                 'Anio sin resultados':anios_vacios}
                )
        

# Guardar una base para todas las palabras        
test_df_tot.to_excel("Caracol_radio_articulos_total.xlsx")
errores.to_excel("Caracol_radio_errores_total.xlsx")
vacios.to_excel("Caracol_radio_vacios_total.xlsx")


elapsed_time = time.time() - start_time


print('\nTotal articulos: {} \nNumero de años: {} \nArticulos por año: {} \nTotal time: {} min'
      .format(len(links_tot),
              fin + 1 - inicio,
              round(len(links_tot)/(fin + 1 - inicio), 3),
              round(elapsed_time/60, 3)))

## Enviar correo
port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "python.development.cerac@gmail.com"  # Enter your address
receiver_email = "srjc211@gmail.com"  # Enter receiver address
password = 'Cerac_2019'
message = """Subject: Finalizo WS de Caracol radio


Tiempo total: """ + str(round(elapsed_time/60, 3)) + "min" \
\
"""\n\nTotal articulos: """ + str(len(links_tot)) + \
\
"""\n\nTotal errores: """ + str(len(errores))

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)

