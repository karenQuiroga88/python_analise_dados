import requests
from bs4 import BeautifulSoup
import pandas as pd
import time 
import random 
import sqlite3
import datetime  

### headers brower user agent --- procurar na net ( what is  my brower)
headers = {
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0 Safari/537.36'
}


baseURL = 'https://www.adorocinema.com/filmes/melhores/'
filmes = []
data_hoje = datetime.date.today().strftime("%d-%m-%Y")
agora = datetime.datetime.now()
paginaLimite = 2
card_temp_min= 1
card_temp_max= 3
pag_temp_min= 2
pag_temp_max= 4
pasta = 'C:/Users/sabado/Desktop/python_analise_dados/python_analise_dados-main/'
bancoDados = "banco_filmes.db"
saidaCSV = f'filmes_adoro_ciname_{data_hoje}.csv'


for pagina in range(1, paginaLimite + 1):
    url = f"{baseURL}?page={pagina}"
    print(f"Colentando da página{pagina}\nEndereço: {url}\n")
    resposta = requests.get(url, headers=headers)
    soup = BeautifulSoup(resposta.text, "html.parser")  ### identifica as tags - usado para webscraping / compreender html

    if resposta .status_code!=200:
        print(f'Erro ao carregar a pagina {pagina}).\nCodigo do erro é: {resposta.status_code}')
        continue 
    
    cards = soup.find_all("div", class_="card entity-card entity-card-list cf")

    for card in cards:
        try: 
            # capturarmp título e o link da página do filme
            titulo_tag = card.find( "a", class_= "meta-title-link")
            titulo = titulo_tag.text.strip() if titulo_tag else "N/A"
            link = "https://www.adorocinema.com/" + titulo_tag ['href'] if titulo_tag else None 

            # capturar a nota do filme
            nota_tag = card.find("span", class_="stareval_note")
            nota = nota_tag.text.strip().replace(",",".") if nota_tag else "N/A"

            if link: 
                filme_resposta = requests.get(link, headers=headers)
                filme_soup = BeautifulSoup(filme_resposta.text,"html.parser")

                #captura o diretor do filme 
                diretor_tag = filme_soup.find("div",class_="meta-body-item meta-body-direction meta-body-oneline")

                if diretor_tag:
                    diretor =(
                    diretor_tag.text
                    .strip()
                    .replace("Direção:", "")
                    .replace("," , "")
                    .replace("|","")
                    .strip()
                ) if diretor_tag else "N/A"
                
                #captura os generos
                genero_blocks = filme_soup.find("div", class_="meta-body-info")
                if genero_blocks:
                    genero_links = genero_blocks.find_all("a")
                    generos= [g.text.strip() for g in genero_links] 
                    categoria = ", ".join(generos[:3]) if generos else "N/A" ### aqui está capurando somente os 3 primeiros, caso tenha mais de 1
                else:
                    categoria = "N/A"
                
                # captura o ano de lançamento do filme 
                # a tag é um span, e o nome da class é date

                ano_tag = filme_soup.find("span", class_="date") if genero_blocks else None
                ano = ano_tag.text.strip () if ano_tag else "N/A"

                #if titulo !="N/A" and link != "N/A" and nota != "N/A":
                if titulo != "N/A" and link is not None and nota is not None:
                    filmes.append({
                        "Titulo": titulo,
                        "Direção": diretor,
                        "Nota": nota,
                        "Link": link,
                        "Ano": ano,
                        "Categoria": categoria
                    })

                else: 
                    print(f"Filme Incompleto ou erro na coleta de dados do filme {titulo}")

                tempo = random.uniform(card_temp_min, card_temp_max) ## aqui faz o tempo parar para não parecer robo
                print(f'tempo de espera entre filmes: {tempo:.1f}')
                time.sleep(tempo)
        except Exception as erro:
            print(f"Erro ao processar o título {titulo}\n Erro: {erro}")
# espera um tempo entre uma página e outra

    tempo = random.uniform(pag_temp_min, pag_temp_max)
    time.sleep(tempo) 

df = pd.DataFrame(filmes)
print(df.head())
