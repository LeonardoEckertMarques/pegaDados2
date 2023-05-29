# https://github.com/stchris/untangle
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
for entry in system.scandir(path='C://Users//Leonardo//Desktop//xml//'):
  if not entry.name.startswith('.') and entry.is_file():
    arquivos.append(entry.name)
	
# gerando a competencia do arquivos
for i in range(len(arquivos)):
        
	nfse = xml.parse('C://Users//Leonardo//Desktop//xml//'+arquivos[i])

	try:
		competencias.append(nfse.CompNfse.Nfse.InfNfse.Competencia.cdata[0:10])
		valorServicos = float(nfse.CompNfse.Nfse.InfNfse.Servico.Valores.ValorServicos.cdata)
		valorIss = float(nfse.CompNfse.Nfse.InfNfse.Servico.Valores.ValorIss.cdata)
		valorIssRetido = float(nfse.CompNfse.Nfse.InfNfse.Servico.Valores.ValorIssRetido.cdata)
		baseCalculo = float(nfse.CompNfse.Nfse.InfNfse.Servico.Valores.BaseCalculo.cdata)
		valorLiquidoNfse = float(nfse.CompNfse.Nfse.InfNfse.Servico.Valores.ValorLiquidoNfse.cdata)

	except AttributeError:
		pass

	retorno.append({
		'Competencia' : competencias[i],
      	'ValorServicos': valorServicos,
      	'ValorIss': valorIss,
      	'ValorIssRetido': valorIssRetido,
      	'BaseCalculo': baseCalculo,
      	'ValorLiquidoNfse': valorLiquidoNfse,
	})


	if comp == retorno[i]["Competencia"]:
		
		retorno[i]["ValorServicos"] += (retorno[i-1]["ValorServicos"])
		retorno[i]["ValorIss"] += (retorno[i-1]["ValorIss"])
		retorno[i]["ValorIssRetido"] += (retorno[i-1]["ValorIssRetido"])
		retorno[i]["BaseCalculo"] += (retorno[i-1]["BaseCalculo"])
		retorno[i]["ValorLiquidoNfse"] += (retorno[i-1]["ValorLiquidoNfse"])
		
		resultado.pop()

		resultado.append({
			'Competencia' : competencias[i],
			'ValorServicos': retorno[i]["ValorServicos"],
			'ValorIss': retorno[i]["ValorIss"],
			'ValorIssRetido': retorno[i]["ValorIssRetido"],
			'BaseCalculo': retorno[i]["BaseCalculo"],
			'ValorLiquidoNfse': retorno[i]["ValorLiquidoNfse"],
		})

	else:		
		comp = retorno[i]["Competencia"]
		resultado.append({
			'Competencia' : competencias[i],
			'ValorServicos': retorno[i]["ValorServicos"],
			'ValorIss': retorno[i]["ValorIss"],
			'ValorIssRetido': retorno[i]["ValorIssRetido"],
			'BaseCalculo': retorno[i]["BaseCalculo"],
			'ValorLiquidoNfse': retorno[i]["ValorLiquidoNfse"],
		})
	

tabela = pd.DataFrame(resultado)
tabela.to_csv('C://Users//Leonardo//Desktop//tabela.csv')
