
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

import matplotlib.pyplot as plt

import time

from matplotlib.backends.backend_pdf import PdfPages




start_time = time.time()


print("\nStarting program...")


#%%

# 1) ---> Definir parametros:
    
    
user = r"\srjc2"

nombre_base = "\\WS - Consolidado articulos.xlsx"

path = r"C:\Users" + user + r"\OneDrive\Documentos\GitHub\MCPP_juan.salgado\Proyecto final"

path_base = path + r"\0_Base_consolidada"

path_nlp = path + r"\2_NLP"

output = path + r"\3_Output"


df = pd.read_excel(path_nlp + r"\merge_bases.xlsx")

df2 = pd.read_excel(path_base + r"\WS - Consolidado articulos.xlsx")

df['day'] = 1

df.rename(columns={"Anio": "year", "Mes": "month"}, inplace = True)

df = df[df.year != 2019]

df['date'] = pd.to_datetime(df[['year', 'month', 'day']])


#%%

# ---> Analisis de los articulos

# 1) ---> Articulos por dia

grouped_dates = df.groupby(df['date'].apply(lambda x : x.date()))

grouped_dates = grouped_dates['date'].aggregate(len)

#grouped_dates.plot.line()

ax = grouped_dates.plot(color = "chocolate")

# _ = plt.xticks(rotation=90, )
_ = plt.grid()
_ = plt.xlabel('Años')
_ = plt.ylabel('Cantidad articulos')
_ = plt.title('Total articulos recopilados')
_ = plt.rc('xtick', labelsize=6)
_ = plt.rc('ytick', labelsize=6)
params = {'legend.fontsize': 10,
      'legend.handlelength': 1.3}
_ = plt.rcParams.update(params)

pdf = PdfPages(output + '\\graph_1.pdf')

pdf.savefig()

pdf.close()


#%%
# 2) ---> Articulos por medio

grouped_medios = df2.groupby(['Medio']).size()

ax = grouped_medios.sort_values(ascending=True).plot(color = "darkcyan",
                               kind='barh')

#_ = plt.xticks(rotation=13, )
_ = plt.grid()
_ = plt.xlabel('Cantidad articulos')
_ = plt.ylabel('Medios')
_ = plt.title('Total articulos por medio')
_ = plt.rc('xtick', labelsize=6)
_ = plt.rc('ytick', labelsize=6)
params = {'legend.fontsize': 10,
      'legend.handlelength': 1.3}
_ = plt.rcParams.update(params)

pdf = PdfPages(output + '\\graph_2.pdf')

pdf.savefig()

pdf.close()


#%%
# 2) ---> Articulos por palabra

grouped_pals = df2.groupby(['Palabra buscada']).size()

ax = grouped_pals.sort_values(ascending=True).plot(color = "y",
                               kind='barh')

#_ = plt.xticks(rotation=13, )
_ = plt.tight_layout()
_ = plt.grid()
_ = plt.xlabel('Cantidad articulos')
#_ = plt.ylabel('Palabra buscada')
#_ = plt.title('Total articulos por palabra buscada')
_ = plt.rc('xtick', labelsize=6)

y_axis = ax.axes.get_yaxis()
y_label = y_axis.get_label()
y_label.set_visible(False)

x_axis = ax.axes.get_xaxis()
x_label = x_axis.get_label()
x_label.set_visible(False)


_ = plt.rc('ytick', labelsize=6)
params = {'legend.fontsize': 10,
      'legend.handlelength': 1.3}
_ = plt.rcParams.update(params)

pdf = PdfPages(output + '\\graph_3.pdf')

pdf.savefig()

pdf.close()


#%%
# 4) ---> Descripcion crimenes

crimes = ['Violenciasexual', 'Homicidio', 'Hurto',
          'Extorsion', 'Secuestro', 'date']

crimes2 = ['Violenciasexual', 'Homicidio', 'Hurto',
          'Extorsion', 'Secuestro']

df_crimes = df[crimes]

grouped_crimes = df_crimes.groupby('date').sum()

grouped_crimes.reset_index(inplace=True)

ax = grouped_crimes.plot(x="date", y=crimes2)

#_ = plt.xticks(rotation=13, )
_ = plt.tight_layout()
_ = plt.grid()
_ = plt.xlabel('Años')
_ = plt.ylabel('Cantidad articulos')
#_ = plt.title('Total articulos clasificados en crimenes')
_ = plt.rc('xtick', labelsize=6)


y_axis = ax.axes.get_yaxis()
y_label = y_axis.get_label()
y_label.set_visible(False)


_ = plt.rc('ytick', labelsize=6)
params = {'legend.fontsize': 7,
      'legend.handlelength': 1.3}
_ = plt.rcParams.update(params)

pdf = PdfPages(output + '\\graph_4.pdf')

pdf.savefig()

pdf.close()


#%%
# 4) ---> Descripcion crimenes

crimes = ['Venezolano', 'Crimenorganizado', 'date']

crimes2 = ['Venezolano', 'Crimenorganizado']

df_crimes = df[crimes]

grouped_crimes = df_crimes.groupby('date').sum()

grouped_crimes.reset_index(inplace=True)

ax = grouped_crimes.plot(x="date", y=crimes2)

#_ = plt.xticks(rotation=13, )
_ = plt.tight_layout()
_ = plt.grid()
_ = plt.xlabel('Años')
_ = plt.ylabel('Cantidad articulos')
#_ = plt.title('Total articulos clasificados en crimenes')
_ = plt.rc('xtick', labelsize=6)


y_axis = ax.axes.get_yaxis()
y_label = y_axis.get_label()
y_label.set_visible(False)


_ = plt.rc('ytick', labelsize=6)
params = {'legend.fontsize': 7,
      'legend.handlelength': 1.3}
_ = plt.rcParams.update(params)

pdf = PdfPages(output + '\\graph_5.pdf')

pdf.savefig()

pdf.close()




