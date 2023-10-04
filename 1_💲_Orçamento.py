# Importação das bibliotecas
import streamlit as st
import pandas as pd
from datetime import datetime
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# Configuração da página
st.set_page_config(
    layout='wide',
    page_title='Forecast - Planilha de Controle',
    page_icon='💲'
)

# Inserindo string de conexão
connection_string = "DefaultEndpointsProtocol=https;AccountName=juliocasagrande27;AccountKey=ILe66QPoZ8QDobUrAv99P/+BuXQpP8BSd6fYGyDd7aFix+Znd7a6LqTh8m/pRfWEPQYTNoMAagoO+AStoczsqw==;EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Nome do container e nome do arquivo no Blob Storage
container_name = "teste"
file_name = "Forecast_actual.xlsx"

# Carregar o arquivo do Blob Storage
container_client = blob_service_client.get_container_client(container_name)
blob_client = container_client.get_blob_client(file_name)

# Baixar o arquivo para um arquivo temporário local
temp_file_path = "temp_file.xlsx"
with open(temp_file_path, "wb") as file:
    blob_data = blob_client.download_blob()
    file.write(blob_data.readall())

# Carregar os dados do arquivo local no Pandas DataFrame
df_original = pd.read_excel(temp_file_path, sheet_name='Resumo CAPEX ')
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