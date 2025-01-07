from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    StaleElementReferenceException,
    UnexpectedAlertPresentException,
)
import time
import pandas as pd


class SetorDataScraper:
    def __init__(self, setor_financeiro, options, service, acoes):
        self.setor_financeiro = setor_financeiro
        self.options = options
        self.service = service
        self.acoes = acoes
        self.dados = None

    def navegador_get(self, acao):
        #navegador = webdriver.Chrome(service=self.service, options=self.options)
        navegador = webdriver.Chrome(options=self.options)
        navegador.get(
            f"https://www.investsite.com.br/principais_indicadores.php?cod_negociacao={acao}"
        )
        return navegador

    def obter_dados_tabela(self, navegador):
        while True:
            try:
                tabela = navegador.find_element(By.ID, "dados_basicos")
                linhas = tabela.find_elements(By.TAG_NAME, "tr")
                lista_dados_basicos = []
                for linha in linhas:
                    # Pegar as células de cada linha
                    celulas = linha.find_elements(By.TAG_NAME, "td")
                    for celula in celulas:
                        lista_dados_basicos.append(celula.text)
                return lista_dados_basicos
            except StaleElementReferenceException:
                continue

    def rodar_acoes(self):
        acoes_processadas = set()
        dados = {"Segmento de Listagem": [], 
                 "Setor": [], 
                 "Segmento": [], 
                 "tic": []}

        for acao in self.acoes:

            navegador = self.navegador_get(acao=acao)

            elemento_text = navegador.find_elements(
                By.XPATH, "/html/body/div[1]/div[4]/div[2]"
            )

            if acao in acoes_processadas:
                print(f"Ação {acao} já processada, pulando.")

            elif (
                elemento_text
                and "código de negociação não encontrado." in elemento_text[0].text
            ):
                print(f"Código de negociação {acao} não encontrado.")

            else:
                start_time = time.time()
                try:
                    df_dic = self.obter_dados_tabela(navegador=navegador)
                except UnexpectedAlertPresentException:
                    df_dic = self.obter_dados_tabela(navegador=navegador)
                
                metrics = [
                    "Segmento de Listagem",
                    "Setor",
                    "Segmento",
                ]

                for i in range(0, len(df_dic)):
                    chave = df_dic[i]
                    if chave in metrics:
                        valor = df_dic[i + 1]
                        dados[chave].append(valor)
                    else:
                        continue

                dados["tic"].append(acao)
                end_time = time.time()

                # Calcula o tempo decorrido em segundos
                execution_time_seconds = end_time - start_time

                # Calcula o tempo decorrido em minutos
                execution_time_minutes = execution_time_seconds / 60

                # Imprime o tempo de execução em minutos
                print(
                    f"Tempo de execução da ação {acao}: {execution_time_minutes:.2f} minutos"
                )

            acoes_processadas.add(acao)

        return pd.DataFrame(dados)
