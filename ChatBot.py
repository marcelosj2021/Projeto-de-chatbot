from time import sleep
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions

chrome = webdriver.Chrome(executable_path=r'./chromedriver.exe')
chrome.get('https://web.whatsapp.com/')

def is_exist(c, str):
    try:
        c.find_element(By.CLASS_NAME, str)
        return True
    except selenium.common.exceptions.NoSuchElementException:
        return False

SearchBox = '//*[@id="main"]/footer/div[1]/div/div/div[2]/div[1]/div/div[2]'
SendButton = '//*[@id="main"]/footer/div[1]/div/div/div[2]/div[2]/button'

# Captura o nome do usuário.
# Fica no laço até encontrar o círculo com a img do perfil. Isso evita que o programa de erro na etapa de autenticação pelo QRCode.  
while True: 
        try:    
            WebDriverWait(chrome, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/header/div[1]/div/img')))                                                                       
            break
        except selenium.common.exceptions.TimeoutException:
            sleep(5)
print(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), 'Whatsapp identificado.')
chrome.find_element(By.XPATH, '//*[@id="side"]/header/div[1]/div/img').click()
sleep(5)

try:
    # Extrai o nome do usuário no whatsapp business
    user = chrome.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[1]/div[2]/div[1]/span/div[1]/span/div[1]/div/div[2]/div[1]/div[1]/div[2]/div/div[1]').text                                
except:
    # Extrai o nome do usuário no whatsapp
    user = chrome.find_element(By.CLASS_NAME,'_13NKt').text
finally:

    chrome.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[2]/div[1]/span/div[1]/span/div[1]/header/div/div[1]/button').click()                              
    print(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), 'Nome do usuário capturado.') 
    print(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), 'Procurando conversa não lida.')
    telefone = ''

