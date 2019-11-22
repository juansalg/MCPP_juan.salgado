
#pip install selenium
# pip install MechanicalSoup
import mechanicalsoup
from bs4 import BeautifulSoup as soup
from requests.auth import HTTPBasicAuth
import pandas as pd
import time
import requests
from IPython.core.display import clear_output
from random import randint
import datetime
from selenium import webdriver

#from lxml import html


"""
session_requests = requests.session()
login_url = 'https://login.semana.com'
result = session_requests.get(login_url)
tree = html.fromstring(result.text)
authenticity_token = list(set(tree.xpath("//input[@name='urlReturn']/@value")))[0]
values = {'username': '80198246',
          'urlReturn': 'https://www.semana.com'}
result = session_requests.post(
	login_url, 
	data = values, 
	headers = dict(referer=login_url))
"""

#print (r.content)

def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%m/%d/%Y')
        return True
    except ValueError:
        return False

now=datetime.datetime.now()
dia=str(now)
dia=dia[2:10]

# ,'Vandalismo bogotá', 'Hurto bogotá'
            #'Policía de Bogotá','Inseguridad bogotá','Percepción de seguridad bogotá',
            #'Percepción de inseguridad bogotá','Seguridad ciudadana bogotá',
            #'Orden público bogotá','Violencia bogotá','Asesinato bogotá','Matar bogotá',
           # 'Robo bogotá','Atraco bogotá','Fleteo bogotá','Orden público bogotá',
          #  'Disturbio bogotá','Riña bogotá','Abuso sexual bogotá','Acoso sexual bogotá',
         #'Acoso infantil bogotá','Golpiza bogotá','Linchamiento bogotá',
         #'Policía Nacional bogotá','Dar de baja bogotá',
         #'Violencia sexual bogotá', 'Lesiones personales bogotá']

keywords = ['Seguridad bogota','Homicidio bogotá']
titles = []
links = []
contents = []
dates = []
pal_buscada = []
paginas = []

start_time = time.time()
request = 0
pages = [str(i) for i in range(2,3)]
count = 0

# Path to chrome.exe

# path = r'C:\Users\JUANCAMILO\Desktop\Data_Science\Github\Cerac\Web scraping\Revista Semana\Chrome\chromedriver.exe'

"""
chromeOptions= webdriver.ChromeOptions()
chromeOptions.binary_location = path
options=webdriver.ChromeOptions()
options.add_argument('headless')
browser = webdriver.Chrome(options=options)
"""

# login

#https://www.semana.com/Buscador?query=Seguridad bogota&post=semana&limit=10&offset= 1&from=2010%2F01%2F01&facet0=type%2FArt%C3%ADculo&to=2018%2F12%2F31


#login = requests.get('https://login.semana.com', auth=HTTPBasicAuth('80198246', '80198246'))

"""
browser = mechanicalsoup.Browser()
login_page = browser.get("https://login.semana.com/?urlReturn=https%3A%2F%2Fwww.semana.com%2FBuscador%3Fquery%3D" + keyword)
login_form = login_page.soup.find("form")
login_form.find("input", {"name": "urlReturn"})["value"] = "14221708"
login_response = browser.submit(login_form, login_page.url)
"""


# 14221708 Helen
# 80198246 Felip

login_data = {
        'typeId':	'CC',
        'id':	'80198246',
        'subscriptionCode' : '',
        'urlReturn':	'https://www.semana.com'
        }

