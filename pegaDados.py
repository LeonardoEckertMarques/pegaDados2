# https://github.com/stchris/untangle
import os as system
import untangle as xml
import pandas as pd

arquivos = []
competencias = []
retorno = []

valorServicos = 0
valorIss = 0
valorIssRetido =  0
baseCalculo =  0
valorLiquidoNfse = 0

# acessa a o diretório xml
for entry in system.scandir(path='C://Users//Suporte//Desktop//xml//'):
  if not entry.name.startswith('.') and entry.is_file():
    arquivos.append(entry.name)
	
# gerando a competencia do arquivos
for i in range(len(arquivos)):
        
	nfse = xml.parse('C://Users//Suporte//Desktop//xml//'+arquivos[i])

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
        
tabela = pd.DataFrame(retorno)
tabela.to_csv('tabela.csv')
