from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from xml.dom import minidom
from selenium.webdriver.remote.webelement import WebElement

driver = webdriver.Chrome() # cria instancia do WebDrive Chrome

# inicio do acesso a pagina
def acessarPagina():
    url = "http://plataforma.servicos.extranet.caixa/sso/"
    tituloPag = "Solução de Crédito Imobiliário – CIWEB"

    print("=== SPIDER PLATAFORMA SERVICOS v0.0.1 INICIANDO... ===")
    print("=== INICIANDO A INSTÂNCIA DO NAVEGADOR... ===")
    driver.maximize_window()
    print("=== NAVEGANDO ATÉ: " + url + " ===")
    driver.get(url) # navega ate uma certa pagina
    print("=== TÍTULO DA PÁGINA: " + tituloPag + " ===")
    assert tituloPag in driver.title # confirma o titulo da pagina

# inicio do login
def realizarLogin():
    nomeCampoUser = "strUsuario"
    nomeCampoSenha = "strSenha"
    user = "c106554"
    password = "8Milhoes"
    nomeBotaoTipoLogin = "btnOriginal"

    # campo usuario
    print("=== PROCURANDO CAMPO DE LOGIN... ===")
    elemInpUser = driver.find_element_by_name(nomeCampoUser) # procura e captura o campo de usuario
    elemInpUser.clear() # limpa o campo
    print("=== INSERINDO USER... ===")
    elemInpUser.send_keys(user) # envia os caracteres para serem inseridos
    elemInpUser.send_keys(Keys.TAB) # ativa a tecla TAB para passar para o proximo campo
    # campo senha
    print("=== PROCURANDO CAMPO DE SENHA... ===")
    elemInpPass = driver.find_element_by_name(nomeCampoSenha) # procura e captura o campo de senha
    elemInpPass.clear() # limpa o campo
    print("=== INSERINDO PASSWORD... ===")
    elemInpPass.send_keys(password) # envia os caracteres para serem inseridos
    elemInpPass.send_keys(Keys.ENTER) # ativa a tecla ENTER para logar
    print("=== LOGADO COM SUCESSO!!! ===")
    # selecao de login
    # print("=== ESPERANDO A PAGINA... ===")
    # print("=== SELECIONANDO TIPO DE LOGIN... ===")
    # elemBtnTipoLogin = driver.find_element_by_name(nomeBotaoTipoLogin) # procura e captura o botao de tipo de login
    # elemBtnTipoLogin.click() # clica no botao do tipo de login

# inicio da navegacao na pagina
def acessaPaginaIntegracao():
    urlMsgInt = "http://plataforma.servicos.extranet.caixa/plataforma-servicos/pages/auditoria/pesquisarAuditoriaMsgIntegracao.xhtml?faces-redirect=true"
    # entrando na pagina da MENSAGEM INTEGRACAO
    print("=== ESPERANDO A PAGINA... ===")
    print("=== INICIANDO A NAVEGACAO NA PAGINA... ===")
    driver.get(urlMsgInt) # navega ate uma certa pagina

# alterando filtros da pagina
def alteraFiltros():
    nomeComboServico = "formPesquisa-j_idt34-j_idt35-j_idt36-tipoOperacaoDetalhada"
    nomeCampoDataIni = "formPesquisa-j_idt34-j_idt73-j_idt88-dataEntradaInicio"
    nomeCampoDataFim = "formPesquisa-j_idt34-j_idt73-j_idt100-dataEntradaFinal"
    codServico = "22"
    dataIni = "01032019"
    dataFim = "31032019"
    idComboResultPag = "formPesquisa-j_idt34-j_idt114-dataTableObjetos_rppDD"
    itensPag = "100"

    print("=== ESPERANDO A PAGINA... ===")
    print("=== INICIANDO OPERACOES NA PAGINA... ===")
    print("=== PROCURANDO A COMBOBOX DOS SERVICOS... ===")
    elemComServ = Select(driver.find_element_by_name(nomeComboServico)) # procura e captura o ComboBox que contem os servicos
    print("=== SELECIONANDO O SERVICO ESCOLHIDO... ===")
    elemComServ.select_by_value(codServico) # seleciona um valor especifico
    print("=== SELECIONANDO UMA DATA DE INICIO... ===")
    elemInpDataIni = driver.find_element_by_name(nomeCampoDataIni) # procura e captura o campo de data inicio
    elemInpDataIni.send_keys(dataIni) # envia os caracteres para serem inseridos
    print("=== SELECIONANDO UMA DATA DE FIM... ===")
    elemInpDataFim = driver.find_element_by_name(nomeCampoDataFim) # procura e captura o campo de data fim
    elemInpDataFim.send_keys(dataFim) # envia os caracteres para serem inseridos
    # aumentando resultados na pagina
    print("=== AUMENTANDO RESULTADOS NA PAGINA... ===")
    elemComResultPag = Select(driver.find_element_by_id(idComboResultPag)) # procura e captura o ComboBox que altera a quantidade de resultados
    elemComResultPag.select_by_value(itensPag) # seleciona um valor especifico
    print("=== ESPERANDO A PAGINA... ===")

