# necessário rodar com jupyter
import os as system
import untangle as xml
import pandas as pd

comp = ""
arquivos = []
resultado = []

# acessa a o diretório xml
diretorio_xml = 'C://Users//Leonardo//Desktop//xml//'
for entry in system.scandir(path=diretorio_xml):
    if not entry.name.startswith('.') and entry.is_file():
        arquivos.append(entry.name)

# gerando a competencia do arquivos
for arquivo in arquivos:
    # acessando o diretório e os arquivos
    xml_path = system.path.join(diretorio_xml, arquivo)
    # associando para a blibloteca untangle
    nfse = xml.parse(xml_path)

    try:
        # usando a bliblioteca untangle
        # dei uma olhada em outras blibliotecas e algumas foram descontinuadas
        competencia = nfse.CompNfse.Nfse.InfNfse.Competencia.cdata[0:7]
        valorServicos = float(nfse.CompNfse.Nfse.InfNfse.Servico.Valores.ValorServicos.cdata)
        valorIss = float(nfse.CompNfse.Nfse.InfNfse.Servico.Valores.ValorIss.cdata)
        valorIssRetido = float(nfse.CompNfse.Nfse.InfNfse.Servico.Valores.ValorIssRetido.cdata)
        baseCalculo = float(nfse.CompNfse.Nfse.InfNfse.Servico.Valores.BaseCalculo.cdata)
        valorLiquidoNfse = float(nfse.CompNfse.Nfse.InfNfse.Servico.Valores.ValorLiquidoNfse.cdata)

    except AttributeError:
        # quando cai no expect
        # são alguns arquivos que não tem as tags necessárias para continuação
        # passando o valor de zero para tags inexistentes
        valorServicos = float(nfse.CompNfse.Nfse.InfNfse.Servico.Valores.ValorServicos.cdata)
        valorIss = 0
        valorIssRetido = 0
        baseCalculo = float(nfse.CompNfse.Nfse.InfNfse.Servico.Valores.BaseCalculo.cdata)
        valorLiquidoNfse = float(nfse.CompNfse.Nfse.InfNfse.Servico.Valores.ValorLiquidoNfse.cdata)

        continue

    finally:
        
        if comp == competencia:
            # para competências iguais
            resultado_anterior = resultado[-1]
            valorServicos += (resultado_anterior["ValorServicos"])
            valorIss += (resultado_anterior["ValorIss"])
            valorIssRetido += (resultado_anterior["ValorIssRetido"])
            baseCalculo += (resultado_anterior["BaseCalculo"])
            valorLiquidoNfse += (resultado_anterior["ValorLiquidoNfse"])
            
            resultado.pop()

        else:
            comp = competencia
        
        resultado.append({
            'Competencia' : comp,
            'ValorServicos': valorServicos,
            'ValorIss': valorIss,
            'ValorIssRetido': valorIssRetido,
            'BaseCalculo': baseCalculo,
            'ValorLiquidoNfse': valorLiquidoNfse,
        })
        

# usando o panda + jupyter para imprimir no formato CSV
tabela = pd.DataFrame(resultado)
arquivo_csv = 'C://Users//Leonardo//Desktop//tabela.csv'
# removendo a coluna de index
tabela.to_csv(arquivo_csv, index=False)
# display usando o jupyter
display(tabela)
