import pandas as pd
import time
import json
import requests
import random
import os
from sqlalchemy import create_engine


ACCESS_TOKEN = "COLE_SEU_TOKEN_AQUI" 

THINGSBOARD_HOST = os.getenv('TB_HOST', 'localhost')
THINGSBOARD_PORT = os.getenv('TB_PORT', '8080')
THINGSBOARD_URL = f"http://{THINGSBOARD_HOST}:{THINGSBOARD_PORT}/api/v1"

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_URI = f"postgresql+psycopg2://user:password@{DB_HOST}:{DB_PORT}/diabetes_db"

print("🚑 Conectando ao Banco de Dados (Dataset Clínico)...")

try:
    engine = create_engine(DB_URI)

    df = pd.read_sql("SELECT * FROM diabetes_tb", engine)
    df.columns = [c.upper() for c in df.columns]

    print(f"Dados carregados! Total: {len(df)} pacientes históricos.")

    url = f"{THINGSBOARD_URL}/{ACCESS_TOKEN}/telemetry"

    while True:
        df_sample = df.sample(frac=1).reset_index(drop=True)

        for index, row in df_sample.iterrows():

            # Lógica de Negócio:
            # Y (Diabético) ou P (Pré) = 1 (Alerta Vermelho)
            # N (Normal) = 0 (Verde)
            classe_original = str(row.get('CLASS', 'N')).strip()
            risco = 1 if classe_original in ['Y', 'P'] else 0

            telemetria = {
                "id_paciente": int(row.get('ID', 999)),
                "hba1c": float(row.get('HBA1C', 0)),    # O principal marcador
                "ureia": float(row.get('UREA', 0)),     # Marcador secundário
                "creatinina": float(row.get('CR', 0)),  # Marcador renal
                "bmi": float(row.get('BMI', 0)),        # Peso
                "risco_diabetes": risco                 # O que o modelo previu
            }

            # Envia para o Dashboard
            try:
                response = requests.post(url, json=telemetria)

                if response.status_code == 200:
                    status_icon = "ALERTA DIABETES" if risco == 1 else "SAUDÁVEL"
                    print(f"Paciente {telemetria['id_paciente']} | HbA1c: {telemetria['hba1c']} | {status_icon}")
                else:
                    print(f"Erro Thingsboard: {response.status_code}")

            except Exception as e:
                print(f"Erro de conexão: {e}")

            time.sleep(1)

except Exception as e:
    print(f"Erro ao ler do banco: {e}")
    print("Verifique se o container 'db' está rodando na porta 5432.")
