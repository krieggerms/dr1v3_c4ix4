import time
from xml.dom import minidom

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

driver = webdriver.Chrome() # cria instancia do WebDrive Chrome
action = webdriver.common.action_chains.ActionChains(driver)

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
    password = "10Milhoes"
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
def alteraFiltros(codNeg):
    nomeComboServico = "formPesquisa-j_idt34-j_idt35-j_idt36-tipoOperacaoDetalhada"
    nomeComboValidacao = "formPesquisa-j_idt34-j_idt35-j_idt62-indicadorValidacao"
    idCampoCodNeg = "formPesquisa-j_idt34-j_idt73-j_idt74-codigoNegocio"
    codServico = "22"
    codValidacao = "1"

    print("=== ESPERANDO A PAGINA... ===")
    print("=== INICIANDO OPERACOES NA PAGINA... ===")
    print("=== PROCURANDO A COMBOBOX DOS SERVICOS... ===")
    elemComServ = Select(driver.find_element_by_name(nomeComboServico)) # procura e captura o ComboBox que contem os servicos
    print("=== SELECIONANDO O SERVICO ESCOLHIDO... ===")
    elemComServ.select_by_value(codServico) # seleciona um valor especifico
    print("=== PROCURANDO A COMBOBOX DE VALIDACAO... ===")
    elemComVal = Select(driver.find_element_by_name(nomeComboValidacao)) # procura e captura o ComboBox que contem as validacoes
    print("=== SELECIONANDO A VALIDACAO ESCOLHIDA... ===")
    elemComVal.select_by_value(codValidacao) # seleciona um valor especifico
    print("=== SELECIONANDO O CODIGO DE NEGOCIO ESCOLHIDO: "+str(codNeg)+"... ===")
    elemInpCodNeg = driver.find_element_by_id(idCampoCodNeg) # procura e captura o campo do cod neg
    elemInpCodNeg.clear() # limpa o campo
    elemInpCodNeg.send_keys(str(codNeg)) # envia os caracteres para serem inseridos

# clicando no botao de pesquisa
def clicaBotaoPesquisa():
    idBotaoPesquisar = "formPesquisa-j_idt25-j_idt29-botaoPesquisar"
    idComboResultPag = "formPesquisa-j_idt34-j_idt114-dataTableObjetos_rppDD"
    itensPag = "100"

    action.send_keys(Keys.CONTROL + Keys.HOME)
    action.perform()
    time.sleep(1)
    action.send_keys(Keys.CONTROL + Keys.HOME)
    action.perform()
    time.sleep(1)
    action.send_keys(Keys.CONTROL + Keys.HOME)
    action.perform()
    time.sleep(1)

    print("=== FILTROS AJUSTADOS, INICIANDO PESQUISA... ===")
    elemBtnPesquisar = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.ID, idBotaoPesquisar)))
    elemBtnPesquisar.click() # clica no botao pesquisar
    print("=== ESPERANDO A PAGINA... ===")
    # aumentando resultados na pagina
    print("=== AUMENTANDO RESULTADOS NA PAGINA... ===")
    elemComResultPag = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.ID, idComboResultPag)))
    elemComResultPag = Select(driver.find_element_by_id(idComboResultPag)) # procura e captura o ComboBox que altera a quantidade de resultados
    elemComResultPag.select_by_value(itensPag) # seleciona um valor especifico
    time.sleep(7)
    print("=== ESPERANDO A PAGINA... ===")

def procuraPaginador():
    classTotPag = "ui-paginator-current"
    time.sleep(10)
    elemClassTotPag = WebDriverWait(driver, 1000).until(EC.element_to_be_clickable((By.CLASS_NAME, classTotPag)))
    pag = elemClassTotPag.text
    numeros = [int(s) for s in pag.split() if s.isdigit()]
    return numeros

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

def leArquivoCsvCodNeg():
    print("=== INICIANDO A LEITURA DO ARQUIVO CSV COM OS COD DE NEGOCIO... ===")
    df = pd.read_csv('historico_atendimento_03-03_09-03.csv', encoding = "ISO-8859-1")
    #df = pd.read_csv('historico_atendimento_10-03_16-03.csv', encoding = "ISO-8859-1")
    print(df)
    print("=== LEITURA CONCLUIDA, REMOVENDO DUPLICATAS... ===")
    df_clean = df.drop_duplicates(subset=['Cód. Negócio'])
    return df_clean

