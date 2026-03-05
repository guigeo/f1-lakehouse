import datetime
import os
import time

import dotenv

from src.collect import CollectResults
from src.sender import Sender

dotenv.load_dotenv()

BUCKET_NAME = os.getenv("BUCKET_NAME")
BUCKET_FOLDER = os.getenv("BUCKET_FOLDER")

print("Iniciando processo...")

print("Coletando dados....")
collect_data = CollectResults(years=[datetime.datetime.now().year])
#collect_data = CollectResults(years=[2025])
collect_data.process_years()

files = [f for f in os.listdir("data") if f.endswith(".parquet")]

if not files:
    print("⚠️ Nenhum dado encontrado. Nada será enviado para o S3.")
    exit()

print(f"✅ {len(files)} arquivo(s) encontrado(s). Iniciando envio para o S3...")

sender_data = Sender(bucket_name=BUCKET_NAME, bucket_folder=BUCKET_FOLDER)
sender_data.process_folder("data/")

print("Coleta e envio finalizados.")