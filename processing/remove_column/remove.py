import pandas as pd


my_column = ["processo_numero", "solicitacao_data",
            "solicitacao_hora", "solicitacao_descricao",
            "solicitacao_bairro", "solicitacao_localidade", 
            "solicitacao_endereco"]

df = pd.read_csv("processing/remove_column/sedec_chamados.csv",
                 usecols=my_column,

                 delimiter=';')



df.dropna(inplace=True)
print(df.info())

# solicitacao_vitimas = pd.get_dummies(df["solicitacao_vitimas"], drop_first=True) ----- Pode ser usado para medir o nivel de perigo, por enquanto nao serve tanto
#df = pd.concat([df, solicitacao_vitimas], axis=1)
df.to_csv(r'C:\Users\parae\Documents\barreiras_prev\processing\merge\correct_column.csv',
          index=False, header=True)
