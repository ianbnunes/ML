import json
import os
import random
import time

import pandas as pd
import requests
from sklearn.model_selection import train_test_split
from sqlalchemy import create_engine

# --- CONFIGURAÇÕES ---
ACCESS_TOKEN = "WeZ7nvnp9CbBoukoNEVV"
QTD_REGISTROS = 50
SIMULAR_LOOP = False

# Configuração de Redes
THINGSBOARD_HOST = os.getenv('TB_HOST', 'localhost')
THINGSBOARD_PORT = os.getenv('TB_PORT', '8080')
THINGSBOARD_URL = f"http://{THINGSBOARD_HOST}:{THINGSBOARD_PORT}/api/v1"

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_URI = f"postgresql+psycopg2://user:password@{DB_HOST}:{DB_PORT}/diabetes_db"

print("Conectando ao Banco de Dados...")

try:
    engine = create_engine(DB_URI)

    df_full = pd.read_sql("SELECT * FROM diabetes_tb", engine)
    df_full.columns = [c.upper() for c in df_full.columns]

    train, test = train_test_split(df_full, test_size=0.2, random_state=42)

    df_validacao = test.reset_index(drop=True)

    print(f"Dataset Total: {len(df_full)}")
    print(f"Dataset Treino (Ignorado): {len(train)}")
    print(f"Dataset Validação (Usado no IoT): {len(df_validacao)}")
    print(f"--> Iniciando envio de {QTD_REGISTROS} pacientes de validação...")

    url = f"{THINGSBOARD_URL}/{ACCESS_TOKEN}/telemetry"

    while True:
        if QTD_REGISTROS > len(df_validacao):
            amostra = df_validacao
        else:
            amostra = df_validacao.sample(n=QTD_REGISTROS)

        for index, row in amostra.iterrows():

            classe_original = str(row.get('CLASS', 'N')).strip()
            risco = 1 if classe_original in ['Y', 'P'] else 0

            telemetria = {
                "id_paciente": int(row.get('ID', 999)),
                "hba1c": float(row.get('HBA1C', 0)),
                "ureia": float(row.get('UREA', 0)),
                "creatinina": float(row.get('CR', 0)),
                "bmi": float(row.get('BMI', 0)),
                "risco_diabetes": risco
            }

            try:
                response = requests.post(url, json=telemetria)
                if response.status_code == 200:
                    status_icon = "🔴 ALERTA" if risco == 1 else "🟢 SAUDÁVEL"
                    print(
                        f"Enviado! Paciente {telemetria['id_paciente']} (Validação) | HbA1c: {telemetria['hba1c']} | {status_icon}")
                else:
                    print(f"Erro TB: {response.status_code}")
            except Exception as e:
                print(f"Erro de conexão: {e}")

            time.sleep(5)

        if not SIMULAR_LOOP:
            print(f"Envio concluído.")
            break

except Exception as e:
    print(f"Erro: {e}")