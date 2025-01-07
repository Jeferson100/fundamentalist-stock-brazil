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


class RetornosMargensDataScraper:
    def __init__(self, setor_financeiro, options, service, acoes, diretorio=None):
        self.setor_financeiro = setor_financeiro
        self.options = options
        self.service = service
        self.acoes = acoes
        self.diretorio = diretorio

    def navegador_get(self, acao):
        #navegador = webdriver.Chrome(service=self.service, options=self.options)
        navegador = webdriver.Chrome(options=self.options)
        navegador.get(
            f"https://www.investsite.com.br/principais_indicadores.php?cod_negociacao={acao}"
        )
        return navegador

    def obter_datas(self, navegador):
        while True:
            try:
                elementos_data = navegador.find_elements(
                    By.XPATH,
                    '//*[@id="tabela_resumo_empresa_margens_retornos"]/thead/tr/th[2]/select',
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
                    '//*[@id="tabela_resumo_empresa_margens_retornos"]/thead/tr/th[2]/select',
                )
                select = Select(select_element)
                select.select_by_visible_text(data)

                tabela = navegador.find_element(
                    By.ID, "tabela_resumo_empresa_margens_retornos"
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
            
            "Retorno s/ Capital Tangível Inicial": [np.nan] * len(datas),
            "Retorno s/ Capital Investido Inicial": [np.nan] * len(datas),
            "Retorno s/ Capital Tangível Inicial Pré-Impostos": [np.nan]
            * len(datas),
            "Retorno s/ Capital Investido Inicial Pré-Impostos": [np.nan]
            * len(datas),
            "Retorno s/ Patrimônio Líquido Inicial": [],
            "Retorno s/ Ativo Inicial": [],
            "Margem Bruta": [],
            "Margem Líquida": [],
            "Margem EBIT": [np.nan] * len(datas),
            "Margem EBITDA": [np.nan] * len(datas),
            "Giro do Ativo Inicial": [],
            "Alavancagem Financeira": [],
            "Passivo/Patrimônio Líquido": [],
            "Dívida Líquida/EBITDA": [np.nan] * len(datas),
        }
        for data in datas:
            while True:
                lista_resumo_balanco = self.obter_dados_tabela(
                    navegador=navegador, data=data
                )
                if lista_resumo_balanco:
                    break
            metrics = [
                "Retorno s/ Capital Tangível Inicial",
                "Retorno s/ Capital Investido Inicial",
                "Retorno s/ Capital Tangível Inicial Pré-Impostos",
                "Retorno s/ Capital Investido Inicial Pré-Impostos",
                "Retorno s/ Patrimônio Líquido Inicial",
                "Retorno s/ Ativo Inicial",
                "Margem Bruta",
                "Margem Líquida",
                "Margem EBIT",
                "Margem EBITDA",
                "Giro do Ativo Inicial",
                "Alavancagem Financeira",
                "Passivo/Patrimônio Líquido",
                "Dívida Líquida/EBITDA",
            ]

            for i in range(0, len(lista_resumo_balanco)):
                chave = lista_resumo_balanco[i]
                if chave in metrics:
                    valor = (
                        lista_resumo_balanco[i + 1]
                        .replace("R$", "")
                        .replace(",", ".")
                        .replace("%", "")
                        .strip()
                    )
                    dados[chave].append(valor)
                else:
                    continue
        try:
            df_resumo_balanco = pd.DataFrame(dados)
        except ValueError:
            for key in dados.keys():
                if len(dados[key]) == 0:
                    dados[key].extend([np.nan] * len(datas))
            df_resumo_balanco = pd.DataFrame(dados)
        
        df_resumo_balanco["datas"] = datas

        df_resumo_balanco.rename(
            columns={
                "Retorno s/ Capital Tangível Inicial": "retorno_sobre_capital_tangivel_inicial",
                "Retorno s/ Capital Investido Inicial": "retorno_sobre_capital_investido_inicial",
                "Retorno s/ Capital Tangível Inicial Pré-Impostos": "retorno_sobre_capital_tangivel_inicial_pre_impostos",
                "Retorno s/ Capital Investido Inicial Pré-Impostos": "retorno_sobre_capital_investido_inicial_pre_impostos",
                "Retorno s/ Patrimônio Líquido Inicial": "retorno_sobre_patrimonio_liquido_inicial",
                "Retorno s/ Ativo Inicial": "retorno_sobre_ativo_inicial",
                "Margem Bruta": "margem_bruta",
                "Margem Líquida": "margem_liquida",
                "Margem EBIT": "margem_ebit",
                "Margem EBITDA": "margem_ebitda",
                "Giro do Ativo Inicial": "giro_do_ativo_inicial",
                "Alavancagem Financeira": "alavancagem_financeira",
                "Passivo/Patrimônio Líquido": "passivo_patrimonio_liquido",
                "Dívida Líquida/EBITDA": "divida_liquida_ebitda",
            },
            inplace=True,
        )

        return df_resumo_balanco

    def coletar_dados_nao_financeiros(self, navegador, datas):
        dados = {
            "Retorno s/ Capital Tangível Inicial": [],
            "Retorno s/ Capital Investido Inicial": [],
            "Retorno s/ Capital Tangível Inicial Pré-Impostos": [],
            "Retorno s/ Capital Investido Inicial Pré-Impostos": [],
            "Retorno s/ Patrimônio Líquido Inicial": [],
            "Retorno s/ Ativo Inicial": [],
            "Margem Bruta": [],
            "Margem Líquida": [],
            "Margem EBIT": [],
            "Margem EBITDA": [],
            "Giro do Ativo Inicial": [],
            "Alavancagem Financeira": [],
            "Passivo/Patrimônio Líquido": [],
            "Dívida Líquida/EBITDA": [],
        }

        for data in datas:
            while True:
                lista_resumo_balanco = self.obter_dados_tabela(
                    navegador=navegador, data=data
                )
                if lista_resumo_balanco:
                    break
            metrics = [
                "Retorno s/ Capital Tangível Inicial",
                "Retorno s/ Capital Investido Inicial",
                "Retorno s/ Capital Tangível Inicial Pré-Impostos",
                "Retorno s/ Capital Investido Inicial Pré-Impostos",
                "Retorno s/ Patrimônio Líquido Inicial",
                "Retorno s/ Ativo Inicial",
                "Margem Bruta",
                "Margem Líquida",
                "Margem EBIT",
                "Margem EBITDA",
                "Giro do Ativo Inicial",
                "Alavancagem Financeira",
                "Passivo/Patrimônio Líquido",
                "Dívida Líquida/EBITDA",
            ]
            for i in range(0, len(lista_resumo_balanco)):
                chave = lista_resumo_balanco[i]
                if chave in metrics:
                    valor = (
                        lista_resumo_balanco[i + 1]
                        .replace("R$", "")
                        .replace(",", ".")
                        .replace("%", "")
                        .strip()
                    )
                    dados[chave].append(valor)
                else:
                    continue
        try:
            df_resumo_balanco = pd.DataFrame(dados)
        except ValueError:
            for key in dados.keys():
                if len(dados[key]) == 0:
                    dados[key].extend([np.nan] * len(datas))
            df_resumo_balanco = pd.DataFrame(dados)
        
        df_resumo_balanco["datas"] = datas

        df_resumo_balanco.rename(
            columns={
                "Retorno s/ Capital Tangível Inicial": "retorno_sobre_capital_tangivel_inicial",
                "Retorno s/ Capital Investido Inicial": "retorno_sobre_capital_investido_inicial",
                "Retorno s/ Capital Tangível Inicial Pré-Impostos": "retorno_sobre_capital_tangivel_inicial_pre_impostos",
                "Retorno s/ Capital Investido Inicial Pré-Impostos": "retorno_sobre_capital_investido_inicial_pre_impostos",
                "Retorno s/ Patrimônio Líquido Inicial": "retorno_sobre_patrimonio_liquido_inicial",
                "Retorno s/ Ativo Inicial": "retorno_sobre_ativo_inicial",
                "Margem Bruta": "margem_bruta",
                "Margem Líquida": "margem_liquida",
                "Margem EBIT": "margem_ebit",
                "Margem EBITDA": "margem_ebitda",
                "Giro do Ativo Inicial": "giro_do_ativo_inicial",
                "Alavancagem Financeira": "alavancagem_financeira",
                "Passivo/Patrimônio Líquido": "passivo_patrimonio_liquido",
                "Dívida Líquida/EBITDA": "divida_liquida_ebitda",
            },
            inplace=True,
        )


        return df_resumo_balanco

    def rodar_acoes(self):
        iteracao = 0
        lista_dataframes = []
        acoes_processadas = set()
        for acao in self.acoes:
            time.sleep(10)
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

                datas = self.obter_datas(navegador=navegador)

                if acao in self.setor_financeiro:
                    try:
                        df_dados = self.coletar_dados_financeiros(
                            navegador=navegador, datas=datas
                        )
                    except UnexpectedAlertPresentException:
                        df_dados = self.coletar_dados_financeiros(
                            navegador=navegador, datas=datas
                        )
                    colunas = df_dados.columns[
                        (df_dados.columns != "giro_do_ativo_inicial")
                        & (df_dados.columns != "alavancagem_financeira")
                        & (df_dados.columns != "passivo_patrimonio_liquido")
                        & (df_dados.columns != "divida_liquida_ebitda")
                        & (df_dados.columns != "datas")
                    ]
                    for col in colunas:
                        df_dados[col] = (
                            pd.to_numeric(df_dados[col], errors="coerce") / 100
                        )
                else:
                    try:
                        df_dados = self.coletar_dados_nao_financeiros(
                            navegador=navegador, datas=datas
                        )
                    except UnexpectedAlertPresentException:
                        df_dados = self.coletar_dados_nao_financeiros(
                            navegador=navegador, datas=datas
                        )

                    colunas = df_dados.columns[
                        (df_dados.columns != "giro_do_ativo_inicial")
                        & (df_dados.columns != "alavancagem_financeira")
                        & (df_dados.columns != "passivo_patrimonio_liquido")
                        & (df_dados.columns != "divida_liquida_ebitda")
                        & (df_dados.columns != "datas")
                    ]
                    for col in colunas:
                        df_dados[col] = (
                            pd.to_numeric(df_dados[col], errors="coerce") / 100
                        )

                df_dados["tic"] = acao

                lista_dataframes.append(df_dados)

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
            self.diretorio = "dados/retornos_margens.csv"
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
