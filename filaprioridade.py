"""Estruturas de Dados e Algoritmos 
Aluno: Eduardo Fontes Baltazar da Silveira 
Trabalho : Algoritmo de controle de fila de espera: 
Considere um sistema de controle de fila de espera para um serviço qualquer. O sistema deve permitir a inclusão de pessoas a serem atendidas e a exclusão, quando solicitado, indicando a pessoa que será atendida a seguir. 

Para a inclusão, a pessoa deve informar seu nome, e se é prioridade. O sistema deve gerar uma senha aleatória e montar um nó (nome, senha e prioridade) para ser inserida nesta fila. A inclusão na fila deve ocorrer da seguinte forma: se a pessoa não tiver prioridade a inclusão deve ocorrer no final da fila; se a pessoa tiver prioridade, a inclusão deve ocorrer na fila no final do último bloco de prioridades, ou criando um novo bloco de prioridades, considerando que cada bloco de prioridades pode ter até 2 pessoas, e que entre cada bloco de prioridades pode ter até 2 pessoas sem prioridade. Desta forma a fila fica no seguinte formato: 1 bloco de prioridades, seguido de 1 bloco sem prioridades, e assim por diante. 

A exclusão deve ocorrer como em uma fila comum, sempre o primeiro da fila.

A fila deve ser construída de forma encadeada.

Deve ser feito e entregue o algoritmo (em um arquivo pdf) e um programa Python equivalente (arquivo py).

"""
import random
import string

class Pessoa:
    def __init__(self, nome, senha, prioridade):
        self.nome = nome
        self.senha = senha
        self.prioridade = prioridade
        self.prox = None

class Fila:
    def __init__(self):
        self.inicio = None
        self.fim = None

def gerar_senha_aleatoria():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def incluir_pessoa(fila, nome, prioridade):
    nova_pessoa = Pessoa(nome, gerar_senha_aleatoria(), prioridade)
    
    if fila.inicio is None:  
        fila.inicio = nova_pessoa
        fila.fim = nova_pessoa
    else:
        if prioridade:
            percorrer = fila.inicio
            anterior = None
            proximo = percorrer.prox
            par = False
            adicionarInicio = True
            # busca onde inserir prioridade
            while proximo is not None and not par:
                # se achou par
                if percorrer.prioridade and (anterior is None or not anterior.prioridade) and not proximo.prioridade:
                    par = True
                    adicionarInicio = False
                else:
                    # se não tiver nenhuma prioridade
                    if percorrer.prioridade:
                        adicionarInicio = False
                    # iteração
                    anterior = percorrer
                    percorrer = proximo
                    proximo = proximo.prox
            if par:
                percorrer.prox = nova_pessoa
                nova_pessoa.prox = proximo
            else:
                if adicionarInicio:
                    aux = fila.inicio
                    fila.inicio = nova_pessoa
                    nova_pessoa.prox = aux
                else:
                    # último caso: caso não tenha par e não possa adicionar no início, então adicionar entre dois sem prioridade
                    percorrer = fila.inicio
                    proximo = percorrer.prox
                    anterior = None
                    insercao = False
                    while proximo is not None and not insercao:
                        if not percorrer.prioridade and (not proximo.prioridade or proximo is None) and (not anterior.prioridade or anterior is None):
                            insercao = True
                        else:
                            anterior = percorrer
                            percorrer = proximo
                            proximo = proximo.prox
                    if insercao: # se achou lugar para inserir 
                        percorrer.prox = nova_pessoa
                        nova_pessoa.prox = proximo
                    else: # se não achou lugar para inserir
                        fila.fim.prox = nova_pessoa
                        fila.fim = nova_pessoa
        else: # se não for prioridade
            fila.fim.prox = nova_pessoa
            fila.fim = nova_pessoa

def excluir_pessoa(fila):
    if fila.inicio is not None:
        a_remover = fila.inicio
        fila.inicio = fila.inicio.prox
        if fila.inicio is None:
            fila.fim = None
        del a_remover

def proxima_pessoa(fila):
    if fila.inicio is not None:
        return fila.inicio.nome
    else:
        return "Fila vazia"

# Exemplo de uso
fila = Fila()
incluir_pessoa(fila, "Ciclope", False)
incluir_pessoa(fila, "Jean Grey", True)
incluir_pessoa(fila, "Tempestade", False)
incluir_pessoa(fila, "Wolverine", True)
incluir_pessoa(fila, "Professor X", False)
incluir_pessoa(fila, "Fera", True)
incluir_pessoa(fila, "Noturno", False)
incluir_pessoa(fila, "Colossus", True)

while fila.inicio is not None:
    print(proxima_pessoa(fila))
    excluir_pessoa(fila)
#Output esperado:Jean Grey, Wolverine (bloco1 prioridade), Ciclope, Tempestade (bloco2 sem prioridade),
#                 Fera, Colossus (bloco3 prioridade), Professor X, Noturno (bloco4 sem prioridade)