# inicio das operacoes com a saida xml
def iniciaOperacoesSaida(csvCodNeg):
    classPag = "ui-paginator-page ui-state-default ui-corner-all"
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
    tamanhoArquivoCsv = len(csvCodNeg)
    codNeg = None
    listCodNeg = ['1078647542', '123610117', '96902175004', '35751923839', '3404115031', '10985087773', '19464096187', '32233054830'
                    , '41407617842', '15295253813', '69501033520', '80959490191', '93309058034', '40341412805', '33408554803'
                    , '87871360906', '2751986420', '90871227053', '2637302399', '26758238806', '27432937800', '32353884865'
                    , '2507823836', '4472579600', '7313035802', '37569820843', '96144149520', '6176870488', '2947577590'
                    , '1394838026', '4838481900', '221654526', '5293909657', '12485749744', '46916527870', '71781374104'
                    , '5150826430', '44290746829', '2087113173', '3724658974', '22597946886', '30364549858', '80763138053'
                    , '2081867940', '58338527068', '25685256817', '35891176807', '32248602863', '24900674869', '44567707400'
                    , '43230393104', '2403830100', '255961790', '36015850817', '2501113144', '8091855800', '32247180809'
                    , '35966211', '7388091955', '7659278967', '7734705731', '42138191249', '10014868709', '35397529869'
                    , '2350223493', '28495699842', '28517508874', '23218752833', '41488082839', '1150170204', '33229656865'
                    , '6346045628', '70044086121', '84026430510', '66202930500', '50513230149', '4432893796', '29000086892'
                    , '67955703391', '37152582840']

    # abrindo saida XML
    try:
        for row in range(tamanhoArquivoCsv):
            if codNeg != None and str(codNeg) not in listCodNeg:
                dfDates.columns = [colunas]
                df = dfDates
                print(df)
                df.to_csv(nomeArquivoCsv, sep=';', encoding='utf-8', index=False)
                listCodNeg += str(codNeg)
            
            dfDates = pd.DataFrame(index=None)
            df = pd.DataFrame(index=None)
            codNeg = csvCodNeg['Cód. Negócio'][row]
            if str(codNeg) not in listCodNeg:
                nomeArquivoCsv = 'itens_'+str(codNeg)+'.csv'
                i = 0
                j = '0'
                aux = 0
                action = webdriver.common.action_chains.ActionChains(driver)
                action.send_keys(Keys.CONTROL + Keys.HOME)
                action.perform()
                time.sleep(1)
                action.send_keys(Keys.CONTROL + Keys.HOME)
                action.perform()
                time.sleep(1)
                action.send_keys(Keys.CONTROL + Keys.HOME)
                action.perform()
                time.sleep(1)
                action.send_keys(Keys.CONTROL + Keys.HOME)
                action.perform()
                time.sleep(1)
                alteraFiltros(codNeg)
                time.sleep(1)
                clicaBotaoPesquisa()
                time.sleep(5)
                numeros = procuraPaginador()
                totPag = numeros[2]
                totItens = numeros[0]
                for p in range(totPag):
                    if p != 0:
                        elemClassPag = driver.find_element_by_xpath("//span[text()='"+str(p+1)+"']")
                        elemClassPag.click()
                        time.sleep(1)
                        print("=== PAGINA ATUAL: "+str(p+1)+" ===")
                        totItens = a
                        action.send_keys(Keys.CONTROL + Keys.HOME)
                        action.perform()
                    p = p + 1
                    if totItens > 100:
                        a = totItens - 100
                        totItens = 100
                        action.send_keys(Keys.CONTROL + Keys.HOME)
                        action.perform()
                    for i in range(totItens):
                        time.sleep(1)
                        action.send_keys(Keys.CONTROL + Keys.HOME)
                        action.perform()
                        time.sleep(1)
                        elemBtnSaidaXml = WebDriverWait(driver, 100000).until(EC.presence_of_element_located((By.ID, idBotaoSaidaXml))) # esperando que o elemento esteja disponivel
                        time.sleep(5)
                        print("=== PROCURANDO BOTAO DE SAIDA XML... ===")
                        elemBtnSaidaXml.click() # clica no botao de saida do xml
                        print("=== ESPERANDO A PAGINA... ===")
                        time.sleep(2)
                        elemDivSaidaXml = WebDriverWait(driver, 10000).until(EC.presence_of_element_located((By.ID, idDivSaidaXML))) # esperando que o elemento esteja disponivel
                        # capturando saida xml
                        print("=== CAPTURANDO TEXTO DE SAIDA XML... ===")
                        elemDivSaidaXml = driver.find_element_by_id(idDivSaidaXML) # procura a div que contem a saida
                        saidaxml = elemDivSaidaXml.text # captura o texto contido
                        print("=== TEXTO CAPTURADO: \n" + saidaxml + " ===")
                        
                        print("=== CLICANDO... ===")
                        cliques()
                        time.sleep(1)
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
                        if i == totItens:
                            break
    except Exception as e:
        print("Ocorreu algum erro na execucao! " + str(e))
    finally:
        print("=== FINALIZADOS: "+str(listCodNeg)+" ===")
    #    dfDates.columns = [colunas]
    #    df = dfDates
    #    print(df)
    #    df.to_csv(nomeArquivoCsv, sep=';', encoding='utf-8', index=False)

def encerraOperacoes():
    driver.close()
    driver.quit()

acessarPagina()
realizarLogin()
acessaPaginaIntegracao()
csvCodNeg = leArquivoCsvCodNeg()
print(csvCodNeg)
iniciaOperacoesSaida(csvCodNeg)

# fechando navegador
encerraOperacoes()
