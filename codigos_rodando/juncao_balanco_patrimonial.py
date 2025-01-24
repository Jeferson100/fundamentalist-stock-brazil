import pandas as pd
import os

df1 = pd.read_csv('../dados/resumo_balanco_ate_100.csv', index_col=0)

print('Carregou df1')

df2 = pd.read_csv('../dados/resumo_balanco_acima_100.csv', index_col=0)

print('Carregou df2')

df_junto = pd.concat([df1, df2])

print('Juntou df1 e df2')

df_junto.to_csv('../dados/resumo_balanco.csv')

print('Salvou df_junto')

os.remove('../dados/resumo_balanco_ate_100.csv')

print('Removeu resumo_balanco_ate_100.csv')

os.remove('../dados/resumo_balanco_acima_100.csv')

print('Removeu resumo_balanco_acima_100.csv')

print('Fim do script')