# clicando no botao de pesquisa
def clicaBotaoPesquisa():
    idBotaoPesquisar = "formPesquisa-j_idt25-j_idt29-botaoPesquisar"

    print("=== FILTROS AJUSTADOS, INICIANDO PESQUISA... ===")
    elemBtnPesquisar = WebDriverWait(driver, 1000).until(EC.element_to_be_clickable((By.ID, idBotaoPesquisar)))
    # elemBtnPesquisar = driver.find_element_by_id(idBotaoPesquisar) # procura e captura o botao de pesquisa
    elemBtnPesquisar.click() # clica no botao pesquisar
    print("=== ESPERANDO A PAGINA... ===")

def procuraPaginador():
    classTotPag = "ui-paginator-current"
    time.sleep(15)
    elemClassTotPag = WebDriverWait(driver, 1000).until(EC.element_to_be_clickable((By.CLASS_NAME, classTotPag)))
    pag = elemClassTotPag.text
    totPag = int(pag[45:51])
    return totPag

def cliques():
    idCampoCodNeg = "formPesquisa-j_idt34-j_idt73-j_idt74-codigoNegocio"

    # clica em um ponto especifico fora da div para que ela desapareca
    action = webdriver.common.action_chains.ActionChains(driver)
    elemInpCodNeg = driver.find_element_by_id(idCampoCodNeg) # procura e captura o campo do cod neg
    action.move_to_element_with_offset(elemInpCodNeg, -10, -100)
    print("=== CLICANDO no CODNEG... ===")
    action.click().perform()
    elemBtnMsgInt = driver.find_element_by_id('a-mensagem-integracao-1024')
    action.move_to_element_with_offset(elemBtnMsgInt, -10, -100)
    print("=== CLICANDO no MENSAGEM INTEGRACAO... ===")
    action.click().perform()
    elemBtnIni = driver.find_element_by_id('a-inicio-1016')
    action.move_to_element_with_offset(elemBtnIni, -10, -100)
    print("=== CLICANDO no INICIO... ===")
    action.click().perform()
    action.move_to_element_with_offset(elemInpCodNeg, -5, -10)
    action.click().perform()
    elemBtnMsgInt = driver.find_element_by_id('a-mensagem-integracao-1024')
    action.move_to_element_with_offset(elemBtnMsgInt, -5, -10)
    action.click().perform()
    elemBtnIni = driver.find_element_by_id('a-inicio-1016')
    action.move_to_element_with_offset(elemBtnIni, -5, -10)
    action.click().perform()                            

