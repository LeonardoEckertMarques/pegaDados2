#!/usr/bin/env python
# coding: utf-8

# In[15]:


import os as system
import untangle as xml
import pandas as pd

arquivos = []
competencias = []
retorno = []
resultado = []

valorServicos = 0
valorIss = 0
valorIssRetido =  0
baseCalculo =  0
valorLiquidoNfse = 0
comp = ""

# acessa a o diretório xml
for entry in system.scandir(path='C://Users//Suporte//Desktop//xml//'):
    if not entry.name.startswith('.') and entry.is_file():
        arquivos.append(entry.name)

# gerando a competencia do arquivos
for i in range(len(arquivos)):
        
    nfse = xml.parse('C://Users//Suporte//Desktop//xml//'+arquivos[i])

    try:

        competencias.append(nfse.CompNfse.Nfse.InfNfse.Competencia.cdata[0:7])
        valorServicos = float(nfse.CompNfse.Nfse.InfNfse.Servico.Valores.ValorServicos.cdata)
        valorIss = float(nfse.CompNfse.Nfse.InfNfse.Servico.Valores.ValorIss.cdata)
        valorIssRetido = float(nfse.CompNfse.Nfse.InfNfse.Servico.Valores.ValorIssRetido.cdata)
        baseCalculo = float(nfse.CompNfse.Nfse.InfNfse.Servico.Valores.BaseCalculo.cdata)
        valorLiquidoNfse = float(nfse.CompNfse.Nfse.InfNfse.Servico.Valores.ValorLiquidoNfse.cdata)

    except AttributeError:
        pass

    # passando os dados para um retorno... onde estou guardando tudo...
    # inclusive a competência... ou vou usar para pesquisar em seguida...

    retorno.append({
        'ValorServicos': valorServicos,
        'ValorIss': valorIss,
        'ValorIssRetido': valorIssRetido,
        'BaseCalculo': baseCalculo,
        'ValorLiquidoNfse': valorLiquidoNfse,
    })
    
    # comparando a competência com a comp
    if comp == competencias[i]:
        
        # para competências iguais
        retorno[i]["ValorServicos"] += (retorno[i-1]["ValorServicos"])
        retorno[i]["ValorIss"] += (retorno[i-1]["ValorIss"])
        retorno[i]["ValorIssRetido"] += (retorno[i-1]["ValorIssRetido"])
        retorno[i]["BaseCalculo"] += (retorno[i-1]["BaseCalculo"])
        retorno[i]["ValorLiquidoNfse"] += (retorno[i-1]["ValorLiquidoNfse"])
        
        # sempre removo a linha antes de adicionar para o resultado...
        # para que não tenha linhas adicionais!
        resultado.pop()

    else:
        comp = competencias[i]
        
    
    resultado.append({
        'Competencia' : comp,
        'ValorServicos': retorno[i]["ValorServicos"],
        'ValorIss': retorno[i]["ValorIss"],
        'ValorIssRetido': retorno[i]["ValorIssRetido"],
        'BaseCalculo': retorno[i]["BaseCalculo"],
        'ValorLiquidoNfse': retorno[i]["ValorLiquidoNfse"],
    })

# usando o panda para imprimir no formato CSV
tabela = pd.DataFrame(resultado)
tabela.to_csv('C://Users//Suporte//Desktop//tabela.csv')
display(resultado)


# In[11]:





# In[ ]:





# In[ ]:




