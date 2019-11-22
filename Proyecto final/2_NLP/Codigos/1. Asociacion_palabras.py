
#%%

# ---> Clear all items in memory:

print("\nClearing all data in memory...")

from IPython import get_ipython
get_ipython().magic('reset -f')


#%%


# -----------------------------------------------------------------------------
### ----------------------------- Cargar paquetes -----------------------------
# -----------------------------------------------------------------------------


#%% 


import pandas as pd

import re

import unidecode

import time

import os



start_time = time.time()


print("\nStarting program...")



#%%


# -----------------------------------------------------------------------------
### ------------------------- Definir funciones a usar ------------------------
# -----------------------------------------------------------------------------


#%%

# 1) ---> Funcion para limpiar los strings:


def limpiar_string(string):
    
    # Eliminate accentuated characters
    new_str = unidecode.unidecode(string)
    
    # Eliminate special characters
    new_str = re.sub('[^A-Za-z0-9 ]+', ' ', new_str)
    
    # To lower
    new_str = new_str.lower()
    
    return new_str



#%%
    
# 2) ---> Funcion para leer la base consolidada de articulos:


def leer_base_articulos(nombre_base, path_base):
    
    elapsed_time_1 = time.time() - start_time
        
    print("\nLeyendo base de articulos. Total time: {} min "
              .format(round(elapsed_time_1/60, 3)))
    
    articulos = pd.read_excel(path_base + nombre_base)
    
    articulos.Contenido = " " + articulos.Contenido + " "
    
    return articulos
    


#%%
    
# 3) ---> Funcion para leer y limpiar las listas:


def leer_lista(nombre_lista, path_lista):
    
    elapsed_time_1 = time.time() - start_time
        
    print("\nLeyendo base de listas. Total time: {} min "
              .format(round(elapsed_time_1/60, 3)))
    
    lista = pd.read_excel(path_lista + nombre_lista)
    
    # Crear filas para las palabras a buscar con '*'
    
    adicionar = lista[lista['Raiz_a_buscar'].str.contains("\*")]
    
    lista = lista[~lista['Raiz_a_buscar'].isin(adicionar['Raiz_a_buscar'])]
    
    caracteres_extra = [' ']
    
    for car in caracteres_extra:
        
        temp = adicionar.loc[:]
        
        temp['Nueva'] = adicionar['Raiz_a_buscar'].apply (lambda x: x[:-1] + car)
        
        temp['Raiz_a_buscar'] = temp['Nueva']
        
        temp = temp.drop('Nueva', axis = 1)
        
        lista = lista.append(temp)
    
    lista_new_column1 = []
        
    for pal in lista['Raiz_a_buscar']:
        
        lista_new_column1.append(limpiar_string(pal))
    
    lista = lista.drop('Raiz_a_buscar', axis=1)
    
    lista['Palabra_a_buscar'] = lista_new_column1

    lista['Palabra_a_buscar'] = lista['Palabra_a_buscar'].apply (lambda x: ' ' + x)

    return lista



#%%
    
# 4) ---> Funcion para limpiar los articulos:
    

def limpiar_articulos(articulos):

    elapsed_time_1 = time.time() - start_time
        
    print("\nLimpiando cada articulo. Total time: {} min "
              .format(round(elapsed_time_1/60, 3)))
    
    
    # Remove articles with **Especial** in title and content; add title to article (if empty)
    
    elapsed_time_1 = time.time() - start_time
        
    print("\nEliminando espacios y **Especial**. Tiempo total: {} min "
              .format(round(elapsed_time_1/60, 3)))
    
    type_content = []
    
    new_content = []
    
    for x in articulos.Contenido[:]:
        
        type_content.append(str(type(x)))
    
    for i in range(len(type_content)):
        
        if 'str' in type_content[i] and '**Especial**' in articulos.Contenido[i]:
            
            new_content.append(articulos.Titulo[i])
            
        elif 'str' in type_content[i]:
            
            new_content.append(articulos.Contenido[i])
            
        else:
            
            new_content.append(articulos.Titulo[i])
            
    articulos = articulos.drop("Contenido", axis=1)
    
    articulos['Contenido'] = new_content
    
    
    articulos = articulos[articulos.Contenido != '**Especial**']
    
    # Clean each article: remove accents & special characters
    
    new_content = []
    
    articulos_error = []
    
    content_error = []
    
    elapsed_time_1 = time.time() - start_time
        
    print("\nEliminando caracteres y acentos. Tiempo total: {} min "
              .format(round(elapsed_time_1/60, 3)))
    
    for i in range(len(articulos.Contenido)):
        
        try:
            new_content.append(limpiar_string(articulos.Contenido[i]))
        
        except:
            
            print("\nArticulo error: ", i)
            
            articulos_error.append(i)
            content_error.append(str(articulos.Contenido[i]))
    
    articulos = articulos.drop("Contenido", axis=1)
    
    articulos['Contenido'] = new_content
    
    return articulos


   
