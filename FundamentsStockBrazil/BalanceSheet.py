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
import datetime


class TabelaResumoDataScraper:
    def __init__(self, setor_financeiro, options, acoes, service=None, diretorio=None, data_inicio:str = None):
        self.setor_financeiro = setor_financeiro
        self.options = options
        self.service = service
        self.acoes = acoes
        self.diretorio = diretorio
        self.data_inicio = data_inicio
        

    def navegador_get(self, acao):
        if self.service is not None:
            navegador = webdriver.Chrome(service=self.service, options=self.options)
        else:
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
                    '//*[@id="tabela_resumo_empresa_bp"]/thead/tr/th[2]/select',
                )
                datas = [elemento.text for elemento in elementos_data]
                if len(datas) == 1:
                    string_de_datas = datas[0]
                    datas = string_de_datas.split("\n")
                if self.data_inicio:
                    data_referencia = datetime.datetime.strptime(self.data_inicio, '%d/%m/%Y')
                    datas = [data for data in datas if 'Atual' in data or datetime.datetime.strptime(data, '%d/%m/%Y') >= data_referencia]
                return datas
            except StaleElementReferenceException:
                continue

    def obter_dados_tabela(self, navegador, data):
        while True:
            try:
                time.sleep(0.2)
                select_element = navegador.find_element(
                    By.XPATH,
                    '//*[@id="tabela_resumo_empresa_bp"]/thead/tr/th[2]/select',
                )
                time.sleep(0.2)

                select = Select(select_element)

                time.sleep(0.5)

                select.select_by_visible_text(data)

                time.sleep(0.2)

                tabela = navegador.find_element(By.ID, "tabela_resumo_empresa_bp")

                time.sleep(0.2)

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
            "Caixa e Equivalentes de Caixa": [np.nan] * len(datas),
            "Ativo Total": [],
            "Dívida de Curto Prazo": [np.nan] * len(datas),
            "Dívida de Longo Prazo": [np.nan] * len(datas),
            "Dívida Bruta": [np.nan] * len(datas),
            "Dívida Líquida": [np.nan] * len(datas),
            "Patrimônio Líquido": [],
            "Valor Patrimonial da Ação": [],
            "Ações Ordinárias": [],
            "Ações Preferenciais": [],
            "Total": [],
        }
        for data in datas:
            while True:
                lista_resumo_balanco = self.obter_dados_tabela(
                    navegador=navegador, data=data
                )
                if lista_resumo_balanco:
                    break
            for i in range(0, len(lista_resumo_balanco)):
                chave = lista_resumo_balanco[i]
                if chave in [
                    "Ativo Total",
                    "Patrimônio Líquido",
                    "Valor Patrimonial da Ação",
                    "Ações Ordinárias",
                    "Ações Preferenciais",
                    "Total",
                ]:
                    valor = (
                        lista_resumo_balanco[i + 1]
                        .replace("R$", "")
                        .replace(",", ".")
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
                "Caixa e Equivalentes de Caixa": "caixa_equivalentes_caixa",
                "Ativo Total": "ativo_total",
                "Dívida de Curto Prazo": "divida_curto_prazo",
                "Dívida de Longo Prazo": "divida_longo_prazo",
                "Dívida Bruta": "divida_bruta",
                "Dívida Líquida": "divida_liquida",
                "Patrimônio Líquido": "patrimonio_liquido",
                "Valor Patrimonial da Ação": "valor_patrimonial_acao",
                "Ações Ordinárias": "acoes_ordinarias",
                "Ações Preferenciais": "acoes_preferenciais",
                "Total": "total",
            },
            inplace=True,
        )

        return df_resumo_balanco

    def coletar_dados_nao_financeiros(self, navegador, datas):
        dados = {
            "Caixa e Equivalentes de Caixa": [],
            "Ativo Total": [],
            "Dívida de Curto Prazo": [],
            "Dívida de Longo Prazo": [],
            "Dívida Bruta": [],
            "Dívida Líquida": [],
            "Patrimônio Líquido": [],
            "Valor Patrimonial da Ação": [],
            "Ações Ordinárias": [],
            "Ações Preferenciais": [],
            "Total": [],
        }

        for data in datas:
            while True:
                lista_resumo_balanco = self.obter_dados_tabela(
                    navegador=navegador, data=data
                )
                if lista_resumo_balanco:
                    break
            metrics = [
                "Caixa e Equivalentes de Caixa",
                "Ativo Total",
                "Dívida de Curto Prazo",
                "Dívida de Longo Prazo",
                "Dívida Bruta",
                "Dívida Líquida",
                "Patrimônio Líquido",
                "Valor Patrimonial da Ação",
                "Ações Ordinárias",
                "Ações Preferenciais",
                "Total",
            ]
            for i in range(0, len(lista_resumo_balanco)):
                chave = lista_resumo_balanco[i]
                if chave in metrics:
                    valor = (
                        lista_resumo_balanco[i + 1]
                        .replace("R$", "")
                        .replace(",", ".")
                        .strip()
                    )
                    dados[chave].append(valor)
                else:
                    continue

            lista_resumo_balanco.clear()

        navegador.delete_all_cookies()
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
                "Caixa e Equivalentes de Caixa": "caixa_equivalentes_caixa",
                "Ativo Total": "ativo_total",
                "Dívida de Curto Prazo": "divida_curto_prazo",
                "Dívida de Longo Prazo": "divida_longo_prazo",
                "Dívida Bruta": "divida_bruta",
                "Dívida Líquida": "divida_liquida",
                "Patrimônio Líquido": "patrimonio_liquido",
                "Valor Patrimonial da Ação": "valor_patrimonial_acao",
                "Ações Ordinárias": "acoes_ordinarias",
                "Ações Preferenciais": "acoes_preferenciais",
                "Total": "total",
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
                By.XPATH, '//*[@id="main-content"]/div[2]/div/p[1]'
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
                        df_resumo_balanco = self.coletar_dados_financeiros(
                            navegador=navegador, datas=datas
                        )
                    except UnexpectedAlertPresentException:
                        df_resumo_balanco = self.coletar_dados_financeiros(
                            navegador=navegador, datas=datas
                        )
                        print(
                            f"Erro na coletação da ação {acao}, UnexpectedAlertPresentException tentando novamente"
                        )
                    colunas = ["ativo_total", "patrimonio_liquido"]
                    for col in colunas:
                        df_resumo_balanco[col] = df_resumo_balanco[col].apply(
                            self.converter_valor
                        )
                else:
                    try:
                        df_resumo_balanco = self.coletar_dados_nao_financeiros(
                            navegador=navegador, datas=datas
                        )
                    except UnexpectedAlertPresentException:
                        df_resumo_balanco = self.coletar_dados_nao_financeiros(
                            navegador=navegador, datas=datas
                        )
                        print(
                            f"Erro na coletação da ação {acao}, UnexpectedAlertPresentException tentando novamente"
                        )

                    colunas = [
                        "caixa_equivalentes_caixa",
                        "ativo_total",
                        "divida_liquida",
                        "divida_curto_prazo",
                        "divida_longo_prazo",
                        "divida_bruta",
                        "patrimonio_liquido",
                    ]
                    for col in colunas:
                        df_resumo_balanco[col] = df_resumo_balanco[col].apply(
                            self.converter_valor
                        )

                df_resumo_balanco["tic"] = acao

                lista_dataframes.append(df_resumo_balanco)

                iteracao += 1

                if iteracao % 10 == 0:
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
            self.diretorio = "../dados/resumo_balanco.csv"
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
