import streamlit as st
from azure.storage.blob import BlobServiceClient
import pyodbc
import uuid
import json
import os
import pandas as pd


# Configurações do Azure Storage
CONNECTION_STRING = "DefaultEndpointsProtocol=https;[...];EndpointSuffix=core.windows.net"
CONTAINER_NAME = "fotos"
ACCOUNT_NAME = "stadevlab01ecommerce"

# Configurações do Azure SQL Server
SQL_SERVER   = "dblab01.database.windows.net"
SQL_DATABASE = "sqllab01ecommerce"
SQL_USERNAME = "adminpaulinomendes01"
SQL_PASSWORD = "0db7:5DH@n>N"


# Título da aplicação
st.title("Cadastro de Produto - E-Commerce na Cloud")


# Formulário para cadastro do produto
product_name = st.text_input("Nome do Produto")
description = st.text_area("Descrição do Produto")
price = st.number_input("Preço do Produto", min_value=0.0, format="%.2f")
uploaded_file = st.file_uploader("Imagem do Produto", type=["png", "jpg", "jpeg"])


# Função para gerar a string de conexão com o Azure SQL Server
def get_sql_connection_string():
    return (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={SQL_SERVER};"
        f"DATABASE={SQL_DATABASE};"
        f"UID={SQL_USERNAME};"
        f"PWD={SQL_PASSWORD};"
    )


# Função para enviar imagem para o Azure Blob Storage
def upload_image(file):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)

        # Cria um nome único para a imagem
        blob_name = f"{uuid.uuid4()}.jpg"
        blob_client = container_client.get_blob_client(blob_name)

        # Faz o upload da imagem
        blob_client.upload_blob(file.read(), overwrite=True)

        # Monta a URL de acesso à imagem
        image_url = f"https://{ACCOUNT_NAME}.blob.core.windows.net/{CONTAINER_NAME}/{blob_name}"
        return image_url
    except Exception as e:
        st.error(f"Erro ao enviar imagem: {e}")
        return None


# Função para inserir os dados do produto no Azure SQL Server usando pyodbc
def insert_product_sql(product_data):
    conn = None
    try:
        conn_str = get_sql_connection_string()
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Insere os dados do produto
        insert_query = """
        INSERT INTO dbo.Produtos (nome, descricao, preco, imagem_url)
        VALUES (?, ?, ?, ?)
        """
        cursor.execute(insert_query, (product_data["nome"], product_data["descricao"], product_data["preco"], product_data["imagem_url"]))
        conn.commit()

        cursor.close()
        return True
    except pyodbc.Error as e:
        st.error(f"Erro ao inserir no Azure SQL: {e}")
        return False
    finally:
        if conn:
            conn.close()


# Função para listar os produtos do Azure SQL Server usando pyodbc
def list_products_sql():
    conn = None
    try:
        conn_str = get_sql_connection_string()
        conn = pyodbc.connect(conn_str)
        
        # Busca os dados dos produtos
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, descricao, preco, imagem_url FROM dbo.Produtos")
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

        cursor.close()
        return rows
    except pyodbc.Error as e:
        st.error(f"Erro ao listar produtos: {e}")
        return []
    finally:
        if conn:
            conn.close()


# Função para exibir a lista de produtos na tela   
def list_produtos_screen():
        products = list_products_sql()
        if products:
        # Define o número de cards por linha
            cards_por_linha = 3
            # Cria as colunas iniciais
            cols = st.columns(cards_por_linha)
            for i, product in enumerate(products):
                col = cols[i % cards_por_linha]
                with col:
                    st.markdown(f"### {product['nome']}")
                    st.write(f"**Descrição:** {product['descricao']}")
                    st.write(f"**Preço:** R$ {product['preco']:.2f}")
                    if product["imagem_url"]:
                        html_img = f'<img src="{product["imagem_url"]}" width="200" height="200" alt="Imagem do produto">'
                        st.markdown(html_img, unsafe_allow_html=True)
                    st.markdown("---")
                # A cada 'cards_por_linha' produtos, se ainda houver produtos, cria novas colunas
                if (i + 1) % cards_por_linha == 0 and (i + 1) < len(products):
                    cols = st.columns(cards_por_linha)
        else:
            st.info("Nenhum produto encontrado.")


# Botão para cadastro do produto
if st.button("Cadastrar Produto"):
    if not product_name or not description or price is None:
        st.warning("Preencha todos os campos obrigatórios!")
    else:
        # Envia a imagem (se houver) para o Azure Storage
        image_url = ""
        if uploaded_file is not None:
            image_url = upload_image(uploaded_file)
        
        # Dados do produto
        product_data = {
            "nome": product_name,
            "descricao": description,
            "preco": price,
            "imagem_url": image_url
        }

        # Insere os dados no Azure SQL Server
        if insert_product_sql(product_data):
            st.success("Produto cadastrado com sucesso no Azure SQL!")
            list_produtos_screen()
        else:
            st.error("Houve um problema ao cadastrar o produto no Azure SQL.")

        # Opcional: Salva os dados localmente (exemplo usando arquivo JSON)
        file_path = "produtos.json"
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    produtos = json.load(f)
                except json.JSONDecodeError:
                    produtos = []
        else:
            produtos = []

        produtos.append(product_data)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(produtos, f, ensure_ascii=False, indent=4)
        
        st.json(product_data)

st.header("Listagem dos Produtos")


# Botão para carregar e exibir a lista de produtos
if st.button("Listar Produtos"):
    list_produtos_screen()
