from fastapi import FastAPI, HTTPException
import boto3
import pandas as pd
from sqlalchemy import create_engine
import os

app = FastAPI()

# Configurações (Vindas do Docker Compose)
DB_URI = os.getenv("DB_URI", "postgresql://user:password@db:5432/diabetes_db")
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://minio:9000")
AWS_ACCESS_KEY = "minioadmin"
AWS_SECRET_KEY = "minioadmin"
BUCKET_NAME = "raw-diabetes-data"
FILE_KEY = "Dataset_of_Diabetes.csv"

@app.get("/")
def home():
    return {"status": "API de Ingestão Online"}

@app.post("/ingest")
def run_ingestion():
    try:
        # 1. Conectar no MinIO (S3)
        print("Conectando ao MinIO...")
        s3 = boto3.client(
            's3',
            endpoint_url=MINIO_ENDPOINT,
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY
        )

        # 2. Baixar o arquivo CSV para a memória
        print(f"Baixando {FILE_KEY}...")
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=FILE_KEY)
        df = pd.read_csv(obj['Body'])
        
        # 3. Conectar no Postgres e Salvar
        print("Salvando no Postgres...")
        engine = create_engine(DB_URI)
        
        # 'replace' recria a tabela se já existir. 'chunksize' evita travar a memória.
        df.to_sql('diabetes_tb', engine, if_exists='replace', index=False, chunksize=10000)
        
        return {
            "message": "Sucesso! Dados ingeridos.",
            "total_linhas": len(df),
            "colunas": list(df.columns)
        }

    except Exception as e:
        print(f"Erro: {e}")
        raise HTTPException(status_code=500, detail=str(e))