#%%
    
# 5) ---> Funcion para rellenar base conteo:
    

def bases_conteo(articulos, lista, nombre_lista, file_message):
    
    time.sleep(1.5)
    
    elapsed_time_1 = time.time() - start_time
    
    print("\nCreacion base conteo. Total time: {} min "
              .format(round(elapsed_time_1/60, 3)))
    
    # Base conteo basico palabras a buscar
    df_conteo = pd.DataFrame({'Columna inicializadora': 
        [x for x in range(len(articulos['Contenido']))]})
    
    # Base con lista de palabras de interes
    df_conteo_pal_buscar = pd.DataFrame({'Columna inicializadora': 
        [x for x in range(len(articulos['Contenido']))]})
    
    # Base con lista de variables
    df_conteo_variable = pd.DataFrame({'Columna inicializadora': 
        [x for x in range(len(articulos['Contenido']))]})
    
    for x in range(len(lista.Palabra_a_buscar)):
        
        df_conteo[lista.Palabra_a_buscar[x]] = 0
        
        df_conteo_pal_buscar[lista['Palabra_interes'][x]] = 0
        
        df_conteo_variable[lista['Variable'][x]] = 0
    
    df_conteo = df_conteo.drop("Columna inicializadora", axis=1)
    
    df_conteo_pal_buscar = df_conteo_pal_buscar.drop("Columna inicializadora", 
                                                     axis=1)
    
    df_conteo_variable = df_conteo_variable.drop("Columna inicializadora", 
                                                 axis=1)
    
    elapsed_time_1 = time.time() - start_time
    
    print("\nRelleno base conteo. Total time: {} min "
              .format(round(elapsed_time_1/60, 3)))
    
    tiempo_inicio = time.time()
    
    print("\nIniciando relleno base conteo...")
        
    contador = 0
    
    for pal in df_conteo:
        
        if contador % file_message == 0:
        
            elapsed_time_1 = time.time() - tiempo_inicio
    
            print("\nPalabra numero: ", contador, "Tiempo total loop: {} min"
                  .format(round(elapsed_time_1/60, 3)))
        
        df_conteo[pal] = articulos.Contenido.apply(lambda x: x.count(pal))
        
        contador = contador + 1
            
    
    elapsed_time_1 = time.time() - tiempo_inicio
    
    print("\nRellenada base conteo. Total time: {} min "
              .format(round(elapsed_time_1/60, 3)))

    
    df_conteo['Link'] = articulos.Link
    df_conteo_pal_buscar['Link'] = articulos.Link
    df_conteo_variable['Link'] = articulos.Link
    
    df_conteo['Anio'] = articulos.Anio
    df_conteo_pal_buscar['Anio'] = articulos.Anio
    df_conteo_variable['Anio'] = articulos.Anio
    
    df_conteo['Mes'] = articulos.Mes
    df_conteo_pal_buscar['Mes'] = articulos.Mes
    df_conteo_variable['Mes'] = articulos.Mes
    
    print("\nGuardando base conteo basico...")
    
    df_conteo.to_excel("Conteo_basico_" + nombre_lista[1:])
    
    return df_conteo, df_conteo_pal_buscar, df_conteo_variable



#%%
    
# 6) ---> Funcion para rellenar base conteo (por palabra interes):


