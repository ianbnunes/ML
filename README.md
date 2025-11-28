# Projeto de Machine Learning: Predição de Diabetes (Pipeline End-to-End)

Este projeto implementa um pipeline completo de Engenharia de Dados e Machine Learning para a predição de diabetes, utilizando contêineres Docker para orquestrar ingestão, armazenamento, modelagem e visualização.

O trabalho baseia-se na reprodução e melhoria de métodos de classificação, integrando ferramentas modernas como MLFlow, MinIO, PostgreSQL e ThingsBoard.

---

## 👥 Equipe
* **Arthur Jatobá Lobo Suzuki** (@user_github)
* **Gabriel Lima Siqueira** (@GabrielLimaSC)
* **Gabriel Ferreira Ferraz** (@gabrielfferraz)
* **Ian de Barros Nunes** (@ianbnunes)
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
├── notebooks/               # Notebooks de análise e scripts
│   ├── analise_diabetes.ipynb   # Notebook principal (Reprodução e Melhorias)
│   ├── simulador_iot.py         # Script de simulação de sensores
│   └── outputs/                 # Gráficos e relatórios gerados
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

1.  Acesse o Console do MinIO: [http://localhost:9001](https://www.google.com/search?q=http://localhost:9001)
      * **Usuário:** `minioadmin`
      * **Senha:** `minioadmin`
2.  Navegue até o bucket **`raw-data`** (criado automaticamente).
3.  Clique em **Upload** e envie o arquivo: `Dataset of Diabetes .csv`.
      * *Nota: Certifique-se de que o nome do arquivo corresponde ao esperado pela API.*

-----

### Passo 3: Ingestão de Dados (FastAPI)

Agora vamos mover os dados do MinIO para o Banco de Dados PostgreSQL.

1.  Acesse a documentação da API: [http://localhost:8000/docs](https://www.google.com/search?q=http://localhost:8000/docs)
2.  Localize o endpoint verde **POST /ingest**.
3.  Clique em **Try it out** -\> **Execute**.
4.  Aguarde a resposta `200 OK` confirmando a quantidade de linhas inseridas no banco.

-----

### Passo 4: Ciência de Dados & Modelagem (Jupyter)

Nesta etapa, treinamos os modelos e geramos os relatórios de comparação.

1.  Acesse o JupyterLab: [http://localhost:8888](https://www.google.com/search?q=http://localhost:8888)
      * *Se pedir token: Verifique os logs do terminal com `docker logs jupyter_container`.*
2.  Abra a pasta `notebooks` e execute o arquivo principal (ex: `analise_diabetes.ipynb`).
3.  Execute todas as células sequencialmente.
4.  **Resultados:**
      * Os gráficos e resumos serão salvos na pasta `notebooks/outputs`.
      * O rastreamento dos experimentos (métricas e modelos) será enviado ao **MLFlow**.

-----

### Passo 5: Rastreamento de Modelos (MLFlow)

Para auditar a performance dos modelos treinados:

1.  Acesse: [http://localhost:5000](https://www.google.com/search?q=http://localhost:5000)
2.  Clique no experimento `Projeto_Diabetes_Clinico` na barra lateral.
3.  Compare as métricas (Acurácia, F1-Score) entre a **Decision Tree** e o **Random Forest**.

-----

### Parando o Projeto

Para encerrar a execução e liberar recursos da máquina:

```bash
docker-compose down
```

