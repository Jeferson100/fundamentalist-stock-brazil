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
    def __init__(
        self,
        setor_financeiro: List[str],
        options,
        service,
        acoes: List[str],
        diretorio: str = None,
        max_concurrent: int = 5
    ):
        self.setor_financeiro = setor_financeiro
        self.options = options
        self.service = service
        self.acoes = acoes
        self.diretorio = diretorio
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def processador_acao(self, acao):
        async with self.semaphore:
            try:
                navegador = await self.navegador_get(acao)
                elemento_text = navegador.find_elements(
                    By.XPATH, "/html/body/div[1]/div[4]/div[2]"
                )

                if (
                    elemento_text
                    and "código de negociação não encontrado." in elemento_text[0].text
                ):
                    print(f"Código de negociação {acao} não encontrado.")
                    return None

                start_time = time.time()
                datas = await self.obter_datas(navegador)

                try:
                    if acao in self.setor_financeiro:
                        df_dados = await self.coletar_dados_financeiros(navegador, datas)
                    else:
                        df_dados = await self.coletar_dados_nao_financeiros(navegador, datas)

                    await self.processar_dataframe(df_dados, acao)
                    
                    end_time = time.time()
                    execution_time_minutes = (end_time - start_time) / 60
                    print(f"Tempo de execução da ação {acao}: {execution_time_minutes:.2f} minutos")
                    
                    return df_dados

                except Exception as e:
                    print(f"Erro ao processar ação {acao}: {str(e)}")
                    return None

            finally:
                navegador.quit()

    async def processar_dataframe(self, df_dados, acao):
        if acao in self.setor_financeiro:
            colunas = df_dados.columns[(df_dados.columns == "market_cap_empresa")]
            for col in colunas:
                df_dados[col] = df_dados[col].apply(self.converter_valor)
        else:
            colunas = ["market_cap_empresa", "enterprise_value"]
            for col in colunas:
                df_dados[col] = df_dados[col].apply(self.converter_valor)

        df_dados["dividend_yield"] = (
            pd.to_numeric(
                df_dados["dividend_yield"]
                .str.replace("%", "")
                .str.replace(",", "."),
                errors="coerce",
            )
            / 100
        )
        df_dados["datas"] = df_dados["datas"].apply(self.converter_data)
        df_dados["tic"] = acao

    async def rodar_acoes(self):
        tasks = []
        lista_dataframes = []
        
        # Criar tasks para cada ação
        for acao in self.acoes:
            task = asyncio.create_task(self.processador_acao(acao))
            tasks.append(task)

        # Aguardar conclusão de todas as tasks
        resultados = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filtrar resultados válidos e concatenar dataframes
        lista_dataframes = [df for df in resultados if df is not None]
        
        if lista_dataframes:
            resultado_final = pd.concat(lista_dataframes)
            self.salvar_dados([resultado_final])
            return resultado_final
        
        return pd.DataFrame()

    # ...rest of the existing methods...
    
async def main():
    setor_financeiro = {'BBAS3', 'BBDC3', 'BBDC4', 'BBSE3', 'ITUB4', 'BPAC11', 'ITUB4', 'SANB11', }
    with open('codigos_ibovespa.txt', 'r') as f:
        codigos_ibovespa = f.read().splitlines()

    chrome_driver_path = "/usr/bin/chromedriver"

    service = Service(executable_path=chrome_driver_path)

    options = Options()
    options.add_argument("--headless")  # Executar em modo headless
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-shm-usage")  # Reduz o uso de memória
    options.add_argument("--disable-gpu")  # Desativar o uso de GPU
    options.add_argument("--window-size=1920,1080")  # Definir o tamanho da janela
    scraper = AsyncPrecosRelativosDataScraper(
        setor_financeiro=setor_financeiro,
        options=options,
        service=service,
        acoes=codigos_ibovespa,
        diretorio='../dados/precos_relativos_async.csv',
        max_concurrent=5  # Número máximo de ações processadas simultaneamente
    )
    
    dataframes = scraper.rodar_acoes()
    print("Dados coletados com sucesso!")
    print(dataframes)

if __name__ == "__main__":
    asyncio.run(main())