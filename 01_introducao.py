import pandas as pd 

# carregar dados da planilha
caminho = 'C:/Users/sabado/Desktop/python_analise_dados-main/python_analise_dados-main/01_base_vendas.xlsx'

# aqui le o arquivo - incluir o nome da aba aba pq é excel
df1 = pd.read_excel(caminho, sheet_name='Relatório de Vendas')
df2 = pd.read_excel(caminho, sheet_name= 'Relatório de Vendas1')

#exibir as primeiras linhhas das tabelas
print('----------Primeiro relatório---------')
print(df1.head())

print('----------Segundo relatório---------')
print(df2.head()) 

# verificar duplicatas 
print('Duplicadas no relatório 01')
print(df1.duplicated().sum())

print('Duplicadas no relatório 02')
print(df2.duplicated().sum())

# consolidar tabelas 
print('Dados consolidados!')
dfConsolidado = pd.concat([df1,df2],ignore_index=True)
print(dfConsolidado.head())

# exibir o numero de clientes por cidade
clientesPorCidade = dfConsolidado.groupby('Cidade')['Cliente'].nunique().sort_values(ascending=False)
print(clientesPorCidade)

# numero de vendas por plano 
vendasPorPlano = dfConsolidado['Plano Vendido'].value_counts()
print('Numero de vendas por Plano')
print(vendasPorPlano)

# exibir as 3 cidades com mais clientes 
top3cidades = clientesPorCidade.head(3)
# top3cidades = clientesPorCidade.shot_values(ascending=False).head(3) --- sintaxe incluindo a ordenação
print('Top 3 cidades')
print(top3cidades)

# adionar uma nova coluna de status 
# vamos classificar os planos como premium se for enterprise, os demais serão 'padrão'

dfConsolidado['Status'] = dfConsolidado ['Plano Vendido'].apply(lambda x:'Premium' if x == 'Enterprise' else 'Padrão')

statusDist = dfConsolidado['Status'].value_counts()
print( statusDist)

# Salvar tabela em Excel 
# Primeiro em excel
dfConsolidado.to_excel('dados_consolidados.xlsx', index=False)
print('Dados salvos em xlsx')

# Depois em csv 
dfConsolidado.to_csv('dados_consolidados.csv',index=False)
print('Dados salvos em CSV')

