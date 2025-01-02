from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import (
    StaleElementReferenceException,
    UnexpectedAlertPresentException,
)
import time
import pandas as pd
import numpy as np


class DreDataScraper:
    def __init__(self, setor_financeiro, options, service, acoes, diretorio=None):
        self.setor_financeiro = setor_financeiro
        self.options = options
        self.service = service
        self.acoes = acoes
        self.diretorio = diretorio

    def navegador_get(self, acao):
        navegador = webdriver.Chrome(service=self.service, options=self.options)
        navegador.get(
            f"https://www.investsite.com.br/principais_indicadores.php?cod_negociacao={acao}"
        )
        return navegador

    def obter_datas(self, navegador):
        while True:
            try:
                elementos_data = navegador.find_elements(
                    By.XPATH,
                    '//*[@id="tabela_resumo_empresa_dre_3meses"]/thead/tr/th[2]/select/option',
                )
                datas = [elemento.text for elemento in elementos_data]
                if len(datas) == 1:
                    string_de_datas = datas[0]
                    datas = string_de_datas.split("\n")
                return datas
            except StaleElementReferenceException:
                continue

    def obter_dados_tabela(self, navegador, data):
        while True:
            try:
                select_element = navegador.find_element(
                    By.XPATH,
                    "/html/body/div[1]/div[4]/div[2]/div[1]/div[3]/table[2]/thead/tr/th[2]/select",
                )
                select = Select(select_element)
                select.select_by_visible_text(data)

                tabela = navegador.find_element(
                    By.ID, "tabela_resumo_empresa_dre_3meses"
                )
                linhas = tabela.find_elements(By.TAG_NAME, "tr")

                lista_resumo_balanco = []
                for linha in linhas:
                    celulas = linha.find_elements(By.TAG_NAME, "td")
                    for celula in celulas:
                        lista_resumo_balanco.append(celula.text)

                return lista_resumo_balanco
            except StaleElementReferenceException:
                continue

    def coletar_dados_financeiros(self, navegador, datas):
        dados = {
            "datas": datas,
            "receita_liquida": [],
            "resultado_bruto": [],
            "ebit": [np.nan] * len(datas),
            "depreciacao_amortizacao": [np.nan] * len(datas),
            "ebitda": [np.nan] * len(datas),
            "lucro_liquido": [],
            "lucro_por_acao": [np.nan] * len(datas),
        }
        for data in datas:
            while True:
                lista_resumo_balanco = self.obter_dados_tabela(
                    navegador=navegador, data=data
                )
                if lista_resumo_balanco:
                    break
            dados["receita_liquida"].append(
                lista_resumo_balanco[1].replace("R$", "").replace(",", ".").strip()
            )
            dados["resultado_bruto"].append(
                lista_resumo_balanco[3].replace("R$", "").replace(",", ".").strip()
            )
            dados["lucro_liquido"].append(
                lista_resumo_balanco[7].replace("R$", "").replace(",", ".").strip()
            )

        df_resumo_balanco = pd.DataFrame(dados)

        return df_resumo_balanco

    def coletar_dados_nao_financeiros(self, navegador, datas):
        dados = {
            "datas": datas,
            "receita_liquida": [],
            "resultado_bruto": [],
            "ebit": [],
            "depreciacao_amortizacao": [],
            "ebitda": [],
            "lucro_liquido": [],
            "lucro_por_acao": [],
        }

        for data in datas:
            while True:
                lista_resumo_balanco = self.obter_dados_tabela(
                    navegador=navegador, data=data
                )
                if lista_resumo_balanco:
                    break
            dados["receita_liquida"].append(
                lista_resumo_balanco[1].replace("R$", "").replace(",", ".").strip()
            )
            dados["resultado_bruto"].append(
                lista_resumo_balanco[3].replace("R$", "").replace(",", ".").strip()
            )
            dados["ebit"].append(
                lista_resumo_balanco[5].replace("R$", "").replace(",", ".").strip()
            )
            dados["depreciacao_amortizacao"].append(
                lista_resumo_balanco[7].replace("R$", "").replace(",", ".").strip()
            )
            dados["ebitda"].append(
                lista_resumo_balanco[9].replace("R$", "").replace(",", ".").strip()
            )
            dados["lucro_liquido"].append(
                lista_resumo_balanco[11].replace("R$", "").replace(",", ".").strip()
            )
            dados["lucro_por_acao"].append(
                lista_resumo_balanco[13].replace("R$", "").replace(",", ".").strip()
            )

        df_resumo_balanco = pd.DataFrame(dados)

        return df_resumo_balanco

    def rodar_acoes(self):
        iteracao = 0
        lista_dataframes = []
        acoes_processadas = set()
        for acao in self.acoes:
            navegador = self.navegador_get(acao=acao)

            elemento_text = navegador.find_elements(
                By.XPATH, "/html/body/div[1]/div[4]/div[2]"
            )

            if acao in acoes_processadas:
                print(f"Ação {acao} já processada, pulando.")

            elif "código de negociação não encontrado." in elemento_text[0].text:
                print(f"Código de negociação {acao} não encontrado.")

            else:
                start_time = time.time()

                datas = self.obter_datas(navegador=navegador)

                if acao in self.setor_financeiro:
                    try:
                        df_dre = self.coletar_dados_financeiros(
                            navegador=navegador, datas=datas
                        )
                    except UnexpectedAlertPresentException:
                        print(
                            f"Erro na coletação da ação {acao}, UnexpectedAlertPresentException tentando novamente"
                        )
                        df_dre = self.coletar_dados_financeiros(
                            navegador=navegador, datas=datas
                        )
                    colunas_selecionadas = df_dre.columns[
                        (df_dre.columns != "datas")
                        & (df_dre.columns != "lucro_por_acao")
                        & (df_dre.columns != "ebit")
                        & (df_dre.columns != "depreciacao_amortizacao")
                        & (df_dre.columns != "lucro_por_acao")
                        & (df_dre.columns != "ebitida")
                        & (df_dre.columns != "lucro_por_acao")
                    ]
                    for col in colunas_selecionadas:
                        df_dre[col] = df_dre[col].apply(self.converter_valor)
                else:
                    try:
                        df_dre = self.coletar_dados_nao_financeiros(
                            navegador=navegador, datas=datas
                        )
                    except UnexpectedAlertPresentException:
                        print(
                            f"Erro na coletação da ação {acao}, UnexpectedAlertPresentException tentando novamente"
                        )
                        df_dre = self.coletar_dados_nao_financeiros(
                            navegador=navegador, datas=datas
                        )
                    for col in df_dre.columns[
                        (df_dre.columns != "datas")
                        & (df_dre.columns != "lucro_por_acao")
                        & (df_dre.columns != "tic")
                    ]:
                        df_dre[col] = df_dre[col].apply(self.converter_valor)

                df_dre["tic"] = acao
                lista_dataframes.append(df_dre)

                iteracao += 1

                if iteracao % 5 == 0:
                    self.salvar_dados(lista_dataframes=lista_dataframes)

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

        return pd.concat(lista_dataframes)

    def salvar_dados(self, lista_dataframes):
        if self.diretorio is None:
            self.diretorio = "dados/dre.csv"
        pd.concat(lista_dataframes).to_csv(self.diretorio)

    def converter_valor(self, valor):
        if isinstance(valor, str):
            if valor.endswith("T"):
                return float(valor.replace("T", "").replace(" ", "")) * 1_000_000
            elif valor.endswith("B"):
                return float(valor.replace("B", "").replace(" ", "")) * 1_000
            elif valor.endswith("M"):
                return float(valor.replace("M", "").replace(" ", "")) * 1
            elif valor.endswith("K"):
                return float(valor.replace("K", "").replace(" ", "")) * 0.001
            elif valor == "NA":
                return float("nan")
        else:
            return valor