def relleno_base_pal_interes(df_conteo_pal_interes, df_conteo_basico, lista):
    
    # Exclude last tree columns of 'df_conteo_basico': Link, Anio, Mes
    
    print("\nIniciando relleno base palabra interes...")
    
    time.sleep(1.5)
    
    for col in df_conteo_basico.columns[:-3]:
        
        pal_interes = lista[lista['Palabra_a_buscar'] == col]['Palabra_interes'].item()
        
        incluir = lista[lista['Palabra_a_buscar'] == col]['Incluir'].item()
        
        if incluir == 1:
            
            df_conteo_pal_interes[pal_interes] = df_conteo_pal_interes[pal_interes] + \
            df_conteo_basico[col]
            
        else:
            
            df_conteo_pal_interes[pal_interes] = df_conteo_pal_interes[pal_interes] - \
            df_conteo_basico[col]
            
    print("\nGuardando base conteo palabra interes...")
    
    df_conteo_pal_interes.to_excel("Conteo_pal_interes_" + nombre_lista[1:])
            
        
    return df_conteo_pal_interes
        

#%%
    
# 7) ---> Funcion para rellenar base conteo (por grupo variable):


def relleno_base_variable(df_conteo_variable, df_conteo_basico, lista):
    
    print("\nIniciando relleno base variable...")
    
    time.sleep(1.5)
    
    # Exclude last tree columns of 'df_conteo_basico': Link, Anio, Mes
    
    for col in df_conteo_basico.columns[:-3]:
        
        variable = lista[lista['Palabra_a_buscar'] == col]['Variable'].item()
        
        incluir = lista[lista['Palabra_a_buscar'] == col]['Incluir'].item()
        
        if incluir == 1:
            
            df_conteo_variable[variable] = df_conteo_variable[variable] + \
            df_conteo_basico[col]
            
        else:
            
            df_conteo_variable[variable] = df_conteo_variable[variable] - \
            df_conteo_basico[col]
            
    print("\nGuardando base conteo variable...")
    
    df_conteo_variable.to_excel("Conteo_variable_" + nombre_lista[1:])
            
        
    return df_conteo_variable
  
    
#%%


# -----------------------------------------------------------------------------
### --------------------------- Llamar las funciones --------------------------
# -----------------------------------------------------------------------------


#%%

# 1) ---> Definir parametros:
    
    
user = r"\srjc2"

nombre_base = "\\WS - Consolidado articulos.xlsx"

path = r"C:\Users" + user + r"\OneDrive\Documentos\GitHub\MCPP_juan.salgado\Proyecto final"

path_base = path + r"\0_Base_consolidada"

path_nlp = path + r"\2_NLP"

os.chdir(path_nlp)
 
"""
,

"""                  
nombres_listas = ['\\final1.xlsx',
                  '\\final2.xlsx',
                  '\\final3.xlsx',
                  '\\final4.xlsx',
                  '\\final5.xlsx',
                  '\\final6.xlsx']


path_lista = path_nlp + r"\Listas"



#%%

# 2) ---> Llamar funciones:

articulos = leer_base_articulos(nombre_base, path_base)

articulos = limpiar_articulos(articulos)

for nombre_lista in nombres_listas:
    
    elapsed_time_1 = time.time() - start_time
    
    print("\n--> Procesando lista {}. Tiempo total: {} min "
              .format(nombre_lista, round(elapsed_time_1/60, 3)))

    
    lista = leer_lista(nombre_lista, path_lista)
    
    df_conteo_basico, df_conteo_pal_interes, df_conteo_variable = \
                                bases_conteo(articulos, lista, nombre_lista, 20)
    
    df_conteo_pal_interes = relleno_base_pal_interes(df_conteo_pal_interes, 
                                                     df_conteo_basico, lista)
    
    df_conteo_variable = relleno_base_variable(df_conteo_variable, 
                                                     df_conteo_basico, lista)



#%%


# -----------------------------------------------------------------------------
### ---------------------------- Proceso completado ---------------------------
# -----------------------------------------------------------------------------


#%%
        
elapsed_time_1 = time.time() - start_time
    
print("\nProceso completado. Tiempo total: {} min "
          .format(round(elapsed_time_1/60, 3)))