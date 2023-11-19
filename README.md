![Coverage Testes](https://gitlab.com/lappis-unb/projects/mec-energia/mec-energia-api/badges/develop/coverage.svg)

# MEC-Energia API

Este repositório contém a implementação da API do sistema MEC-Energia.

O sistema MEC-Energia tem por objetivo auxiliar as instituições de ensino superior (IES) a gerenciar e avaliar a adequação de contratos de conta de energia elétrica a partir do registro das faturas mensais de energia, gerando relatórios de recomendações de ajustes nos contratos visando economia de recursos.

A documentação online do sistema está disponível em [Documentação](https://lappis-unb.gitlab.io/projects/mec-energia/documentacao)


## Como executar o serviço

Para acessar o banco, é recomendado que você tenha 
[Docker Compose](https://docs.docker.com/compose/install/) instalado em
sua máquina.

Copie o arquivo `.env.dev` para `.env`:

```
cp .env.dev .env 
```

Levante os containers da API e do banco de dados com:

```sh
docker-compose up -d
```

Se tudo deu certo, a API do Django REST deve estar acessível em 
http://localhost:8000.

Para ter acesso completo dos dados na API, você precisa criar um 
usuário. Leia como fazer isso em [seed](docs/seed.md#usuário).

Além disso, a API também tem seus endpoints documentados no Swagger em
http://localhost:8000/api/swagger/schema/. 
Que para acessar é preciso primeiro entrar com um dos usuários criados em http://localhost:8000/api-auth/login/.

Para derrubar os containers utilize:

```sh
docker-compose down
```


## Código de Conduta e Políticas

* Leia o [Código de Conduta](/CODE_OF_CONDUCT.md) do projeto;
* Veja as [Políticas](docs/politicas/branches-commits.md) do projeto.


## Documentação Extra de Configuração

Para saber mais sobre configuração de ambiente de desenvolvimento e 
outras coisas, acesse os seguintes links:

- **Comece aqui:** [ambiente de desenvolvimento](docs/ambiente-desenvolvimento.md)
- [Seed/popular](docs/seed.md)
- [Testes](docs/testes.md)
- [Depuração](docs/depuracao.md)
