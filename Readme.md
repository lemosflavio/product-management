# Gerencimanto de Produtos

Projeto destinado para auxiliar o gerenciamento de produtos.


## Como rodar

Abra o console e faça o download do projeto
```shell script
git clone git@github.com:lemosflavio/product-management.git
```

Rodando localmente
```shell script
pip install -r requirements.txt
python api/run.py
```

Rodando via docker
```
docker-compose up --build
```

## Rodando

O projeto possui uma collection do postman com alguns exemplos das possíveis requests na API

* `GET /health_check/` - Informa a saúde da aplicação, no caso se a conexão com o banco está ativa;
* `GET /products/` - Lista os produtos cadastrados, também é possível realizar filtrar pelo status e o ean do produto;
* `GET /products/{product_id}` - Retorna as informações do produto correspondente ao product_id passado;
* `POST /products/` - Cria um produto caso as informações sejam validas. Caso tente ser adicionado um produto que esteja "deletado" o produto será reativado;
* `PUT /products/{product_id}` - Atualiza as informações passadas no produto correspondente ao product_id passado;
* `DELETE /products/{product_id}` - Atualiza o status para deletado o produto com o product_id correspondente   

## Rodando os testes

Instalar as dependências de desenvolvimento e rodar a suíte de testes

```shell script
pip install -r rquirements-dev.txt
pytest
```

