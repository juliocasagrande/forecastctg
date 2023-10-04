# Importação das bibliotecas
import streamlit as st
import pandas as pd
from datetime import datetime
from azure.storage.blob import BlobServiceClient
import io
st.set_page_config(
        layout='wide',
        page_title='Forecast - Planilha de Controle',
        page_icon='💲'
)

# Dados de login (usuário e senha)
username_valido = "admin"
senha_valida = "admin"

# Função de login
def login():
    # Adicione campos de entrada de usuário e senha
    username = st.text_input("Nome de Usuário")
    senha = st.text_input("Senha", type="password")
    
    if st.button("Login"):
        if username == username_valido and senha == senha_valida:
            st.success('Login efetuado com sucesso!')
            return True
        else:
            st.error("Credenciais inválidas. Tente novamente.")
    return False

# Verificar login
if login():
    # Configurar a string de conexão do Azure Blob Storage
    connection_string = "DefaultEndpointsProtocol=https;AccountName=juliocasagrande27;AccountKey=ILe66QPoZ8QDobUrAv99P/+BuXQpP8BSd6fYGyDd7aFix+Znd7a6LqTh8m/pRfWEPQYTNoMAagoO+AStoczsqw==;EndpointSuffix=core.windows.net"

    # Nome do contêiner e nome do arquivo no Blob Storage
    container_name = "teste"
    file_name = "Forecast_actual.xlsx"  # Substitua pelo nome do seu arquivo XLSX

    # Criar um cliente de serviço de blob
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Obter o contêiner
    container_client = blob_service_client.get_container_client(container_name)

    # Obter o blob (arquivo)
    blob_client = container_client.get_blob_client(file_name)

    # Ler o conteúdo do blob (arquivo) como binário
    blob_data = blob_client.download_blob()
    blob_binary_data = blob_data.readall()

    if "data" not in st.session_state:
        # Converter o conteúdo binário para um DataFrame
        df_original = pd.read_excel(io.BytesIO(blob_binary_data), sheet_name='Resumo CAPEX ')
        df_original.set_index('Projeto ', inplace=True)

        # Carregar os dados do arquivo local no Pandas DataFrame
        df_original = df_original.sort_values(by='FORECAST 2023', ascending=False)
        df_original.replace(0, "", inplace=True)

        # Lista com os nomes das colunas que queremos selecionar
        colunas_selecionadas = [0, 1, 4, 6, 13, 14, 15, 16, 17, 18, 19, 22, 23]

        # Utilizamos o método 'iloc' para selecionar as colunas pelos seus índices
        df_dict = {}
        for col in colunas_selecionadas:
            column_name = df_original.columns[col]
            values = df_original.iloc[:, col]
            df_dict[column_name] = values

        df_dict = pd.DataFrame(df_dict)
        st.session_state["data"] = df_dict
