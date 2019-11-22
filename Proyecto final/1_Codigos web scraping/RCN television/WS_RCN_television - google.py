# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 20:00:34 2019

@author: JCSR
"""


# pip install git+https://github.com/abenassi/Google-Search-API
# from googlesearch import search
from google import google
from requests import get
from bs4 import BeautifulSoup as soup
# import requests
import pandas as pd
import time
import re
from IPython.core.display import clear_output
from random import randint
import smtplib, ssl

# 'for' para cambiar el año, desde 'inicio' a 'fin',
# y buscar en 'pag_buscar' paginas de resultados de google

inicio = 2010
fin = 2018
pag_buscar = 7
count = 0
start_time = time.time()


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
            
            a_buscar = "site:noticias.canalrcn.com " + pal + " before:" + str(year) + \
            "-12-31 after:" + str(year) + "-1-01"
            
            
            search_results = google.search(a_buscar, pag_buscar)
            
            urls_buscados = []
            
            for result in search_results:
                urls_buscados.append(result.link)
            
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
                 'Anio no recopilado':year_err}
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
message = """Subject: Finalizo WS de Publimetro


Tiempo total: """ + str(round(elapsed_time/60, 3)) + "min" \
\
"""\n\nTotal articulos: """ + str(len(links_tot)) + \
\
"""\n\nTotal errores: """ + str(len(errores))

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)