with requests.Session() as s:
    url = 'https://login.semana.com/User/LogInSubscriber'
    r = s.get(url)
    #soup = soup(r.content, 'html5lib)
    r = s.post(url, data = login_data)  

    for keyword in keywords:
        for page in pages:
    
    
            page=str((int(page)-1)*10)
            
            url = "https://www.semana.com/Buscador?query=" + keyword + "&post=semana&limit=10&offset= " + page + "&from=2010%2F01%2F01&facet0=type%2FArt%C3%ADculo&to=2018%2F12%2F31"
            
                  #  https://www.semana.com/Buscador?query=Seguridad%20bogota&post=semana&limit=10&offset=%201&from=2010%2F01%2F01&facet0=type%2FArt%C3%ADculo&to=2018%2F12%2F31
            #url = "https://www.semana.com/Buscador?query=" + keyword + \
            #"%20bogot%C3%A1&post=semana&limit=10&offset=" + page + \
            #"&from=2010%2F01%2F01&facet0=type%2FArt%C3%ADculo&to=2018%2F12%2F31"
            #url = "https://www.semana.com/Buscador?query=" + keyword + "&post=semana&limit=10&offset=" + page + "&from=2000%2F01%2F01&facet0=type%2FArt%C3%ADculo"
            print("")
            print(url)
            print("")
            html = s.get(url)
            stringg = str(html.content)
            htmlsoup = soup(html.content,'html5lib')
            time.sleep(randint(2,4))
            request += 1
            count += 1
            elapsed_time = time.time() - start_time
            print("")
            print('Palabra: {}; Página: {}; Tiempo: {} min'.format(keyword, page,
                                          round(elapsed_time/60,3)))
            print("")
            clear_output(wait = True)
            articles = htmlsoup.find_all('div',class_="result")
            if (len(articles) == 0):
                print("")
                print(request)
                print("\nThere were no more articles found with your keyword")
                test_df=pd.DataFrame({'Titulo':titles,
                                          'Fecha':dates,
                                          'Contenido':contents,
                                          'Link':links,
                                          'Palabra buscada':pal_buscada,
                                          'Pagina':paginas})
                break
            else:   
                for oneArticle in articles:
                    link = oneArticle.a['href']
                    content = ''
                    url2 = link
                    link = ''
                    while link == '':
                        try:
                            link = requests.get(url2)
                            break
                        except:
                            print("Connection refused by the server")
                            time.sleep(3)
                            print("Let's try again...")
                            continue
                    print("")
                    print(url2)    
                    noodles=soup(link,'html5lib')
                    content=noodles.find_all('div', id="contentItem")
                    if len(content) != 0 :
                        try:
                                tipo=''
                                date = noodles.find('span', class_="date").text.strip()
                                date=date[2:15]
                                date=date.replace(" ", "  ")
                                date=date[0:10].replace(" ","")
                                if validate(date)==True:
                                    objDate = datetime.datetime.strptime(date, '%m/%d/%Y')
                                    strDate = datetime.datetime.strftime(objDate, '%b %d %Y')
                                else:
                                    objDate = datetime.datetime.strptime(date, '%Y/%m/%d')
                                    strDate = datetime.datetime.strftime(objDate, '%b %d %Y')
                        except:
                            date = '**Especial**'
                                    
                        title = ''
                        
                        if noodles.find('h1', class_="tittleArticuloOpinion") != None:
                            title = noodles.find('h1', class_="tittleArticuloOpinion").text.strip()
                        else:
                            if noodles.find('h1', class_="nameColumnista") != None:
                                title = noodles.find('h1', class_="nameColumnista").text.strip()
                            if noodles.find('h2', class_ = "article-h") != None:
                                title = noodles.find('h2', class_ = "article-h").text.strip()
                                                 
                                
                            titles.append(title)
                            texto=''
                            for textos in content:
                                texto=texto+textos.getText()
                            texto=texto.replace('\n','').strip()
                            contents.append(texto)
                            dates.append(strDate)
                            links.append(url2)
                            pal_buscada.append(keyword)
                            paginas.append(page)
                              
                            
                            test_df=pd.DataFrame({'Titulo':titles,
                                              'Fecha':dates,
                                              'Contenido':contents,
                                              'Link':links,
                                              'Palabra buscada':pal_buscada,
                                              'Pagina':paginas})
                    else :
                        date = 0
                        title = ''
                        if noodles.find('h1', class_="tittleArticuloOpinion") != None:
                            title = noodles.find('h1', class_="tittleArticuloOpinion").text.strip()
                        else:
                            if noodles.find('h1', class_="nameColumnista") != None:
                                title = noodles.find('h1', class_="nameColumnista").text.strip()
                            if noodles.find('h2', class_ = "article-h") != None:
                                title = noodles.find('h2', class_ = "article-h").text.strip()
                        titles.append(title)
                        content="Especial"
                        contents.append(content)
                        dates.append(date)
                        links.append(url2)
                        pal_buscada.append(keyword)
                        paginas.append(page)
                        
                        test_df=pd.DataFrame({'Titulo':titles,
                                          'Fecha':dates,
                                          'Contenido':contents,
                                          'Link':links,
                                          'Palabra buscada':pal_buscada,
                                          'Pagina':paginas})
      
test_df.to_excel("semana_total2.xlsx")

elapsed_time_2 = time.time() - start_time

print("")
print('\nTotal articulos: {} \nNumero de paginas: {} \nArticulos por pagina: {} \nTotal time: {} min'
      .format(len(links),
              len(pages),
              round(len(links)/len(pages), 3),
              round(elapsed_time_2/60, 3)))
    