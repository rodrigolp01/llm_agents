<h1 align="center"> Criação e Integração de um Novo Agente na Plataforma de Advisors </h1>

* Foi criado um agente capaz de receber um trecho de código python e retornar sugestões de melhoria. São 2 arquivos, sendo que o primeiro implementar a classe CodeOptimizerLLM e o segundo para testar o modelo.

    - [code_analyzer.py](code_analyzer.py)
    - [code_analyzer_test.py](code_analyzer_test.py)

    Foram testados varios modelos de LLM open-source: [EleutherAI/gpt-neo-125M](https://huggingface.co/EleutherAI/gpt-neo-125m), [EleutherAI/gpt-neo-2.7B](https://huggingface.co/EleutherAI/gpt-neo-2.7B), [Salesforce/codegen-2B-multi](https://huggingface.co/Salesforce/codegen-2B-multi), entre outros. O melhor resultado foi obtido pelo gpt-neo-2.7B, gerando esse uma saida mais próxima da que se obtem de um GPT-3.5-turbo ou GPT-4. Modelos maiores não foram testados, devido a prazo, custo computacional/tempo para resposta da API e limite de GPU. Algumas variações de prompt foram testadas, mas sem melhora significativa.

    Foi usada a biblioteca [transformers](https://huggingface.co/docs/transformers/index) para carregar o modelo, geração de tokens e geração da saída. Foi fixado o tamanho de 512 tokens para exemplificar. Os demais parametros foram calibrados considerando os resultados obtidos entre os modelos testados.

* Também foi criada uma API ([app.py](app.py)) com 4 Endpoints:

    - POST /analyze-code: Recebe um trecho de código Python e retorna sugestões de melhoria.
    - GET /health: Retorna o status do agente (ex.: { "status": "ok" }).
    - GET /analyzes: Retorna as analises salvas no banco Postgres
    - POST /crewai/event: Recebe um trecho de código Python e retorna sugestões de melhoria.

    Esse ultimo endpoint serve para simular com seria uma integração com a plataforma CREWAI. O CREWAI chama a custom_tool(analise de código) que valida o evento, e chama o agente de analise.

    O comando abaixo levanta a API.

    ```sh
    uvicorn app:app --reload
    ```

    Abaixo exemplos de comandos para testar o funcionamento da API com agente de sugestão de melhoria de código python:

    ```sh
    curl -X GET http://localhost:8000/health
    ```

    ```sh
    curl -X POST http://localhost:8000/analyze-code -H "Content-Type: application/json" -d "{\"code\": \"def example_function(n):\n    result = []\n    for i in range(n):\n        result.append(i * i)\n    return result\"}"
    ```
    
    ```sh
    curl -X POST http://localhost:8000/crewai/event -H "Content-Type: application/json" -d "{\"event_type\": \"analyze-code\", \"payload\": {\"code\": \"def example_function(n):\\n    result = []\\n    for i in range(n):\\n        result.append(i * i)\\n    return result\"}}"
    ```

    ```sh
    curl -X GET http://localhost:8000/analyzes/
    ```

* O arquivo [database.py](database.py) contém as funções para inicialização do banco na API.

<h2 align="center"> Instalação </h2>

* A API foi testada em um sistema Windows 11 com suporte a GPU.

    - Instalação das dependencia do python

    ```sh
    pip install requirements.txt
    ```

    - Instalação do banco Postgres: baixar pelo site [PostgreSQL Downloads](https://www.postgresql.org/download/windows/), instalar e configurar usuário e senha. Também é possivel já criar a tabela que será usada no projeto "code_analyzer_db".

    ```sh
    psql -U postgres
    CREATE DATABASE code_analyzer_db;
    ```
    ou usar o script [create_table.py](create_table.py) após configuração do banco.


<h2 align="center"> Integração com CREWAI </h2>
Foi sugerida uma integração do agente com a plataforma CREWAI usando um novo endpoint, considerando que agora o trecho de código deve vir da CREWAI. Isso parece estar de acordo com o encontrado em (https://docs.crewai.com/how-to/create-custom-tools). O contrato sugerido também considera que o retorno inclui o status de sucesso ou falha do endpoint, nesse caso.

<h2 align="center"> Sugestões de Melhorias para a API </h2>

* Como melhorias, pensando em escalabilidade e crescimento futuro podemos ter:

    - Utilização de Filas de Mensagens (ex: Apache Kafka) para desacoplar a entrada e o processamento. Assim o agente vai trabalhar em segundo plano.

    - Cache (ex: Redis e Celery): Usa um cache com o Redis para armazenar os códigos e sugestões geradas anteriormente para evitar reanálise do mesmo pedido. O Celery seria usado para processar as tarefas da fila.

    - Alterar arquitetura para microserviços: Ter multiplas APIs para cada fucnionalidade, como analise de código e gerenciamento de filas.

    - Monitoramento: Para logs e analise de desempenho, poderiamos usar ferramentas com Grafana e Prometheus.

    - Utilizar métricas especificas de geração de código [Benchmarks and Metrics for Evaluations of Code Generation: A Critical Review](https://arxiv.org/html/2406.12655v1). Nesse paper, o modelo utilizado foi citado!!

    - Criar arquivo .env com todas aconfigurações sensíveis, como feito para a senha do postgres: database_user, password, host, database_name, model_name etc.
