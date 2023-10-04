# Importação das bibliotecas
import streamlit as st
import pandas as pd
from datetime import datetime
from azure.storage.blob import BlobServiceClient
import io
st.set_page_config(
        layout='wide',
        page_title='Forecast - Planilha de Controle',
        page_icon='💲')

# Obter a data atual
data_atual = datetime.now()

# Formatando a data para o formato DD/MM/AA
hoje = data_atual.strftime('%d/%m/%y')

# Formatando a hora para o formato HH:MM
hora_atual = data_atual.strftime('%H:%M')

df_dict = st.session_state['data']

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