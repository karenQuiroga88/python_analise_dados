import meu_modulo as mm 
'''
print(mm.soma(2,6))
print(mm.saudacao('Caio',66))

valor_a = int(input('Insira o primeiro valor: '))
valor_b = int(input('Insira o primeiro valor: '))

print(mm.soma(valor_a,valor_b))
'''
from datetime import date
ano_atual = date.today().year
nascimento = int(input('Insita seu nascimento'))
print(mm.idade(nascimento,ano_atual)) 


usarioNasc = int(input('Informe o ano em que masceu: '))
usuarioAtual = int(input('Informe o ano atual: '))
print(mm.calcularIdade(usarioNasc,usuarioAtual))

###notebooklm