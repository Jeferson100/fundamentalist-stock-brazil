from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import (
    StaleElementReferenceException,
    UnexpectedAlertPresentException,
)
from typing import List
import asyncio
import time
import pandas as pd
import numpy as np
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class AsyncPrecosRelativosDataScraper:
    def __init__(self, 
                 setor_financeiro : List[str], 
                 options, 
                 service, 
                 acoes: List[str], 
                 diretorio: str = None):
        self.setor_financeiro = setor_financeiro
        self.options = options
        self.service = service
        self.acoes = acoes
        self.diretorio = diretorio
    
    async def navegador_get(self, acao):
        navegador = webdriver.Chrome(service=self.service, options=self.options)
        navegador.get(
            f"https://www.investsite.com.br/principais_indicadores.php?cod_negociacao={acao}"
        )
        return navegador
    
    async def obter_datas(self, navegador):
        while True:
            try:
                elementos_data = navegador.find_elements(
                    By.XPATH,
                    '//*[@id="tabela_resumo_empresa_precos_relativos"]/thead/tr/th[2]/select',
                )
                datas = [elemento.text for elemento in elementos_data]
                if len(datas) == 1:
                    string_de_datas = datas[0]
                    datas = string_de_datas.split("\n")
                return datas
            except StaleElementReferenceException:
                continue
    
    async def obter_dados_tabela(self, navegador, data):
        while True:
            try:
                select_element = navegador.find_element(
                    By.XPATH,
                    "/html/body/div[3]/div/div[2]/div/div[2]/main/div[2]/div[1]/section[2]/div/table/thead/tr/th[2]/select",
                )
                select = Select(select_element)
                select.select_by_visible_text(data)

                tabela = navegador.find_element(By.ID, "precos_relativos")
                linhas = tabela.find_elements(By.TAG_NAME, "tr")

                lista_resumo_balanco = []
                for linha in linhas:
                    celulas = linha.find_elements(By.TAG_NAME, "td")
                    for celula in celulas:
                        lista_resumo_balanco.append(celula.text)

                return lista_resumo_balanco
            except StaleElementReferenceException:
                await asyncio.sleep(0.1)
                continue

    async def coletar_dados_financeiros(self, navegador, datas):
        dados = {
            "datas": datas,
            "Preço/Lucro": [],
            "Preço/VPA": [],
            "Preço/Receita Líquida": [],
            "Preço/FCO": [],
            "Preço/FCF": [np.nan] * len(datas),
            "Preço/Ativo Total": [],
            "Preço/EBIT": [np.nan] * len(datas),
            "Preço/Capital Giro": [np.nan] * len(datas),
            "Preço/NCAV": [np.nan] * len(datas),
            "EV/EBIT": [np.nan] * len(datas),
            "EV/EBITDA": [np.nan] * len(datas),
            "EV/Receita Líquida": [np.nan] * len(datas),
            "EV/FCO": [np.nan] * len(datas),
            "EV/FCF": [np.nan] * len(datas),
            "EV/Ativo Total": [np.nan] * len(datas),
            "Market Cap Empresa": [],
            "Enterprise Value": [np.nan] * len(datas),
            "Dividend Yield": [],
        }
        for data in datas:
            while True:
                lista_resumo_balanco = await self.obter_dados_tabela(
                    navegador=navegador, data=data
                )
                if lista_resumo_balanco:
                    break
            metricas = [
                "Preço/Lucro",
                "Preço/VPA",
                "Preço/Receita Líquida",
                "Preço/FCO",
                "Preço/Ativo Total",
                "Market Cap Empresa",
                "Dividend Yield",
            ]
            for i in range(0, len(lista_resumo_balanco)):
                chave = lista_resumo_balanco[i]
                if chave in metricas:
                    valor = lista_resumo_balanco[i + 1].replace(',', '.')
                    dados[chave].append(valor)

        df_resumo_balanco = pd.DataFrame(dados)

        df_resumo_balanco = df_resumo_balanco.rename(
            columns=lambda coluna: coluna.replace("/", "_").replace(" ", "_").lower()
        )

        return df_resumo_balanco

    
    async def coletar_dados_nao_financeiros(self, navegador, datas):
        dados = {
            "datas": datas,
            "Preço/Lucro": [],
            "Preço/VPA": [],
            "Preço/Receita Líquida": [],
            "Preço/FCO": [],
            "Preço/FCF": [],
            "Preço/Ativo Total": [],
            "Preço/EBIT": [],
            "Preço/Capital Giro": [],
            "Preço/NCAV": [],
            "EV/EBIT": [],
            "EV/EBITDA": [],
            "EV/Receita Líquida": [],
            "EV/FCO": [],
            "EV/FCF": [],
            "EV/Ativo Total": [],
            "Market Cap Empresa": [],
            "Enterprise Value": [],
            "Dividend Yield": [],
        }

        for data in datas:
            while True:
                lista_resumo_balanco = await self.obter_dados_tabela(
                    navegador=navegador, data=data
                )
                if lista_resumo_balanco:
                    break

            metricas = [
                "Preço/Lucro",
                "Preço/VPA",
                "Preço/Receita Líquida",
                "Preço/FCO",
                "Preço/FCF",
                "Preço/Ativo Total",
                "Preço/EBIT",
                "Preço/Capital Giro",
                "Preço/NCAV",
                "EV/EBIT",
                "EV/EBITDA",
                "EV/Receita Líquida",
                "EV/FCO",
                "EV/FCF",
                "EV/Ativo Total",
                "Market Cap Empresa",
                "Enterprise Value",
                "Dividend Yield",
            ]
            for i in range(0, len(lista_resumo_balanco)):
                chave = lista_resumo_balanco[i]
                if chave in metricas:
                    valor = lista_resumo_balanco[i + 1].replace(',', '.')
                    dados[chave].append(valor)

        df_resumo_balanco = pd.DataFrame(dados)

        df_resumo_balanco = df_resumo_balanco.rename(
            columns=lambda coluna: coluna.replace("/", "_").replace(" ", "_").lower()
        )

        return df_resumo_balanco
    
    async def rodar_acoes(self):
        iteracao = 0
        lista_dataframes = []
        acoes_processadas = set()
        for acao in self.acoes:

            navegador = await self.navegador_get(acao=acao)

            elemento_text = navegador.find_elements(
                By.XPATH, "/html/body/div[1]/div[4]/div[2]"
            )

            if acao in acoes_processadas:
                print(f"Ação {acao} já processada, pulando.")

            # elif 'código de negociação não encontrado.' in elemento_text[0].text:
            if (
                elemento_text
                and "código de negociação não encontrado." in elemento_text[0].text
            ):
                print(f"Código de negociação {acao} não encontrado.")

            else:
                start_time = time.time()

                datas = await self.obter_datas(navegador=navegador)

                if acao in self.setor_financeiro:
                    try:
                        df_dados = await self.coletar_dados_financeiros(
                            navegador=navegador, datas=datas
                        )
                    except UnexpectedAlertPresentException:
                        df_dados = await self.coletar_dados_financeiros(
                            navegador=navegador, datas=datas
                        )
                    colunas = df_dados.columns[
                        (df_dados.columns == "market_cap_empresa")
                    ]
                    for col in colunas:
                        df_dados[col] = df_dados[col].apply(self.converter_valor)
                    df_dados["dividend_yield"] = (
                        pd.to_numeric(df_dados["dividend_yield"].str.replace('%', '').str.replace(',', '.'),errors='coerce') / 100
                    )
                    df_dados["datas"] = df_dados["datas"].apply(self.converter_data)
                else:
                    try:
                        df_dados = await self.coletar_dados_nao_financeiros(
                            navegador=navegador, datas=datas
                        )
                    except UnexpectedAlertPresentException:
                        df_dados = self.coletar_dados_nao_financeiros(
                            navegador=navegador, datas=datas
                        )
                    colunas = ["market_cap_empresa", "enterprise_value"]
                    for col in colunas:
                        df_dados[col] = df_dados[col].apply(self.converter_valor)

                    df_dados['dividend_yield'] = pd.to_numeric(df_dados["dividend_yield"].str.replace('%', '').str.replace(',', '.'),errors='coerce') / 100

                    df_dados["datas"] = df_dados["datas"].apply(self.converter_data)

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
            self.diretorio = "dados/precos_relativos.csv"
        pd.concat(lista_dataframes).to_csv(self.diretorio)

    def converter_valor(self, valor):
        if isinstance(valor, str):
            if valor.endswith("T"):
                return (
                    float(
                        valor.replace("R$", "")
                        .replace("T", "")
                        .replace(" ", "")
                        .replace(",", ".")
                    )
                    * 1_000_000
                )
            elif valor.endswith("B"):
                return (
                    float(
                        valor.replace("R$", "")
                        .replace("B", "")
                        .replace(" ", "")
                        .replace(",", ".")
                    )
                    * 1_000
                )
            elif valor.endswith("M"):
                return (
                    float(
                        valor.replace("R$", "")
                        .replace("M", "")
                        .replace(" ", "")
                        .replace(",", ".")
                    )
                    * 1
                )
            elif valor.endswith("K"):
                return (
                    float(
                        valor.replace("R$", "")
                        .replace("K", "")
                        .replace(" ", "")
                        .replace(",", ".")
                    )
                    * 0.001
                )
            elif valor == "NA":
                return float("nan")
        else:
            return valor

    def converter_data(self, valor):
        if "Atual - " in valor:
            return valor.replace("Atual - ", "")
        return valor


