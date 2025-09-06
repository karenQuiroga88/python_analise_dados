from flask import Flask, request, render_template_string
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.io as pio
import random
import os

pio.renderers.default = "browser"

caminho = "C:/Users/sabado/Desktop/python_analise_dados-main/"
tabela = ["drinks.csv","avengers.csv"]

codHtml = '''
    <h1> Dashboards - Consumo de Alcool </h1>
    <h2> Parte 01 </h2>
        <ul>
            <li><a href="/grafico1"> Top 10 paises em consumo de alcool </a></li>
            <li><a href="/grafico2"> Media de consumo por Tipo </a></li>
            <li><a href="/grafico3"> Consumo total por Região </a></li>
            <li><a href="/grafico4"> Comparativo entre tipos de bebidas </a></li>
            <li><a href="/pais"> Insights por pais </a></li>
        </ul>
    <h2> Parte 02 </h2>
        <ul>
            <li><a href="/comparar"> Comparar </a></li>
            <li><a href="/upload"> Upload CSV Vingadores </a></li>
            <li><a href="/apagar"> Apagar Tabela </a></li>
            <li><a href="/ver"> Ver Tabela </a></li>
            <li><a href="/vaa"> V.A.A (Vingadores Alcolicos Anonimos) </a></li>
        </ul>
'''

def carregarCsv():
    try:
        dfDrinks = pd.read_csv(os.path.join(caminho, tabela[0]))
        dfAvengers = pd.read_csv(os.path.join(caminho, tabela[1]), encoding='latin1')
        return dfDrinks, dfAvengers
    except Exception as erro:
        print(f"Erro ao carregar os arquivos CSV: {erro}")
        return None, None

