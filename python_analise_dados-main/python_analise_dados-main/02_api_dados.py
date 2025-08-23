### servicodados.ibge.gov.br 
#http.dog

import json, requests
name = input('Escreva o nome a ser buscado')
resposta = requests.get('https://servicodados.ibge.gov.br/api/v2/censos/nomes/karen')

jsonDados = json.loads(resposta.text)
print = (jsonDados[0]['res'])