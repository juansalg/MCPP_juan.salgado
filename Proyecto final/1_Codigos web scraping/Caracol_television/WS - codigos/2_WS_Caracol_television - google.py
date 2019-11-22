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

# 'for' para cambiar el año, desde 'inicio' a 'fin',
# y buscar en 'pag_buscar' paginas de resultados de google

inicio = 2010
fin = 2013
num_art = 5
count = 0
start_time = time.time()


# Define parameters for google search
my_api_key1 = 'AIzaSyCzaKFRVms75E0BxXDkWpgdQxua4EHXfFY'
my_api_key2 = 'AIzaSyD1H0oxSEgPuIFSBqkcjd4g4COqrbe1w04'
my_api_key3 = 'AIzaSyBtuwqLlac_IsoTRaZWw5uwpn9r6WzAAAs'
my_api_key4 = 'AIzaSyCyw7j6z1V53hanAloj49estCif_rJ0U10'

my_api_key5 = 'AIzaSyCucU97qP-cO-aZPL9JGevtki2oxEWTnHE'
my_api_key6 = 'AIzaSyAqJB9r1fCqjqAKG0obR6rKBeNmMV-mQog'
my_api_key7 = 'AIzaSyCjBMlUijHQ-3VD7Dh9VcuriLxTLww8z-I'

keys = [my_api_key5, my_api_key6, my_api_key7]


my_cse_id = "008462511346546009877:r03t75mpi2m"

# Define function *standard* to search google results in the cse
def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

def get_link(results): 
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
count_req_key = 0
key_index = 0

# Use first key
my_api_key = keys[key_index]


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
            
            # Change keys so that limit is not touched
            count_req_key = count_req_key + 1
            if count_req_key > 45 and key_index == 0:
                key_index = key_index + 1
                count_req_key = 0
            elif count_req_key > 90:
                key_index = key_index + 1
                count_req_key = 0
            
            results = google_search(a_buscar, my_api_key, my_cse_id, num = num_art)
            
            # Llenar vector con links buscados
            urls_buscados = []
            get_link(results)

            
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
                link = get(url  )
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
                    titulo = linksoup.find('div', attrs = {'class':'titulo'})
                    title = titulo.h1.text
                except:
                    title = '**Especial**'
                    
                # Extraccion de la fecha 
                try:
                    fecha = linksoup.find('div', attrs = {'class': 'tiempo'})
                    fecha = fecha.text
                    date = re.search("(.*)[0-9] ", fecha).group()
                except:
                    date = '**Especial**'
                    
                # Extracción del texto del articulo
                try: 
                    articulo_total = linksoup.find('div', attrs = {'class':'texto-central'})
                    # Para los textos que estan divididos con 'div'
                    articulo_txt = articulo_total.find_all('div')
                    texto1 = ''
                    for i in range(len(articulo_txt)):
                        texto1 = texto1 + " " + articulo_txt[i].getText()
                        
                    # Para los textos que estan divididos con 'div'    
                    articulo_txt = articulo_total.find_all('p')
                    texto2 = ''
                    for i in range(len(articulo_txt)):
                        texto2 = texto2 + " " + articulo_txt[i].getText()
                    
                    # Escoger el texto mas largo
                    if len(texto2) > len(texto1):
                        texto = texto2[:]
                    elif len(texto1) > len(texto2):
                        texto = texto1[:]
                    else:
                        texto = '**Textos iguales**'
                        
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
            a_buscar2 = 'site:noticias.canalrcn.com ' + a_buscar
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
test_df_tot.to_excel("RCN_tv_articulos_prueba.xlsx")
errores.to_excel("RCN_tv_errores_prueba.xlsx")
vacios.to_excel("RCN_tv_vacios_prueba.xlsx")


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
message = """Subject: Finalizo WS de RCN television


Tiempo total: """ + str(round(elapsed_time/60, 3)) + "min" \
\
"""\n\nTotal articulos: """ + str(len(links_tot)) + \
\
"""\n\nTotal errores: """ + str(len(errores))

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)

