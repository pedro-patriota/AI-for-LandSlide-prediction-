import pandas as pd

df_calls = pd.read_csv("processing/merge/correct_column.csv")
df_type = pd.read_csv("processing/merge/tipo_ocorrencia.csv",
                 delimiter=';')


inner_merged  = pd.merge(df_calls, df_type)
inner_merged.to_csv(r'C:\Users\parae\Documents\barreiras_prev\processing\merged.csv',
          index=False, header=True)


inner_merged = inner_merged.loc[inner_merged['solicitacao_descricao'] != 'teste']


confirmado = []
for row in inner_merged['processo_ocorrencia']:
    if row == 'Deslizamentos de Barreiras' :    confirmado.append('1')
    elif row == 'Não há Ocorrência para essa Solicitação' :    confirmado.append('2')
    else:           confirmado.append('0')

inner_merged['confirmado'] = confirmado

print(inner_merged.head())

print(inner_merged['confirmado'].value_counts(dropna=False))

inner_merged.to_csv(r'C:\Users\parae\Documents\barreiras_prev\processing\location\merged.csv',
          index=False, header=True)


