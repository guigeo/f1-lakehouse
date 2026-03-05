import datetime
import os
import time

import dotenv

from src.collect import CollectResults
from src.sender import Sender

dotenv.load_dotenv()

BUCKET_NAME = os.getenv("BUCKET_NAME")
BUCKET_FOLDER = os.getenv("BUCKET_FOLDER")

#while True:

print("Iniciando processo...")

print("Coletando dados....")
#collect_data = CollectResults(years=[datetime.datetime.now().year])
collect_data = CollectResults(years=[2019])
collect_data.process_years()

print("Enviando dados...")
sender_data = Sender(bucket_name=BUCKET_NAME, bucket_folder=BUCKET_FOLDER)
sender_data.process_folder("data/")

print("Iteração finalizada.")
#time.sleep(60*60*6)