def criarBandoDados():
    conn = sqlite3.connect(f"{caminho}banco01.bd")
    #carregar dados usando nossa função criada aneriormente
    dfDrinks, dfAvengers = carregarCsv()
    if dfDrinks is None or dfAvengers is None:
        print("Falha ao carregar os dados!")
        return

    #inserir as tabelas no banco de dados
    dfDrinks.to_sql("bebidas", conn, if_exists="replace", index=False)
    dfAvengers.to_sql("vingadores", conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string(codHtml)

@app.route('/grafico1')
def grafico1():
    with sqlite3.connect(f'{caminho}banco01.bd') as conn:
        df = pd.read_sql_query("""
            SELECT country, total_litres_of_pure_alcohol
            FROM bebidas
            ORDER BY total_litres_of_pure_alcohol DESC
            LIMIT 10
        """, conn)
    figuraGrafico01 = px.bar(
        df,
        x = "country", 
        y =  "total_litres_of_pure_alcohol",
        title = "Top 10 paises com maior consumo de alcool"
    )
    return figuraGrafico01.to_html()

@app.route('/grafico2')
def grafico2():
     with sqlite3.connect(f'{caminho}banco01.bd') as conn:
         df = pd.read_sql_query ("""
        SELECT AVG(beer_servings) as cerveja,
            AVG(beer_servings) as destilados,
            AVG(wine_servings) as vinhos
            FROM bebidas                                                                         
""",conn)
         
     df_melted = df.melt(var_name='Bebidas', value_name= 'Média de Porções')
     figuraGrafico02= px.bar(
         df_melted,
         x = "Bebidas",
         y = "Média de Porções",
         title = "Media de consumo global por tipo"
     )
     return figuraGrafico02.to_html()

@app.route("/grafico3")
def grafico3(): 
    regioes = {
        'Europa': ['Franca', 'Germany', 'Spain', 'Italy', 'Portugal'],
        'Asia':['China','Japan', 'India', 'Thailand'],
        'Africa': [ 'Angola', 'Nigéria', 'Egypt', 'Algeria'],
        'Americas': ['USA', 'Canada', 'Brasil', 'Argentina', 'Mexico']
    }
    dados = []
    with sqlite3.connect(f'{caminho}banco01.bd') as conn:
    #itera sobre o dicionário, de regioes onde cada chave (regiao tem uma lista de paises)
        for regiao, paises in regioes.items():
            placeholdelders = ",".join([f" '{pais}'"for pais in paises])
            query = f"""
            SELECT SUM(total_litres_of_pure_alcohol) as total
            FROM bebidas
            WHERE country IN ({placeholdelders})
            """
            total = pd.read_sql_query(query,conn).iloc[0,0] ###  caso o valor não seja aceitável, exiba 0; iloc
            dados.append({
                "Região": regiao,
                "Consumo total": total
        })

    dfRegioes = pd.DataFrame(dados)
    figuraGrafico3 = px.pie(
        dfRegioes,
        names = "Região",
        values = "Consumo total",
        title = "Consumo total por Região"
    )
    return figuraGrafico3.to_html()

@app.route('/comparar', methods=['POST','GET'])
def comparar():
    opcoes = [
        'beer_servings',
        'spirit',
        'wine_servings'
        ]

    if request.method == 'POST':
        eixoX = request.form.get('eixo_x')
        eixoY = request.form.get('eixo_y')
        if eixoX == eixoY:
            return "<marquee>Escolha outra opção..</marquee>"
        conn = sqlite3.connect(f'{caminho}banco01.bd')
        df = pd.read_sql_query("SELECT country, {}, {} FROM bebidas".format(eixoX, eixoY), conn)
        conn.close()
        figuraComparar = px.scatter(
            df,
            x = eixoX,
            y = eixoY,
            title = f"Comparação entre {eixoX} VS {eixoY}"
        )
        figuraComparar.update_traces(
            textposition = "top center"
        )
        return figuraComparar.to_html()
    
            
    return render_template_string("""
    <style>
/* Fundo geral da página */
body {
    font-family: 'Segoe UI', sans-serif;
    background: #111;
    color: #eee;
    margin: 0;
    padding: 2rem;
    display: flex;
    justify-content: center;
}

/* Título */
h2 {
    text-align: center;
    color: #b97ff7;
    margin-bottom: 1.2rem;
    font-size: 1.6rem;
}

/* Formulário */
form {
    background: #1c1c1c;
    padding: 1.5rem 2rem;
    border-radius: 8px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
    width: 100%;
    max-width: 320px;
}

/* Rótulos */
label {
    display: block;
    margin-bottom: 0.3rem;
    color: #ccc;
    font-size: 0.95rem;
}

/* Select (combobox) */
select {
    width: 100%;
    padding: 0.4rem 0.6rem;
    margin-bottom: 1rem;
    border: 1px solid #555;
    border-radius: 4px;
    background-color: #2a2a2a;
    color: #eee;
    font-size: 0.95rem;
}

/* Botão de submit */
input[type="submit"] {
    background-color: #b97ff7;
    color: #111;
    border: none;
    padding: 0.6rem 1rem;
    font-size: 1rem;
    font-weight: bold;
    border-radius: 4px;
    cursor: pointer;
    width: 100%;
    transition: background-color 0.3s ease;
}

input[type="submit"]:hover {
    background-color: #9e5be0;
}

/* Remover <br> visuais */
br {
    display: none;
}


    </style>                              

    <h2> Comparar Campos </h2> 
    <form method="POST"> 
        <label for="eixo_x"> Eixo X: </label>
        <select name="eixo_x">
            {% for opcao in opcoes %}                      
                <option value={{opcao}}"> {{opcao}}</option>
             {% endfor %}                      
        </select>
        <br></br>
                                  
        <label for="eixo_y"> Eixo Y: </label>
        <select name="eixo_y">
            {% for opcao in opcoes %}
                <option value={{opcao}}"> {{opcao}} </option>
            {% endfor %}
                         
        <select name="eixo_y">
                                  
        </select>
        <br></br>
                                  
        <input type="submit" value="--Comparar--"> 
    </form>
""", opcoes = opcoes)


if __name__ == '__main__':
    criarBandoDados()
    app.run(debug=True)

