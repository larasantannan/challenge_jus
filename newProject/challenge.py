from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)

# Rota inicial.
@app.route('/')
def index():
    return render_template('home.html')

# Rota para exibir os dados do processo.
@app.route('/contents', methods=['POST'])
def contents():

    # Variáveis que recebem os valores referente ao nome do tribunal e número do processo.
    court = request.form['court']
    process = request.form['processNumber']

    # Variáveis para tratamento das entradas e processamento dos valores de entrada para realização do crawler.
    first_part_process = ''
    second_part_process = ''

    x = process.split('.')

    first_part_process = x[0] + '.' + x[1]
    second_part_process = x[len(x) - 1]

    # ChromeOptions utilizado para evitar que o browser seja aberto durante o processo de crawler.
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')

    # Início do processo de crawler com a definição da fonte que será crawleada.
    if court == "TJSP":
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get("https://esaj.tjsp.jus.br/cpopg/open.do")
    else:
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get("https://esaj.tjms.jus.br/cpopg5/open.do")

       
    # Processo de busca dos dados.
    element = driver.find_element_by_name("numeroDigitoAnoUnificado")
    element.send_keys(first_part_process)
    second_element = driver.find_element_by_name("foroNumeroUnificado")
    second_element.send_keys(second_part_process)

    button = driver.find_element_by_xpath('//*[@id="pbEnviar"]')
    button.click()

    show_all_process_data = driver.find_element_by_xpath('//*[@id="linkpartes"]')
    show_all_process_data.click()

    show_all_moves = driver.find_element_by_xpath('//*[@id="linkmovimentacoes"]')
    show_all_moves.click()

    class_process = driver.find_element_by_xpath('/html/body/div/table[4]/tbody/tr/td/div[1]/table[2]/tbody/tr[2]/td[2]/table/tbody/tr/td/span[1]/span')
    area = driver.find_element_by_xpath('/html/body/div/table[4]/tbody/tr/td/div[1]/table[2]/tbody/tr[3]/td[2]/table/tbody/tr/td')
    subject = driver.find_element_by_xpath('/html/body/div/table[4]/tbody/tr/td/div[1]/table[2]/tbody/tr[4]/td[2]/span')
    
    if court == 'TJMS':
        value = driver.find_element_by_xpath('/html/body/div/table[4]/tbody/tr/td/div[1]/table[2]/tbody/tr[9]/td[2]/span')
        judge = driver.find_element_by_xpath('/html/body/div/table[4]/tbody/tr/td/div[1]/table[2]/tbody/tr[8]/td[2]/span')
        distribution = driver.find_element_by_xpath('/html/body/div/table[4]/tbody/tr/td/div[1]/table[2]/tbody/tr[5]/td[2]/span')
    else:
        distribution = driver.find_element_by_xpath('/html/body/div/table[4]/tbody/tr/td/div[1]/table[2]/tbody/tr[6]/td[2]/span')
        value = driver.find_element_by_xpath('/html/body/div/table[4]/tbody/tr/td/div[1]/table[2]/tbody/tr[10]/td[2]/span')
        judge = driver.find_element_by_xpath('/html/body/div/table[4]/tbody/tr/td/div[1]/table[2]/tbody/tr[9]/td[2]/span')
    

    process_data = driver.find_elements_by_xpath('//*[@id="tableTodasPartes"]')
    move_data = driver.find_elements_by_xpath('//*[@id="tabelaTodasMovimentacoes"]')

    # Início do processo de render do template com a passagem dos parâmetros que serão exibidos na tela.
    return render_template('contents.html', 
        class_process=class_process.text, 
        processNumber=process, 
        area=area.text,
        subject=subject.text,
        distribution=distribution.text,
        value=value.text,
        judge=judge.text,
        links=process_data,
        movimentacoes=move_data,
        court=court
    )

    driver.close()

if __name__ == '__main__':
    app.run(debug=True)