# Considerações finais

Primeiramente obrigado pela oportunidade de estar fazendo esta etapa do teste.
Tentei ser dinâmico e mostrar meu conhecimento em Elasticsearch utilizando as libs de consulta por API do próprio Elasticsearch.
Portanto ficaram as transações armazenadas no Elasticsearch, e as informações do Customer (nome, idade, agencia e conta) armazenadas no Postgres e acessado via SQLAlchemy.
Cada item do projeto está operando em um container específico, como solicitado.

Para iniciar o projeto, basta:

```cmd
$ docker-compose up -d
```

A aplicação subirá e as rotas podem ser acessadas por clients de APIs como Insomnia, Thunderclient e Postman. Uma documentação do tipo Swagger está disponível em http://localhost:5000/apidocs .


Os testes encontram-se em um diretório chamado `/test/` na raiz do projeto. Para acessá-los, entre no container:

```cmd
$ docker exec -it topaz-teste bash
```

E para executá-los, basta executar:

```cmd
$ python3 -m unittest test/*.py
```
