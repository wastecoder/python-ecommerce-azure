# Armazenando dados de um E-Commerce na Cloud

Este repositório contém o código de um desafio de projeto do bootcamp **Microsoft Azure Cloud** Native da DIO.
O objetivo principal é criar uma aplicação web simples para cadastrar produtos de um e-commerce e armazenar seus dados _(nome, descrição, preço e URL da imagem)_ de forma persistente na nuvem, utilizando os serviços do Microsoft Azure.


## :file_folder: Estrutura do Projeto

```bash
ecommerce-azure-python/
├── .venv/
├── sql/
│   └── create_table_produtos.sql
├── src/
│   ├── main.py
│   ├── .env
│   └── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── produtos.json
```

* `sql/`: Contém scripts SQL para criação de tabelas.
* `src/`: Contém o código fonte principal da aplicação Streamlit (`main.py`).
* `requirements.txt`: Lista das dependências necessárias para executar o projeto.


## :cloud: Tecnologias e Serviços Azure Utilizados
Durante o desenvolvimento deste projeto, foram utilizados os seguintes serviços do Microsoft Azure:

* **Grupo de Recursos:** Organização lógica dos recursos do projeto.
* **Conta de Armazenamento (Azure Blob Storage):** Armazenamento escalável para imagens de produtos via URLs.
* **Banco de Dados SQL do Azure:** Banco de dados relacional para dados dos produtos.
* **Servidor SQL do Azure:** Hospedagem do Banco de Dados SQL.


## :snake: Tecnologias Python Utilizadas
A aplicação foi desenvolvida utilizando as seguintes bibliotecas Python:

* **Streamlit:** Criação rápida de interface web interativa.
* **Azure Storage Blob:** Interação com o Azure Blob Storage (upload de imagens).
* **pyodbc:** Conexão e operações no Azure SQL Database.
* **uuid:** Geração de nomes únicos para arquivos de imagem.
* **json:** Manipulação de dados JSON (salva localmente em produtos.json).
* **os:** Interação com o sistema operacional (verificação de arquivos).

## :gear: Processo de Cadastro e Armazenamento
1. **Interface com Streamlit:** Interface web para inserir os dados e a imagem do produto.
2. **Upload da Imagem para o Azure Blob Storage:**
   -  A imagem do produto cadastrado é enviada para um container específico (`fotos`) dentro da Conta de Armazenamento Azure Blob Storage.
   -  Um nome único é gerado para o arquivo utilizando `uuid` antes do upload.
3. **Obtenção da URL da Imagem:** Após o upload, gera a URL pública da imagem armazenada no Blob Storage.
4. **Armazenamento dos Dados no Azure SQL Server:** Os dados do produto (incluindo a URL da imagem) são salvos na tabela `dbo.Produtos` no Banco de Dados SQL do Azure utilizando a biblioteca `pyodbc`.

## :bulb: Insights e Possibilidades

* **Escalabilidade:** A nuvem permite armazenar grande quantidade de imagens e dados com alta disponibilidade, aliviando a carga da aplicação e do banco de dados.
* **Separação de Dados:** Separar o armazenamento de imagens dos dados dos produtos melhora o desempenho e facilita o gerenciamento de cada tipo de informação.
* **Integração Simples:** As ferramentas de desenvolvimento da nuvem para Python simplificam a conexão e o uso dos serviços na sua aplicação.
* **Flexibilidade para Crescer:** O projeto pode ser facilmente expandido com novas funcionalidades (listagem, edição, carrinho, etc.) e outros serviços de nuvem para otimizar a performance e adicionar recursos.
* **Gerenciamento da Infraestrutura:** A infraestrutura na nuvem pode ser automatizada, facilitando a criação, configuração e gerenciamento dos recursos do projeto.


## :computer: Instalação e Execução

Para executar esta aplicação localmente, siga os passos abaixo:

1.  **Clone o projeto na pasta desejada:**
    ```bash
    git clone https://github.com/wastecoder/python-ecommerce-azure.git
    ```
2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Crie um ambiente virtual (recomendado):**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # No Linux/macOS
    .venv\Scripts\activate  # No Windows
    ```
4.  **Configure as variáveis de ambiente:**
    * Crie o arquivo `.env` na pasta `src/` e defina as seguintes variáveis com as suas credenciais do Azure:
        ```
        AZURE_STORAGE_CONNECTION_STRING="SUA_CONNECTION_STRING"
        SQL_SERVER="SEU_SQL_SERVER.database.windows.net"
        SQL_DATABASE="SEU_SQL_DATABASE"
        SQL_USERNAME="SEU_SQL_USERNAME"
        SQL_PASSWORD="SUA_SQL_PASSWORD"
        ```
    * **Importante:** O arquivo `.env` está no `.gitignore` para evitar o commit de informações sensíveis.
5.  **Execute a aplicação Streamlit:**
    ```bash
    streamlit run src/main.py
    ```

    Isso abrirá a aplicação no seu navegador web.
