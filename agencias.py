from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import pandas as pd
from scraping import Scraping
import numpy as np




geral = []
ag_aux = []
colunas = ['Nome', 'Endereco', 'Cep - UF', 'Telefone', 'Numero CGC', 'Horario de Atendimento']
url = "https://www.caixa.gov.br/atendimento/Paginas/encontre-a-caixa.aspx"


with Scraping(url=url) as driver:
    
    try:
        # submit cookie
        driver.find_element(By.ID, 'adopt-accept-all-button').click()

        # Primeiro cammpo de selecao: Tipo de Atendimentos
        classe_atendimento = driver.find_element(By.CLASS_NAME, 'select-d')
        tipo_atendimento = Select(classe_atendimento)
        # 1 = Agencias
        tipo_atendimento.select_by_value("1")

        time.sleep(3)
        # Segundo campo: Unidade Federativa - UF
        uf = driver.find_element(By.ID, 'ctl00_ctl61_g_7fcd6a4b_5583_4b25_b2c4_004b6fef4036_ddlUf')
        regiao = Select(uf)
        # RJ = Rio de Janeiro
        regiao.select_by_value("MG")

        time.sleep(3)
        # Numero de cidades do rio de janeiro
        class_cont = driver.find_element(By.ID, 'ctl00_ctl61_g_7fcd6a4b_5583_4b25_b2c4_004b6fef4036_ddlCidade')
        # lista de elementos: cidades do rio de janeiro
        total_agencias = len(Select(class_cont).options)
        

        for i, item in enumerate(range(total_agencias)):
            #print(agencias.options[item].text)
            municipio = driver.find_element(By.ID, 'ctl00_ctl61_g_7fcd6a4b_5583_4b25_b2c4_004b6fef4036_ddlCidade')
            agencias = Select(municipio)

            # botão de pesquisar
            time.sleep(3)
            btn = driver.find_element(By.ID, 'ctl00_ctl61_g_7fcd6a4b_5583_4b25_b2c4_004b6fef4036_btnBuscar')

            # Seleciona um municipio e pesquisa
            agencias.options[item].click()
            
            btn.click()
            time.sleep(3)

            # Resultado da Pesuisa pode ser dessa classe 
            resultado = driver.find_element(By.CLASS_NAME, 'colsm-7')
            resultado2 = driver.find_elements(By.CLASS_NAME, 'resultado-busca-item')
            res = resultado.text

            match res:

                case 'Nenhum ponto de atendimento foi localizado com os dados informados.':
                    print(f'Não há dados para essa opção')
                
                case '':
                    print(f'Opcao não é valida')
                case _:
                    for item in resultado2:
                        ax = item.text.split('\n')
                        array_1x6 = np.array(ax)
                        geral.append(pd.DataFrame([array_1x6], columns=colunas))
            print(f'\n\n: vez: {i}')
    finally:
        driver.quit()


data = pd.concat(geral)

data.to_csv('Agencias_Estado_MG.csv')
