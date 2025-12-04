# Projeto de Machine Learning: Predição de Diabetes (Pipeline End-to-End)

Este projeto implementa um pipeline completo de Engenharia de Dados e Machine Learning para a predição de diabetes, utilizando contêineres Docker para orquestrar ingestão, armazenamento, modelagem e visualização.

O trabalho baseia-se na reprodução e melhoria de métodos de classificação do Paper escolhido: 
* Comparative Effectiveness of Classification Algorithms in Predicting Diabetes (https://doi.org/10.1109/CICN63059.2024.10847398)
  
Integrando ferramentas modernas como MLFlow, MinIO, PostgreSQL e ThingsBoard.

---

## 👥 Equipe
* **Arthur Jatobá Lobo Suzuki** (@ajls@cesar.school)
* **Gabriel Lima Siqueira** (@gabrielLimaSC)
* **Gabriel Ferreira Ferraz** (@gabrielfferraz)
* **Ian de Barros Nunes** (@ianbnunes)
* **João Antonio Sampaio Ferreira** (@jasf@cesar.school)
* **Maria Augusta Barreto de Gois** (@maria-bg)

**Instituição:** CESAR School  
**Disciplina:** Aprendizado de Máquina - 2025.2  

---

## Arquitetura do Projeto

O projeto roda inteiramente sobre **Docker Compose**, integrando os seguintes serviços:

1.  **MinIO (S3):** Armazenamento de objetos (Data Lake) para os dados brutos (CSV).
2.  **PostgreSQL:** Banco de dados relacional para estruturar os dados processados e armazenar metadados do MLFlow e ThingsBoard.
3.  **FastAPI:** API de ingestão responsável por ler do MinIO e popular o PostgreSQL.
4.  **JupyterLab:** Ambiente de desenvolvimento para análise exploratória e treinamento dos modelos.
5.  **MLFlow:** Rastreamento de experimentos, métricas e versionamento de modelos.
6.  **ThingsBoard:** Dashboard IoT para visualização de dados simulados em tempo real.

---

## Estrutura de Pastas

```text
/
├── docker-compose.yml       # Orquestração dos serviços
├── fastapi/                 # Código da API de Ingestão
├── jupyterlab/              # Configuração do ambiente Jupyter
├── mlflow/                  # Configuração do servidor MLFlow
├── mlruns/                  # Logs do MLFlow
├── notebooks/               # Notebooks de análise e scripts
│   ├── analise_diabetes.ipynb   # Notebook principal baseado no Paper     
│   ├── analise_diabetes_completa_tradicional_mlp.ipynb   # Notebook comparativo com MLP
└── reports/                 # Gráficos e relatórios gerados
├── alerta_pacientes.json    # JSON do dashboard a ser criado no ThingsBoard
└── README.md                # Documentação do projeto
---
````

## Como Executar o Projeto

Siga este guia passo a passo para levantar a infraestrutura, processar os dados e visualizar os resultados.

### Pré-requisitos
* **Docker Desktop** instalado e rodando.
* **Git** (opcional, para clonar o repositório).
* **Python 3.9+** (apenas se for rodar os scripts de simulação fora do Docker).

---

### Passo 1: Infraestrutura (Docker)
Na raiz do projeto (onde está o `docker-compose.yml`), abra o terminal e execute:

```bash
docker-compose up -d --build
````

**Verificação:**
Aguarde alguns minutos. Certifique-se de que todos os contêineres estão com status `Up` ou `Healthy` executando:

```bash
docker ps
```
-----

### Passo 2: Configuração do Data Lake (MinIO)

Antes de ingerir os dados, precisamos colocar o arquivo CSV no nosso armazenamento de objetos.

1.  Acesse o Console do MinIO: [http://localhost:9001](http://localhost:9001)
      * **Usuário:** `minioadmin`
      * **Senha:** `minioadmin`
2.  Navegue até o bucket **`raw-diabetes-data`** (criado automaticamente).
3.  Clique em **Upload** e envie o arquivo: `Dataset_of_Diabetes.csv` disponibilizado.
      * *Nota: Certifique-se de que o nome do arquivo corresponde ao esperado pela API.*

-----

### Passo 3: Ingestão de Dados (FastAPI)

Agora vamos mover os dados do MinIO para o Banco de Dados PostgreSQL.

1.  Acesse a documentação da API: [http://localhost:8000/docs](http://localhost:8000/docs)
2.  Localize o endpoint verde **POST /ingest**.
3.  Clique em **Try it out** -\> **Execute**.
4.  Aguarde a resposta `200 OK` confirmando a quantidade de linhas inseridas no banco.

-----

### Passo 4: Ciência de Dados & Modelagem (Jupyter)

Nesta etapa, treinamos os modelos e geramos os relatórios de comparação.

1.  Acesse o JupyterLab: [http://localhost:8888](http://localhost:8888)
      * Se pedir por uma senha/token, escreva: **`diabetes-jupyter`**
2.  Abra a pasta `notebooks` e execute o arquivo principal (`analise_diabetes.ipynb`).
3.  Execute todas as células sequencialmente.
4.  **Resultados:**
      * Os gráficos e resumos serão salvos na pasta `notebooks/outputs`.
      * O rastreamento dos experimentos (métricas e modelos) será enviado ao **MLFlow**.
5. Repita essas duas últimas etapas no arquivo  `analise_diabetes_completa_tradicional_mlp.ipynb` para obter os resultados incrementados.

-----

### Passo 5: Rastreamento de Modelos (MLFlow)

Para auditar a performance dos modelos treinados:

1.  Acesse: [http://localhost:5000](http://localhost:5000)
2.  Clique no experimento `Projeto_ML_Diabetes` na barra lateral.
3.  Compare as métrica de Acurácia entre os modelos avaliados.
4.  Faça o mesmo ára 

-----

### Passo 6: Visualização de Dados no ThingsBoard

O **ThingsBoard** é a interface de visualização em tempo real dos dados de diabetes simulados.
Após levantar os contêineres, siga as etapas abaixo para fazer login e acessar o painel.



1.  Acesse: [http://localhost:8080](http://localhost:8080)
2.  Realize o login padrão com as credenciais padrão do ThingsBoard:
     * **Usuário:** `tenant@thingsboard.org`
     * **Senha:** `tenant`
3.  No menu lateral, clique em **Dashboards**. Em seguida clique em Importar.
4.  Selecione o arquivo .json no diretório (**`alerta_pacientes.json`**).
    O dashboard completo será restaurado automaticamente em poucos segundos.
5. Por fim, acesse-o para visualizar:
   * Métricas simuladas em tempo real (por exemplo, glicemia, ureia, creatinina).
   * Histórico de valores enviados pela API de simulação.
   * Gráficos e widgets configurados no ThingsBoard.
  
6. (Opcional) Se desejar testar o envio de dados simulados:
* Vá em **Devices → diabetes-simulator**. Se ele não estiver disponível, crie um com o mesmo nome.
* Copie o **Access Token** do dispositivo.
* Use-o com o script **simulador_iot.py**:

```python
ACCESS_TOKEN = "seu_token_de_acesso"
```
* Em seguida, no dashboard importado, procure pelo lápis de Edição do dashboard.
* Clique nos lápis de edição de cada widget e na seção de **Dados** faça o seginte:
  * Selecione o tipo: **`Dispositivo`** e em seguida selecione na categoria Dipositivo*: **`diabetes-simulator`** (o device que você criou)
---

### Parando o Projeto

Para encerrar a execução e liberar recursos da máquina:

```bash
docker-compose down

```