async def main():
    # Configurações do navegador

    with open('codigos_ibovespa.txt', 'r') as f:
        acoes = f.read().splitlines()

    setor_financeiro = {'BBAS3', 'BBDC3', 'BBDC4', 'BBSE3', 'ITUB4', 'BPAC11', 'ITUB4', 'SANB11', 'IRBR3'}

    chrome_driver_path = "/usr/bin/chromedriver"

    service = Service(executable_path=chrome_driver_path)

    options = Options()
    options.add_argument("--headless")  # Executar em modo headless
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-shm-usage")  # Reduz o uso de memória
    options.add_argument("--disable-gpu")  # Desativar o uso de GPU
    options.add_argument("--window-size=1920,1080")  # Definir o tamanho da janela
    
    # Dados de exemplo

    diretorio = "dados/precos_relativos.csv"

    # Instanciar o scraper
    scraper = AsyncPrecosRelativosDataScraper(
        setor_financeiro=setor_financeiro,
        options=options,
        service=service,
        acoes=acoes,
        diretorio=diretorio
    )

    # Rodar a coleta de dados
    dataframes = await scraper.rodar_acoes()

    # Salvar os resultados
    print("Dados coletados com sucesso!")
    print(dataframes)

# Executar o evento assíncrono
if __name__ == "__main__":
    asyncio.run(main())
