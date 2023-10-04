# Importação das bibliotecas
import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da página
st.set_page_config(
    layout='wide',
    page_title='Forecast - Planilha de Controle',
    page_icon='💲'
)

# Carregar os dados e ordenar pelo Forecast 2023
df_original = pd.read_excel(r"C:\Users\jlcasagrande\AppData\Roaming\Python\Python311\Scripts\Projetos Python\Orçamento_Streamlit\Forecast_actual.xlsx", sheet_name='Resumo CAPEX ')
df_original = df_original.sort_values(by='FORECAST 2023', ascending=False)

# Lista com os nomes das colunas que queremos selecionar
colunas_selecionadas = [0, 1, 4, 6, 13, 14, 15, 16, 17, 18, 19, 23]

# Utilizamos o método 'iloc' para selecionar as colunas pelos seus índices
df_dict = {}
for col in colunas_selecionadas:
    column_name = df_original.columns[col]
    values = df_original.iloc[:, col]
    df_dict[column_name] = values

# Formatar as colunas financeiras para duas casas decimais
colunas_financeiras = ['FORECAST 2023', 'FORECAST 2024', 'FORECAST 2025', 'FORECAST 2026', 'FORECAST 2027',
                       'FORECAST 2028', 'TOTAL FORECAST', 'SAP/SI', 'REALIZADO TOTAL']

for col in colunas_financeiras:
    df_dict[col] = df_dict[col].apply(lambda x: round(max(0, x), 2))

# Obter a data atual
data_atual = datetime.now()

# Formatando a data para o formato DD/MM/AA
hoje = data_atual.strftime('%d/%m/%y')

# Formatando a hora para o formato HH:MM
hora_atual = data_atual.strftime('%H:%M')

# Montagem do Layout
st.title('Orçamento Engenharia Eletromecânica - CTG Br')
st.write(f"Atualizado em: {hoje} às {hora_atual} hs")
df_dict = pd.DataFrame(df_dict)

uhe = st.sidebar.selectbox('Selecione a UHE', ["TODAS"] + df_dict['UHE'].unique().tolist())

if uhe == "TODAS":
    df_dict
else:
    df_dict_filtrado = df_dict[df_dict['UHE'] == uhe]
    df_dict_filtrado