
# Fundamentalist Stock Brazil - InvestSite

![Fundamentalist Stock Brazil - InvestSite](imagens/touro_urso_gerado.jpg)


Este repositório contém scripts para a coleta de dados fundamentais de ações brasileiras a partir do site [InvestSite](https://www.investsite.com.br/) utilizando a biblioteca Selenium. O objetivo é automatizar a extração de dados financeiros importantes para facilitar a análise e tomada de decisões de investimento.

## Dados coletados

Se voce quiser só coletar os dados para a sua analise, a pasta [dados](dados) contém 6 arquivos .csv. Os arquivos são: 
- `capex.csv`

Capex contém os seguintes indicadores: `capex_tres_meses`, `fluxo_caixa_livre_tres_meses`, `capex_doze_meses`, `fluxo_caixa_livre_doze_meses`.

- `retornos_margens.csv`

Retornos Margens contém os seguintes indicadores: `retorno_sobre_capital_tangivel_inicial`,`retorno_sobre_capital_investido_inicial`, `retorno_sobre_capital_investido_inicial`, `retorno_sobre_capital_tangivel_inicial_pre_impostos`,`retorno_sobre_capital_investido_inicial_pre_impostos`, `retorno_sobre_patrimonio_liquido_inicial`,`retorno_sobre_ativo_inicial`, `margem_bruta`, `margem_liquida` ,`margem_ebit`,`margem_ebitda`,`giro_do_ativo_inicial`,`alavancagem_financeira`,`passivo_patrimonio_liquido`,`divida_liquida_ebitda`.

- `dre.csv`

DRE contém os seguintes indicadores: `receita_liquida`, `resultado_bruto`, `ebit`, `depreciacao_amortizacao`, `ebitda`, `lucro_liquido`, `lucro_por_acao`.

- `precos_relativos.csv`

Precos Relativos contém os seguintes indicadores:`preco_lucro`, `preco_vpa`,`preco_receita_liquida`, `preco_fco`,`preco_fcf`,`preco_ativo_total`,`preco_ebit`,`preco_capital_giro`,`preco_ncav`,`ev_ebit`,`ev_ebitda`,`ev_receita_liquida´ ,ev_fco`,`ev_fcf`,`ev_atito_total`, `market_cap_empresa`,`enterprise_value (ev)`,`dividend_yield`.

- `setor.csv`

Setor contém os seguintes indicadores: `setor`,`segmento_listagem`,`segmento`.

- `resumo_balanço.csv` 

Resumo contém os seguintes indicadores: `caixa_equivalentes_caixa`, `ativo_total`, `dividas_curto_prazo`, `divida_longo_prazo`, `divida_bruta`, `divida_liquida`, `patrimonio_liquido`, `valor_patrimonial_acao`, `acoes_ordinarias`, `acoes_preferenciais`, `total`.

- `fluxo_caixa.csv`

Fluxo de caixa contém os seguintes indicadores: `fluxo_caixa_operacional`, `fluxo_caixa_investimentos`, `fluxo_caixa_financiamento`, `aumento_reducao_caixa_equivalentes`



Os arquivos contêm dados de 71 ações, que são as seguintes:

`ABEV3`, `AZUL4`, `B3SA3`, `BBAS3`, `BBDC3`, `BBDC4`, `BBSE3`, `BEEF3`, `BPAC11`, `BRAP4`, `BRFS3`, `BRKM5`, `CCRO3`, `CIEL3`, `CMIG4`, `COGN3`, `CPFE3`, `CRFB3`, `CSAN3`, `CSNA3  `, `CVCB3`, `CYRE3`, `ECOR3`, `EGIE3`, `ELET3`, `ELET6`, `EMBR3`, `ENGI11`, `EQTL3`, `EZTC3 `, `FLRY3`, `GGBR4`, `GOAU4`, `GOLL4`, `HAPV3`, `HYPE3`, `IRBR3`, `ITSA4`, `ITUB4`, `JBSS3`, `KLBN11`, `LREN3`, `MGLU3`, `MRFG3`, `MRVE3`, `MULT3`, `NTCO3`, `PCAR3`, `PETR3`, `PETR4`, `PRIO3`, `QUAL3`, `RADL3`, `RAIL3`, `RENT3`, `SANB11`, `SBSP3`, `SUZB3`, `TAEE11`, `TIMS3`, `TOTS3`, `UGPA3`, `USIM5`, `VALE3`, `VIVT3`, `WEGE3`, `WIZC3`, `YDUQ3`, `SOMA3`, `BPAC11`, `MDIA3`




# Instruções

Para usar este projeto, execute os comandos abaixo:

1. Clone este repositório:

```bash
git clone git@github.com:Jeferson100/fundamentalist-stock-brazil.git

cd fundamentalist-stock-brazil

```
2. Instale os pacotes necessários:

```bash
pip install -r requirements.txt
```
3. Configure o Selenium:

Baixe o driver do navegador correspondente ao navegador que você planeja usar  e adicione-o ao seu PATH. No meu caso usei o [Chrome](https://chromedriver.chromium.org/downloads).


# Usando o Projeto

## Classe TabelaResumoDataScraper

A classe `TabelaResumoDataScraper` é responsável por coletar os dados da tabela de resumo do balanço patrimonial. Para ver um exemplo de como usar a classe, verifique o arquivo [rodando_balanco_patrimonial.py](codigos_rodando/rodando_balanco_patrimonial.py).

### Exemplo de Uso

```python
import sys
sys.path.append('..')
from FundamentsStockBrazil.BalanceSheet import TabelaResumoDataScraper
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Lista de ações a serem processadas
acoes = ['ABEV3', 'AZUL4', 'B3SA3']

# Definição do setor financeiro
setor_financeiro = {'BBAS3', 'BBDC3', 'BBDC4', 'BBSE3', 'ITUB4', 'BPAC11', 'ITUB4', 'SANB11', 'IRBR3'}

# Caminho para o driver do Chrome
chrome_driver_path = "/usr/bin/chromedriver"

# Configuração do serviço do Chrome
service = Service(executable_path=chrome_driver_path)

# Configurações do Chrome
options = Options()
options.add_argument("--headless")  # Executar em modo headless
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")  # Reduzir o uso de memória
options.add_argument("--disable-gpu")  # Desativar o uso de GPU
options.add_argument("--window-size=1920,1080")  # Definir o tamanho da janela

# Inicializa o scraper
scraper = TabelaResumoDataScraper(setor_financeiro, options, service, acoes=acoes, diretorio='../dados/resumo_balanco.csv')

# Executa a coleta de dados
dados = scraper.rodar_acoes()

# Salva os dados em um arquivo CSV
dados.to_csv('../dados/resumo_balanco.csv')

```
**Saida da execução:**
```
Tempo de execução da ação ABEV3: 1.13 minutos

Tempo de execução da ação AZUL4: 0.70 minutos

Tempo de execução da ação B3SA3: 1.53 minutos
```
**Arquivo de saida:**


<div>
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>datas</th>
      <th>caixa_equivalentes_caixa</th>
      <th>ativo_total</th>
      <th>divida_curto_prazo</th>
      <th>divida_longo_prazo</th>
      <th>divida_bruta</th>
      <th>divida_liquida</th>
      <th>patrimonio_liquido</th>
      <th>valor_patrimonial_acao</th>
      <th>acoes_ordinarias</th>
      <th>acoes_preferenciais</th>
      <th>total</th>
      <th>tic</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>30/06/2024</td>
      <td>14150.0</td>
      <td>143440.0</td>
      <td>1240.00</td>
      <td>2210.00</td>
      <td>3460.00</td>
      <td>-10700.0</td>
      <td>95260.0</td>
      <td>6.05</td>
      <td>15.757.657.000</td>
      <td>0</td>
      <td>15.757.657.000</td>
      <td>ABEV3</td>
    </tr>
    <tr>
      <th>1</th>
      <td>31/03/2024</td>
      <td>12840.0</td>
      <td>133820.0</td>
      <td>1650.00</td>
      <td>2170.00</td>
      <td>3820.00</td>
      <td>-9030.0</td>
      <td>86590.0</td>
      <td>5.50</td>
      <td>15.757.657.000</td>
      <td>0</td>
      <td>15.757.657.000</td>
      <td>ABEV3</td>
    </tr>
    <tr>
      <th>2</th>
      <td>31/12/2023</td>
      <td>16060.0</td>
      <td>132640.0</td>
      <td>1300.00</td>
      <td>2200.00</td>
      <td>3500.00</td>
      <td>-12560.0</td>
      <td>78970.0</td>
      <td>5.01</td>
      <td>15.753.833.000</td>
      <td>0</td>
      <td>15.753.833.000</td>
      <td>ABEV3</td>
    </tr>
    <tr>
      <th>3</th>
      <td>30/09/2023</td>
      <td>17410.0</td>
      <td>137910.0</td>
      <td>1240.00</td>
      <td>2480.00</td>
      <td>3720.00</td>
      <td>-13700.0</td>
      <td>90250.0</td>
      <td>5.73</td>
      <td>15.753.833.000</td>
      <td>0</td>
      <td>15.753.833.000</td>
      <td>ABEV3</td>
    </tr>
    <tr>
      <th>4</th>
      <td>30/06/2023</td>
      <td>12120.0</td>
      <td>133290.0</td>
      <td>1320.00</td>
      <td>2670.00</td>
      <td>3990.00</td>
      <td>-8120.0</td>
      <td>85070.0</td>
      <td>5.40</td>
      <td>15.753.833.000</td>
      <td>0</td>
      <td>15.753.833.000</td>
      <td>ABEV3</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>59</th>
      <td>30/06/2009</td>
      <td>2340.0</td>
      <td>20940.0</td>
      <td>8.22</td>
      <td>8.23</td>
      <td>16.45</td>
      <td>-2320.0</td>
      <td>19560.0</td>
      <td>9.57</td>
      <td>2.044.014.295</td>
      <td>0</td>
      <td>2.044.014.295</td>
      <td>B3SA3</td>
    </tr>
    <tr>
      <th>60</th>
      <td>31/03/2009</td>
      <td>2590.0</td>
      <td>21200.0</td>
      <td>3.57</td>
      <td>NaN</td>
      <td>3.57</td>
      <td>-2590.0</td>
      <td>19460.0</td>
      <td>9.52</td>
      <td>2.044.014.295</td>
      <td>0</td>
      <td>2.044.014.295</td>
      <td>B3SA3</td>
    </tr>
    <tr>
      <th>61</th>
      <td>31/12/2008</td>
      <td>1780.0</td>
      <td>20430.0</td>
      <td>4.09</td>
      <td>NaN</td>
      <td>4.09</td>
      <td>-1780.0</td>
      <td>19290.0</td>
      <td>9.44</td>
      <td>2.044.014.295</td>
      <td>0</td>
      <td>2.044.014.295</td>
      <td>B3SA3</td>
    </tr>
    <tr>
      <th>62</th>
      <td>30/09/2008</td>
      <td>2060.0</td>
      <td>20750.0</td>
      <td>148.24</td>
      <td>NaN</td>
      <td>148.24</td>
      <td>-1910.0</td>
      <td>19530.0</td>
      <td>9.56</td>
      <td>2.044.014.295</td>
      <td>0</td>
      <td>2.044.014.295</td>
      <td>B3SA3</td>
    </tr>
    <tr>
      <th>63</th>
      <td>30/06/2008</td>
      <td>2800.0</td>
      <td>21270.0</td>
      <td>502.73</td>
      <td>NaN</td>
      <td>502.73</td>
      <td>-2300.0</td>
      <td>19630.0</td>
      <td>9.62</td>
      <td>2.040.797.995</td>
      <td>0</td>
      <td>2.040.797.995</td>
      <td>B3SA3</td>
    </tr>
  </tbody>
</table>
<p>141 rows × 13 columns</p>
</div>



## Classe DreDataScraper

A classe `DreDataScraper` é responsável por coletar os dados da tabela de DRE. Para ver um exemplo de como usar a classe, verifique o arquivo [rodando_dre.py](codigos_rodando/rodando_dre.py).

### Exemplo de Uso

```python
import sys
sys.path.append('..')
from FundamentsStockBrazil.IncomeStatement import DreDataScraper
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Lê os códigos das ações do Ibovespa a partir de um arquivo
acoes = ['ABEV3', 'AZUL4', 'B3SA3']

# Define o setor financeiro
setor_financeiro = {'BBAS3', 'BBDC3', 'BBDC4', 'BBSE3', 'ITUB4', 'BPAC11', 'SANB11', 'IRBR3'}

# Caminho para o driver do Chrome
chrome_driver_path = "/usr/bin/chromedriver"

# Configuração do serviço do Chrome
service = Service(executable_path=chrome_driver_path)

# Configurações do Chrome
options = Options()
options.add_argument("--headless")  # Executar em modo headless
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")  # Reduz o uso de memória
options.add_argument("--disable-gpu")  # Desativar o uso de GPU
options.add_argument("--window-size=1920,1080")  # Definir o tamanho da janela

# Inicializa o scraper
scraper = DreDataScraper(setor_financeiro, options, service, acoes=codigos_ibovespa, diretorio='../dados/dre.csv')

# Executa a coleta de dados
dados = scraper.rodar_acoes()

# Salva os dados em um arquivo CSV
dados.to_csv('../dados/dre.csv')

```
**Saida da execução**

```
Tempo de execução da ação ABEV3: 0.73 minutos
Tempo de execução da ação AZUL4: 0.48 minutos
Tempo de execução da ação B3SA3: 1.16 minutos

```
**Arquivo de saida:**

<div>
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>datas</th>
      <th>receita_liquida</th>
      <th>resultado_bruto</th>
      <th>ebit</th>
      <th>depreciacao_amortizacao</th>
      <th>ebitda</th>
      <th>lucro_liquido</th>
      <th>lucro_por_acao</th>
      <th>tic</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>30/06/2024</td>
      <td>20040.00</td>
      <td>9980.00</td>
      <td>4050.00</td>
      <td>-1620.0</td>
      <td>5660.0</td>
      <td>2400.00</td>
      <td>0.15</td>
      <td>ABEV3</td>
    </tr>
    <tr>
      <th>1</th>
      <td>31/03/2024</td>
      <td>20280.00</td>
      <td>10220.00</td>
      <td>4880.00</td>
      <td>-1570.0</td>
      <td>6450.0</td>
      <td>3700.00</td>
      <td>0.23</td>
      <td>ABEV3</td>
    </tr>
    <tr>
      <th>2</th>
      <td>31/12/2023</td>
      <td>19990.00</td>
      <td>10690.00</td>
      <td>5430.00</td>
      <td>-1400.0</td>
      <td>6820.0</td>
      <td>4390.00</td>
      <td>0.28</td>
      <td>ABEV3</td>
    </tr>
    <tr>
      <th>3</th>
      <td>30/09/2023</td>
      <td>20320.00</td>
      <td>10090.00</td>
      <td>4900.00</td>
      <td>-1590.0</td>
      <td>6480.0</td>
      <td>3910.00</td>
      <td>0.25</td>
      <td>ABEV3</td>
    </tr>
    <tr>
      <th>4</th>
      <td>30/06/2023</td>
      <td>18900.00</td>
      <td>9260.00</td>
      <td>3450.00</td>
      <td>-1580.0</td>
      <td>5020.0</td>
      <td>2500.00</td>
      <td>0.16</td>
      <td>ABEV3</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>59</th>
      <td>30/06/2009</td>
      <td>378.24</td>
      <td>378.24</td>
      <td>250.04</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>188.13</td>
      <td>0.09</td>
      <td>B3SA3</td>
    </tr>
    <tr>
      <th>60</th>
      <td>31/03/2009</td>
      <td>316.55</td>
      <td>316.55</td>
      <td>167.79</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>226.98</td>
      <td>0.11</td>
      <td>B3SA3</td>
    </tr>
    <tr>
      <th>61</th>
      <td>31/12/2008</td>
      <td>370.44</td>
      <td>370.44</td>
      <td>69.50</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>115.39</td>
      <td>0.06</td>
      <td>B3SA3</td>
    </tr>
    <tr>
      <th>62</th>
      <td>30/09/2008</td>
      <td>404.68</td>
      <td>404.68</td>
      <td>97.46</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>200.97</td>
      <td>0.10</td>
      <td>B3SA3</td>
    </tr>
    <tr>
      <th>63</th>
      <td>30/06/2008</td>
      <td>826.90</td>
      <td>826.90</td>
      <td>386.98</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>329.24</td>
      <td>0.16</td>
      <td>B3SA3</td>
    </tr>
  </tbody>
</table>
<p>141 rows × 9 columns</p>
</div>

## Classe CapexDataScraper

A classe `CapexDataScraper` é responsável por fazer o web scraping dos dados do Capex. Para ver um exemplo de como usar a classe, verifique o arquivo [rodando_capex.py](codigos_rodando/rodando_capex.py).

### Exemplo de Uso

```python
import sys
sys.path.append('..')
from FundamentsStockBrazil.CapitalExpenditure import CapexDataScraper
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Lê os códigos das ações do Ibovespa a partir de um arquivo
codigos_ibovespa = ['ABEV3', 'AZUL4', 'B3SA3']

# Define o setor financeiro
setor_financeiro = {'BBAS3', 'BBDC3', 'BBDC4', 'BBSE3', 'ITUB4', 'BPAC11', 'SANB11', 'IRBR3'}

# Caminho para o driver do Chrome
chrome_driver_path = "/usr/bin/chromedriver"

# Configuração do serviço do Chrome
service = Service(executable_path=chrome_driver_path)

# Configurações do Chrome
options = Options()
options.add_argument("--headless")  # Executar em modo headless
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")  # Reduz o uso de memória
options.add_argument("--disable-gpu")  # Desativar o uso de GPU
options.add_argument("--window-size=1920,1080")  # Definir o tamanho da janela

# Inicializa o scraper
scraper = CapexDataScraper(setor_financeiro, options, service, acoes=codigos_ibovespa, diretorio='../dados/capex.csv')

# Executa a coleta de dados
dados = scraper.rodar_acoes()

# Salva os dados em um arquivo CSV
dados.to_csv('../dados/capex.csv')

```

**Saida da execução**

```
Tempo de execução da ação ABEV3: 0.72 minutos
Tempo de execução da ação AZUL4: 0.45 minutos
Tempo de execução da ação B3SA3: 0.76 minutos

```
**Arquivo de saida:**
<div>
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>datas</th>
      <th>capex_tres_meses</th>
      <th>fluxo_caixa_livre_tres_meses</th>
      <th>capex_doze_meses</th>
      <th>fluxo_caixa_livre_doze_meses</th>
      <th>tic</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>30/06/2024</td>
      <td>-973.35</td>
      <td>2380.00</td>
      <td>-5410.00</td>
      <td>20540.0</td>
      <td>ABEV3</td>
    </tr>
    <tr>
      <th>1</th>
      <td>31/03/2024</td>
      <td>-979.68</td>
      <td>-261.48</td>
      <td>-5700.00</td>
      <td>20310.0</td>
      <td>ABEV3</td>
    </tr>
    <tr>
      <th>2</th>
      <td>31/12/2023</td>
      <td>-2200.00</td>
      <td>11750.00</td>
      <td>-5850.00</td>
      <td>18860.0</td>
      <td>ABEV3</td>
    </tr>
    <tr>
      <th>3</th>
      <td>30/09/2023</td>
      <td>-1260.00</td>
      <td>6670.00</td>
      <td>-5650.00</td>
      <td>16930.0</td>
      <td>ABEV3</td>
    </tr>
    <tr>
      <th>4</th>
      <td>30/06/2023</td>
      <td>-1260.00</td>
      <td>2150.00</td>
      <td>-6210.00</td>
      <td>14550.0</td>
      <td>ABEV3</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>48</th>
      <td>31/03/2012</td>
      <td>-2.57</td>
      <td>218.06</td>
      <td>-37.57</td>
      <td>1570.0</td>
      <td>B3SA3</td>
    </tr>
    <tr>
      <th>49</th>
      <td>31/12/2011</td>
      <td>-11.40</td>
      <td>252.89</td>
      <td>-41.04</td>
      <td>1640.0</td>
      <td>B3SA3</td>
    </tr>
    <tr>
      <th>50</th>
      <td>30/09/2011</td>
      <td>-10.90</td>
      <td>584.01</td>
      <td>-119.12</td>
      <td>1970.0</td>
      <td>B3SA3</td>
    </tr>
    <tr>
      <th>51</th>
      <td>30/06/2011</td>
      <td>-12.70</td>
      <td>519.22</td>
      <td>-121.18</td>
      <td>1800.0</td>
      <td>B3SA3</td>
    </tr>
    <tr>
      <th>52</th>
      <td>31/03/2011</td>
      <td>-6.04</td>
      <td>287.16</td>
      <td>-148.67</td>
      <td>1790.0</td>
      <td>B3SA3</td>
    </tr>
  </tbody>
</table>
<p>130 rows × 6 columns</p>
</div>

## Classe PrecosRelativosDataScraper

A classe `PrecosRelativosDataScraper` tem como objetivo baixar dados de indicadores de precos relativos. Para um exemplo de como usar a classe, veja o arquivo [rodando_precos_relativos.py](codigos_rodando/rodando_precos_relativos.py).

```python
import sys
sys.path.append('..')
from FundamentsStockBrazil.RelativePrices import PrecosRelativosDataScraper
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Lista de códigos das ações do Ibovespa
codigos_ibovespa = ['ABEV3', 'AZUL4', 'B3SA3']

# Define o setor financeiro
setor_financeiro = {'BBAS3', 'BBDC3', 'BBDC4', 'BBSE3', 'ITUB4', 'BPAC11', 'SANB11', 'IRBR3'}

# Caminho para o driver do Chrome
chrome_driver_path = "/usr/bin/chromedriver"

# Configuração do serviço do Chrome
service = Service(executable_path=chrome_driver_path)

# Configurações do Chrome
options = Options()
options.add_argument("--headless")  # Executar em modo headless
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")  # Reduz o uso de memória
options.add_argument("--disable-gpu")  # Desativar o uso de GPU
options.add_argument("--window-size=1920,1080")  # Definir o tamanho da janela

# Inicializa o scraper
scraper = PrecosRelativosDataScraper(setor_financeiro, options, service, acoes=codigos_ibovespa, diretorio='../dados/precos_relativos.csv')

# Executa a coleta de dados
dados = scraper.rodar_acoes()

# Salva os dados em um arquivo CSV
dados.to_csv('../dados/precos_relativos.csv')
```

**Saida da execução**

```
Tempo de execução da ação ABEV3: 1.14 minutos
Tempo de execução da ação AZUL4: 0.74 minutos
Tempo de execução da ação B3SA3: 1.52 minutos
```

<div>
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>datas</th>
      <th>preco_lucro</th>
      <th>preco_vpa</th>
      <th>preco_receita_liquida</th>
      <th>preco_fco</th>
      <th>preco_fcf</th>
      <th>preco_ativo_total</th>
      <th>preco_ebit</th>
      <th>preco_capital_giro</th>
      <th>preco_ncav</th>
      <th>ev_ebit</th>
      <th>ev_ebitda</th>
      <th>ev_receita_liquida</th>
      <th>ev_fco</th>
      <th>ev_fcf</th>
      <th>ev_atito_total</th>
      <th>market_cap_empresa</th>
      <th>enterprise_value</th>
      <th>dividend_yield</th>
      <th>tic</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>02/08/2024</td>
      <td>12.99</td>
      <td>1.96</td>
      <td>2.32</td>
      <td>7.21</td>
      <td>9.11</td>
      <td>1.30</td>
      <td>9.71</td>
      <td>50.58</td>
      <td>-4.21</td>
      <td>9.16</td>
      <td>6.94</td>
      <td>2.19</td>
      <td>6.80</td>
      <td>8.59</td>
      <td>1.23</td>
      <td>187040.0</td>
      <td>176350.0</td>
      <td>0.0615</td>
      <td>ABEV3</td>
    </tr>
    <tr>
      <th>1</th>
      <td>30/06/2024</td>
      <td>12.85</td>
      <td>1.94</td>
      <td>2.29</td>
      <td>7.13</td>
      <td>9.01</td>
      <td>1.29</td>
      <td>9.61</td>
      <td>50.02</td>
      <td>-4.16</td>
      <td>9.05</td>
      <td>6.86</td>
      <td>2.16</td>
      <td>6.72</td>
      <td>8.49</td>
      <td>1.22</td>
      <td>184990.0</td>
      <td>174300.0</td>
      <td>0.0622</td>
      <td>ABEV3</td>
    </tr>
    <tr>
      <th>2</th>
      <td>31/03/2024</td>
      <td>13.22</td>
      <td>2.21</td>
      <td>2.41</td>
      <td>7.37</td>
      <td>9.44</td>
      <td>1.43</td>
      <td>10.28</td>
      <td>-809.80</td>
      <td>-4.04</td>
      <td>9.80</td>
      <td>7.38</td>
      <td>2.30</td>
      <td>7.03</td>
      <td>9.00</td>
      <td>1.37</td>
      <td>191770.0</td>
      <td>182740.0</td>
      <td>0.0600</td>
      <td>ABEV3</td>
    </tr>
    <tr>
      <th>3</th>
      <td>31/12/2023</td>
      <td>13.67</td>
      <td>2.51</td>
      <td>2.49</td>
      <td>8.02</td>
      <td>10.51</td>
      <td>1.49</td>
      <td>10.63</td>
      <td>-44.62</td>
      <td>-3.41</td>
      <td>9.96</td>
      <td>7.53</td>
      <td>2.33</td>
      <td>7.51</td>
      <td>9.84</td>
      <td>1.40</td>
      <td>198180.0</td>
      <td>185630.0</td>
      <td>0.0580</td>
      <td>ABEV3</td>
    </tr>
    <tr>
      <th>4</th>
      <td>30/09/2023</td>
      <td>13.43</td>
      <td>2.24</td>
      <td>2.46</td>
      <td>8.97</td>
      <td>11.97</td>
      <td>1.47</td>
      <td>10.88</td>
      <td>54.65</td>
      <td>-4.61</td>
      <td>10.14</td>
      <td>7.64</td>
      <td>2.29</td>
      <td>8.37</td>
      <td>11.16</td>
      <td>1.37</td>
      <td>202590.0</td>
      <td>188900.0</td>
      <td>0.0593</td>
      <td>ABEV3</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>60</th>
      <td>30/06/2009</td>
      <td>70.40</td>
      <td>2.68</td>
      <td>36.01</td>
      <td>33.08</td>
      <td>34.12</td>
      <td>2.51</td>
      <td>87.62</td>
      <td>38.74</td>
      <td>-2.138.78</td>
      <td>83.74</td>
      <td>NA</td>
      <td>34.41</td>
      <td>31.62</td>
      <td>32.61</td>
      <td>2.39</td>
      <td>52450.0</td>
      <td>50130.0</td>
      <td>0.0176</td>
      <td>B3SA3</td>
    </tr>
    <tr>
      <th>61</th>
      <td>31/03/2009</td>
      <td>60.11</td>
      <td>2.69</td>
      <td>27.34</td>
      <td>25.94</td>
      <td>26.67</td>
      <td>2.47</td>
      <td>72.67</td>
      <td>46.12</td>
      <td>-86.97</td>
      <td>69.09</td>
      <td>NA</td>
      <td>25.99</td>
      <td>24.66</td>
      <td>25.36</td>
      <td>2.35</td>
      <td>52450.0</td>
      <td>49860.0</td>
      <td>0.0176</td>
      <td>B3SA3</td>
    </tr>
    <tr>
      <th>62</th>
      <td>31/12/2008</td>
      <td>81.24</td>
      <td>2.72</td>
      <td>32.74</td>
      <td>26.84</td>
      <td>27.53</td>
      <td>2.57</td>
      <td>94.69</td>
      <td>58.95</td>
      <td>-210.94</td>
      <td>91.47</td>
      <td>NA</td>
      <td>31.63</td>
      <td>25.93</td>
      <td>26.59</td>
      <td>2.48</td>
      <td>52450.0</td>
      <td>50670.0</td>
      <td>0.0176</td>
      <td>B3SA3</td>
    </tr>
    <tr>
      <th>63</th>
      <td>30/09/2008</td>
      <td>NA</td>
      <td>2.69</td>
      <td>NA</td>
      <td>NA</td>
      <td>NA</td>
      <td>2.53</td>
      <td>NA</td>
      <td>40.42</td>
      <td>688.87</td>
      <td>NA</td>
      <td>NA</td>
      <td>NA</td>
      <td>NA</td>
      <td>NA</td>
      <td>2.44</td>
      <td>52450.0</td>
      <td>50540.0</td>
      <td>0.0176</td>
      <td>B3SA3</td>
    </tr>
    <tr>
      <th>64</th>
      <td>30/06/2008</td>
      <td>NA</td>
      <td>2.67</td>
      <td>NA</td>
      <td>NA</td>
      <td>NA</td>
      <td>2.46</td>
      <td>NA</td>
      <td>33.22</td>
      <td>-770.99</td>
      <td>NA</td>
      <td>NA</td>
      <td>NA</td>
      <td>NA</td>
      <td>NA</td>
      <td>2.35</td>
      <td>52370.0</td>
      <td>50070.0</td>
      <td>0.0176</td>
      <td>B3SA3</td>
    </tr>
  </tbody>
</table>
<p>144 rows × 20 columns</p>
</div>






