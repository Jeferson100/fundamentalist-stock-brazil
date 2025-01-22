#!/usr/bin/env python
import sys
sys.path.append('..')
from FundamentsStockBrazil.BalanceSheet import TabelaResumoDataScraper
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

with open('codigos_ibovespa.txt', 'r') as f:
    codigos_ibovespa = f.read().splitlines()
codigos_ibovespa = codigos_ibovespa[:150]

setor_financeiro = {'BBAS3', 'BBDC3', 'BBDC4', 'BBSE3', 'ITUB4', 'BPAC11', 'ITUB4', 'SANB11'}

chrome_driver_path = "/usr/bin/chromedriver"

service = Service(executable_path=chrome_driver_path)

options = Options()
options.add_argument("--headless")  # Executar em modo headless
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-dev-shm-usage")  # Reduz o uso de memória
options.add_argument("--disable-gpu")  # Desativar o uso de GPU
options.add_argument("--window-size=1920,1080")  # Definir o tamanho da janela

scraper = TabelaResumoDataScraper(setor_financeiro, options, acoes=codigos_ibovespa, diretorio='../dados/resumo_balanco.csv')

dados = scraper.rodar_acoes()

dados.to_csv('../dados/resumo_balanco.csv')