# inicio das operacoes com a saida xml
def iniciaOperacoesSaida(totPag):
    classPag = "ui-paginator-page ui-state-default ui-corner-all"
    nomeArquivoCsv = 'file_name.csv'
    colunas = ["Data de Referencia da Consulta"
                    , "Identificacao do Contrato"
                    , "Digito do Contrato"
                    , "Identificacao da Pessoa Principal"
                    , "Nome Principal"
                    , "Cidade"
                    , "UF"
                    , "Dia de Nascimento"
                    , "Mes de Nascimento"
                    , "Ano de Nascimento"
                    , "Canal do Solicitante"]
    
    dfDates = pd.DataFrame(index=None)
    df = pd.DataFrame(index=None)
    lista = None
    j = '0'
    aux = 0
    idBotaoSaidaXml = "formPesquisa-j_idt34-j_idt114-dataTableObjetos-"+j+"-imgConteudoSaidaXml"
    idDivSaidaXML = "formPesquisa-j_idt34-j_idt114-dataTableObjetos-"+j+"-j_idt134" 

    # abrindo saida XML
    try:
        for p in range(totPag):
            if p != 0:
                elemClassPag = driver.find_element_by_xpath("//span[text()='"+str(p+1)+"']")
                elemClassPag.click()
                print("=== PAGINA ATUAL: "+str(p+1)+" ===")
            for i in range(10):
                elemBtnSaidaXml = WebDriverWait(driver, 10000).until(EC.presence_of_element_located((By.ID, idBotaoSaidaXml))) # esperando que o elemento esteja disponivel
                print("=== PROCURANDO BOTAO DE SAIDA XML... ===")
                elemBtnSaidaXml.click() # clica no botao de saida do xml
                print("=== ESPERANDO A PAGINA... ===")
                elemDivSaidaXml = WebDriverWait(driver, 10000).until(EC.presence_of_element_located((By.ID, idDivSaidaXML))) # esperando que o elemento esteja disponivel
                # capturando saida xml
                print("=== CAPTURANDO TEXTO DE SAIDA XML... ===")
                elemDivSaidaXml = driver.find_element_by_id(idDivSaidaXML) # procura a div que contem a saida
                saidaxml = elemDivSaidaXml.text # captura o texto contido
                print("=== TEXTO CAPTURADO: \n" + saidaxml + " ===")
                
                print("=== CLICANDO... ===")
                cliques()
                print("=== CLICANDO... ===")
                cliques()
               
                aux = aux + 1
                j = j.replace(j, str(aux))
                idBotaoSaidaXml = "formPesquisa-j_idt34-j_idt114-dataTableObjetos-"+j+"-imgConteudoSaidaXml"
                idDivSaidaXML = "formPesquisa-j_idt34-j_idt114-dataTableObjetos-"+j+"-j_idt134"
                print("=== BOTAO XML ATUAL: "+j+" ===")

                # tratando saida recebida
                # extraindo as informacoes necessarias
                if (saidaxml[3:8] != 'Fault'):
                    xmldoc = minidom.parseString(saidaxml)
                    dataReferenciaConsulta = xmldoc.getElementsByTagName('dataReferenciaConsulta')[0].firstChild.nodeValue
                    identificacaoContrato = xmldoc.getElementsByTagName('identificacaoContrato')[0].firstChild.nodeValue
                    digitoContrato = xmldoc.getElementsByTagName('digitoContrato')[0].firstChild.nodeValue
                    identificacaoPessoaPrincipal = xmldoc.getElementsByTagName('identificacaoPessoaPrincipal')[0].firstChild.nodeValue
                    nomePrincipal = xmldoc.getElementsByTagName('nomePrincipal')[0].firstChild.nodeValue
                    nomePrincipal = nomePrincipal.strip()
                    cidade = xmldoc.getElementsByTagName('cidade')[0].firstChild.nodeValue
                    uf = xmldoc.getElementsByTagName('uf')[0].firstChild.nodeValue
                    diaNascimento = xmldoc.getElementsByTagName('diaNascimento')[0].firstChild.nodeValue
                    mesNascimento = xmldoc.getElementsByTagName('mesNascimento')[0].firstChild.nodeValue
                    anoNascimento = xmldoc.getElementsByTagName('anoNascimento')[0].firstChild.nodeValue
                    canalSolicitante = xmldoc.getElementsByTagName('canalSolicitante')[0].firstChild.nodeValue
                    #criando um arquivo CSV para a saida do processamento
                    lista = [dataReferenciaConsulta
                        , identificacaoContrato
                        , digitoContrato
                        , identificacaoPessoaPrincipal
                        , nomePrincipal
                        , cidade
                        , uf
                        , diaNascimento
                        , mesNascimento
                        , anoNascimento
                        , canalSolicitante]
                                
                    dfDates = dfDates.append([lista], ignore_index=True)
                    print(dfDates)
                    lista = None
    except Exception as e:
        print("Ocorreu algum erro na execucao! " + str(e))
    finally:
        dfDates.columns = [colunas]
        df = dfDates
        print(df)

        df.to_csv(nomeArquivoCsv, sep=';', encoding='utf-8', index=False)

def encerraOperacoes():
    driver.close()
    driver.quit()

acessarPagina()
realizarLogin()
acessaPaginaIntegracao()
alteraFiltros()
clicaBotaoPesquisa()
totPag = procuraPaginador()
iniciaOperacoesSaida(totPag)

# fechando navegador
encerraOperacoes()