while True: 

    # Lista de conversas.
    # Fica no laço até encontrar a lista de conversa. Isso evita que o programa de erro caso não tenha nenhuma conversa.
    while True:
        try:
            WebDriverWait(chrome, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="pane-side"]/div[1]/div/div')))
            break
        except selenium.common.exceptions.TimeoutException:
            sleep(5)

    lc = chrome.find_element(By.XPATH, '//*[@id="pane-side"]/div[1]/div/div').find_elements(By.CLASS_NAME, '_3m_Xw')
   
    # Lista de conversas organizada
    lco = []

    # Organiza lista de conversas
    max = 0
    for c in lc:

        lco.append(c)
        if max == 11: 
            break
        max=max+1

    lco.reverse() 
    
    # Seleciona uma conversa por vez da lista de conversas organizada
    for c in lco:
        
        # Verifica se é uma mensagem que não foi lida
        if is_exist(c,'_1pJ9J'):
            span = c.find_element(By.CLASS_NAME, '_ccCW')
            telefone = span.get_attribute('title')
            print(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), 'Encontrou uma mensagem não lida do', span.get_attribute('title'))

            c.click()

            # Fica no laço até encontrar uma mensagem não lida de outro usuário na lista de conversas.
            while True:
                # Pega as mensagens de uma conversa
                lm = chrome.find_element(By.CLASS_NAME, 'y8WcF').find_elements(By.CLASS_NAME, '_2wUmf')

                UltimaMsgRobo = ''
                UltimaMsgCliente = ''
                exit = False
                x = False
                
                TemAnimalDomestico = ''
                QtdePessoasLocacao = 0
                QtdeCriancas = 0
                QtdePessoasAutonomas = 0
                QtdePessoasAssalariadas = 0
                BarulhoExcessivo = ''
                ClientName = ''
                
                for m in lm:
                    if is_exist(m,'copyable-text'):                          
                        emissor = m.find_element(By.CLASS_NAME,'copyable-text').get_attribute('data-pre-plain-text')
                        texto = m.find_element(By.CLASS_NAME,'i0jNr').text

                        if user in emissor:
                            UltimaMsgRobo = texto
                            UltimaMsgCliente = ''
                            x = True
                        else:
                            if x:
                                UltimaMsgCliente = texto

                                # Armazena as respostas do usuário nas variáveis
                                if UltimaMsgRobo == 'Você possui animal doméstico? Digite somente SIM ou NÃO.':
                                    TemAnimalDomestico = UltimaMsgCliente
                                elif UltimaMsgRobo == 'A locação seria para quantas pessoas? Digite somente o número.':
                                    QtdePessoasLocacao = UltimaMsgCliente 
                                elif UltimaMsgRobo == 'Quantas são crianças? Digite somente o número e caso não tenha, digite o número zero.':
                                    QtdeCriancas = UltimaMsgCliente
                                elif UltimaMsgRobo == 'Quantas pessoas tem emprego fixo ou são aposentadas ou são pensionistas? Digite somente o número e caso não tenha, digite o número zero.':
                                    QtdePessoasAssalariadas = UltimaMsgCliente
                                elif UltimaMsgRobo == 'Barulho excessivo no imóvel, a qualquer horário do dia, é proibido. Você está de acordo? Digite somente SIM ou NÃO.':
                                    BarulhoExcessivo = UltimaMsgCliente
                                elif UltimaMsgRobo == 'Qual é seu nome?':
                                    ClientName = UltimaMsgCliente
                                    
                                if UltimaMsgCliente != "": 
                                    x = False

                if UltimaMsgRobo == 'Você possui animal doméstico? Digite somente SIM ou NÃO.' and UltimaMsgCliente != '':
                    if 'NÃO' in UltimaMsgCliente.upper() or 'NAO' in UltimaMsgCliente.upper():
                        c.find_element(By.XPATH, SearchBox).send_keys('A locação seria para quantas pessoas? Digite somente o número.')
                        c.find_element(By.XPATH, SendButton).click()                            
                    elif 'SIM' in UltimaMsgCliente.upper():
                        c.find_element(By.XPATH, SearchBox).send_keys('Lamento, seu perfil não é compatível para fazer a locação do imóvel. Agradecemos seu contato.')
                        c.find_element(By.XPATH, SendButton).click()                        
                    else:
                        UltimaMsgCliente = ''
                        c.find_element(By.XPATH, SearchBox).send_keys('Não entendi.')
                        c.find_element(By.XPATH, SendButton).click()                            
                        c.find_element(By.XPATH, SearchBox).send_keys(UltimaMsgRobo)
                        c.find_element(By.XPATH, SendButton).click()

                elif UltimaMsgRobo == 'A locação seria para quantas pessoas? Digite somente o número.' and UltimaMsgCliente != '':
                    try:
                        num = int(UltimaMsgCliente)
                        if num <= 5:
                            c.find_element(By.XPATH, SearchBox).send_keys('Quantas são crianças? Digite somente o número e caso não tenha, digite o número zero.')
                            c.find_element(By.XPATH, SendButton).click()                            
                        else:
                            c.find_element(By.XPATH, SearchBox).send_keys('Lamento, seu perfil não é compatível para fazer a locação do imóvel. Agradecemos seu contato.')
                            c.find_element(By.XPATH, SendButton).click() 
                            
                    except ValueError:
                        UltimaMsgCliente = ''
                        c.find_element(By.XPATH, SearchBox).send_keys('Não entendi.')
                        c.find_element(By.XPATH, SendButton).click()
                            
                        c.find_element(By.XPATH, SearchBox).send_keys(UltimaMsgRobo)
                        c.find_element(By.XPATH, SendButton).click()
                                        
                elif UltimaMsgRobo == 'Quantas são crianças? Digite somente o número e caso não tenha, digite o número zero.' and UltimaMsgCliente != '': 
                    try:
                        num = int(UltimaMsgCliente)
                        if num <=2:
                            c.find_element(By.XPATH, SearchBox).send_keys('Quantas pessoas tem emprego fixo ou são aposentadas ou são pensionistas? Digite somente o número e caso não tenha, digite o número zero.')
                            c.find_element(By.XPATH, SendButton).click()                           
                        else:
                            c.find_element(By.XPATH, SearchBox).send_keys('Lamento, seu perfil não é compatível para fazer a locação do imóvel. Agradecemos seu contato.')
                            c.find_element(By.XPATH, SendButton).click()
                                
                    except ValueError:
                        UltimaMsgCliente = ''
                        c.find_element(By.XPATH, SearchBox).send_keys('Não entendi.')
                        c.find_element(By.XPATH, SendButton).click()                           
                        c.find_element(By.XPATH, SearchBox).send_keys(UltimaMsgRobo)
                        c.find_element(By.XPATH, SendButton).click()
                                
                elif UltimaMsgRobo == 'Quantas pessoas tem emprego fixo ou são aposentadas ou são pensionistas? Digite somente o número e caso não tenha, digite o número zero.' and UltimaMsgCliente != '':
                    try:
                        num = int(UltimaMsgCliente)
                        if (int(QtdePessoasLocacao) >= 4 and num >=2) or (int(QtdePessoasLocacao) < 4 and num >=1):
                            c.find_element(By.XPATH, SearchBox).send_keys('Barulho excessivo no imóvel, a qualquer horário do dia, é proibido. Você está de acordo? Digite somente SIM ou NÃO.')
                            c.find_element(By.XPATH, SendButton).click()                                 
                        else:
                            c.find_element(By.XPATH, SearchBox).send_keys('Lamento, seu perfil não é compatível para fazer a locação do imóvel. Agradecemos seu contato.')
                            c.find_element(By.XPATH, SendButton).click()
                            
                    except ValueError:
                        UltimaMsgCliente = ''
                        c.find_element(By.XPATH, SearchBox).send_keys('Não entendi.')
                        c.find_element(By.XPATH, SendButton).click()                         
                        c.find_element(By.XPATH, SearchBox).send_keys(UltimaMsgRobo)
                        c.find_element(By.XPATH, SendButton).click()

                elif UltimaMsgRobo == 'Barulho excessivo no imóvel, a qualquer horário do dia, é proibido. Você está de acordo? Digite somente SIM ou NÃO.' and UltimaMsgCliente != '':
                    if 'SIM' in UltimaMsgCliente.upper():
                        r = UltimaMsgCliente
                        c.find_element(By.XPATH, SearchBox).send_keys('Qual é seu nome?')
                        c.find_element(By.XPATH, SendButton).click()                      
                    elif 'NÃO' in UltimaMsgCliente.upper() or 'NAO' in UltimaMsgCliente.upper():
                        c.find_element(By.XPATH, SearchBox).send_keys('Lamento, seu perfil não é compatível para fazer a locação do imóvel. Agradecemos seu contato.')
                        c.find_element(By.XPATH, SendButton).click()                    
                    else:
                        UltimaMsgCliente = ''
                        c.find_element(By.XPATH, SearchBox).send_keys('Não entendi.')
                        c.find_element(By.XPATH, SendButton).click()                          
                        c.find_element(By.XPATH, SearchBox).send_keys(UltimaMsgRobo)
                        c.find_element(By.XPATH, SendButton).click()
                        
                elif UltimaMsgRobo == 'Qual é seu nome?' and UltimaMsgCliente != '':
                    c.find_element(By.XPATH, SearchBox).send_keys('Retornaremos seu contato em breve para agendar uma visita e esclarecer qualquer dúvida que tenha sobre o imóvel e a locação.')
                    c.find_element(By.XPATH, SendButton).click()
                    
                elif UltimaMsgRobo == 'Retornaremos seu contato em breve para agendar uma visita e esclarecer qualquer dúvida que tenha sobre o imóvel e a locação.':
                        c.find_element(By.XPATH, SearchBox).send_keys('Obrigado!')
                        c.find_element(By.XPATH, SendButton).click()

                        c.find_element(By.XPATH, SearchBox).send_keys(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                        c.find_element(By.XPATH, SearchBox).send_keys(Keys.SHIFT + Keys.ENTER)
                        c.find_element(By.XPATH, SearchBox).send_keys('1) Tem animal: ', str(TemAnimalDomestico))
                        c.find_element(By.XPATH, SearchBox).send_keys(Keys.SHIFT + Keys.ENTER)
                        c.find_element(By.XPATH, SearchBox).send_keys('2) Quantas pessoas: ', str(QtdePessoasLocacao))
                        c.find_element(By.XPATH, SearchBox).send_keys(Keys.SHIFT + Keys.ENTER)
                        c.find_element(By.XPATH, SearchBox).send_keys('3) Quantas crianças: ', str(QtdeCriancas))
                        c.find_element(By.XPATH, SearchBox).send_keys(Keys.SHIFT + Keys.ENTER)
                        c.find_element(By.XPATH, SearchBox).send_keys('4) Quantos assalariado/aposentado/pensionista: ', str(QtdePessoasAssalariadas))
                        c.find_element(By.XPATH, SearchBox).send_keys(Keys.SHIFT + Keys.ENTER)
                        c.find_element(By.XPATH, SearchBox).send_keys('5) Concordo com o silêncio: ', str(BarulhoExcessivo))
                        c.find_element(By.XPATH, SearchBox).send_keys(Keys.SHIFT + Keys.ENTER)
                        c.find_element(By.XPATH, SearchBox).send_keys('6) Nome do interessado: ', str(ClientName))
                        c.find_element(By.XPATH, SearchBox).send_keys(Keys.SHIFT + Keys.ENTER)
                        c.find_element(By.XPATH, SearchBox).send_keys('7) Telefone: ', str(telefone))
                        c.find_element(By.XPATH, SendButton).click()
                        sleep(1)

                elif (UltimaMsgRobo == '') or UltimaMsgRobo == 'Lamento, seu perfil não é compatível para fazer a locação do imóvel. Agradecemos seu contato.'  or UltimaMsgRobo == 'Retornaremos seu contato em breve para agendar uma visita e esclarecer qualquer dúvida que tenha sobre o imóvel e a locação.' or "Tem animal:" in UltimaMsgRobo:
                    c.find_element(By.XPATH, SearchBox).send_keys('Olá, tudo bem? Bem-vindo ao canal de atendimento via WhatsApp. Eu sou um ChatBot e estou aqui para ajudar você.')                        
                    c.find_element(By.XPATH, SendButton).click()
                    c.find_element(By.XPATH, SearchBox).send_keys('Notei que você tem interesse em locar nosso imóvel.')  
                    c.find_element(By.XPATH, SendButton).click()
                    c.find_element(By.XPATH, SearchBox).send_keys('Você possui animal doméstico? Digite somente SIM ou NÃO.')  
                    c.find_element(By.XPATH, SendButton).click()
                                    
                # Lista de conversas
                lc2 = chrome.find_element(By.XPATH, '//*[@id="pane-side"]/div[1]/div/div').find_elements(By.CLASS_NAME, '_3m_Xw')
            
                # Lista de conversas organizada
                lco2 = []

                # Organiza lista de conversas
                max2 = 0

                for c2 in lc2:
                    lco2.append(c2)
                    if max2 == 11: 
                        break
                    max2=max2+1

                lco2.reverse() 
                
                # Seleciona uma conversa por vez da lista de conversas organizada
                for c2 in lco2:
                    # Verifica se é uma mensagem que não foi lida
                    if is_exist(c2,'_1pJ9J'):
                        exit = True
                        break

                if exit: 
                    break
                

