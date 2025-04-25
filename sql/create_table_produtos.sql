CREATE TABLE Produtos (
    id          INT             IDENTITY(1,1)       PRIMARY KEY,
    nome        NVARCHAR(255),
    descricao   NVARCHAR(MAX),
    preco       DECIMAL(18,2),
    imagem_url  NVARCHAR(2083)
)
