
# Fundamentalist Stock Brazil - InvestSite
Este repositório contém scripts para a coleta de dados fundamentais de ações brasileiras a partir do site [InvestSite](https://www.investsite.com.br/) utilizando a biblioteca Selenium. O objetivo é automatizar a extração de dados financeiros importantes para facilitar a análise e tomada de decisões de investimento.

## Dados coletados

Se voce quiser só coletar os dados para a sua analise, a pasta [dados](dados) contém 6 arquivos .csv. Os arquivos são: 
- `capex.csv`

Capex contém os seguintes indicadores: `capex_tres_meses`, `fluxo_caixa_livre_tres_meses`, `capex_doze_meses`, `fluxo_caixa_livre_doze_meses`.

- `retornos_margens.csv`

Retornos Margens contém os seguintes indicadores: `retorno_sobre_capital_tangivel_inicial`, `retorno_sobre_capital_investido_inicial`, `retorno_sobre_capital_investido_inicial`,`retorno_sobre_capital_tangivel_inicial_pre_impostos`,`retorno_sobre_capital_investido_inicial_pre_impostos`, `retorno_sobre_patrimonio_liquido_inicial`,`retorno_sobre_ativo_inicial`, `margem_bruta`, `margem_liquida` ,`margem_ebit`,`margem_ebitda`,`giro_do_ativo_inicial`,`alavancagem_financeira`,`passivo_patrimonio_liquido`,`divida_liquida_ebitda`.

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

## 1. retornos_margens.ipynb
Neste notebook, são coletados e analisados os seguintes indicadores financeiros:

Retorno sobre capital tangível inicial,
Retorno sobre capital investido inicial,
Margens brutas e líquidas,
Margens EBIT e EBITDA,
Giro do ativo inicial,
Alavancagem financeira,
Passivo e patrimônio líquido,
Dívida líquida e EBITDA.
E outros indicadores relevantes.

## 2. dre_trimestre_investsite.ipynb
Neste notebook, são analisados dados do Demonstrativo de Resultado do Exercício (DRE) trimestral obtidos do InvestSite, incluindo:

Receita líquida,
Resultado bruto,
EBIT,
Depreciação e amortização,
EBITDA,
Lucro líquido e 
Lucro por ação

## 3. precos_relativos_invesrsite.ipynb
Neste notebook, são coletados e analisados dados de preços relativos, Market Cap, EV (Enterprise Value) e Dividend Yield, proporcionando informações sobre a avaliação de mercado das empresas.

## 4. resumo_balanço_patrimonial_investsite.ipynb
Neste notebook, são obtidos e analisados dados do balanço patrimonial, incluindo:

Caixa e equivalentes de caixa,
Ativo total,
Dívidas de curto e longo prazo,
Dívida bruta e líquida,
Patrimônio líquido,
Valor patrimonial por ação e
Total de ações ordinárias e preferenciais

## 5. selecionando_dados_juntos.ipynb
Neste notebook, são selecionados e avaliados conjuntos de dados utilizando algoritmos SHAP e Random Forest para identificar as características mais importantes, destacando indicadores relevantes para análises futuras.

Principais Características Identificadas:

High -> 23241.4748 (softmax = 1.0000)

Low -> 20588.7602 (softmax = 0.0000)

Open -> 18922.4840 (softmax = 0.0000)

PE Diário -> 152.5423 (softmax = 0.0000)

Preço da Dívida Líquida Diária -> 115.7628 (softmax = 0.0000)

Porcentagem de Ações Ordinárias -> 114.8245 (softmax = 0.0000)

Preço do Ativo Total Diário -> 106.3465 (softmax = 0.0000)

Margem Líquida -> 105.8848 (softmax = 0.0000)

EV Ativo Total -> 88.1089 (softmax = 0.0000)

Preço Valor Patrimonial Diária -> 63.0183 (softmax = 0.0000)
