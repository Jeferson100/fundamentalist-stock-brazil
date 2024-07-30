
# Fundamentalist Stock Brazil - InvestSite
Este repositório contém análises e dados fundamentais coletados do site InvestSite utilizando a biblioteca Selenium.

# Notebooks:

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
