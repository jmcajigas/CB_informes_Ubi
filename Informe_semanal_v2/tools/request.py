# %%
# this cell enables relative path imports
import os
from dotenv import load_dotenv
import pickle
load_dotenv()
_PROJECT_PATH: str = os.environ["_project_path"]
_PICKLED_DATA_FILENAME: str = os.environ["_pickled_data_filename"]
_CSV_DATA_FILENAME: str = os.environ["_csv_data_filename"]
sas_url : str = os.environ["sas_url"]


import sys
from pathlib import Path
project_path = Path(_PROJECT_PATH)
sys.path.append(str(project_path))

import urllib3

urllib3.disable_warnings()

# %%
# import all your modules here
import time
import json
import pandas as pd

import config_v2 as cfg
from library_ubidots_v2 import Ubidots as ubi

# %%
from azure.storage.blob import BlobServiceClient, BlobClient, ContentSettings

class AzureBlobFileDownloader:
    def __init__(self, sas_url):
        self.blob_service_client = BlobServiceClient(account_url=sas_url)

    def upload_pkl_file(self, bancolombia_pkl, blob_name, blob_container):
        try:
            blob_client = self.blob_service_client.get_blob_client(container=blob_container, blob=blob_name)
            blob_content = pickle.dumps(bancolombia_pkl)
            blob_client.upload_blob(data=blob_content, overwrite=True)

        except Exception as e:
            print(f"Fallo la subida perrito '{blob_name}': {str(e)}")
            
    def read_file_content_as_pickle(self, blob_name, blob_container):
        try:
            blob_client = self.blob_service_client.get_blob_client(container=blob_container, blob=blob_name)
            blob_content = blob_client.download_blob().readall()
            print(f"Content of file '{blob_name}':")
            file_content = pickle.loads(blob_content)
            return file_content
        except Exception as e:
            print(f"Failed to read content of '{blob_name}': {str(e)}")
            return None

# %%
downloader = AzureBlobFileDownloader(sas_url)
blob_container = "Bancolombia"
downloader.blob_container = blob_container

# %%
'''
import ssl
import urllib3

# Disable SSL certificate verification
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

'''

# %%
#blob_container = "Bancolombia"
blob_name = r"data/data_weekly_report.pkl"
downloader.blob_container = blob_container
df1 = downloader.read_file_content_as_pickle(blob_name, blob_container)
#bancolombia_pkl

# %%
#blob_name = r"data/data_weekly_report.pkl"
#downloader.upload_pkl_file(bancolombia_pkl,blob_name, blob_container)

# %%
# set your constants here
baseline=cfg.BASELINE
study=cfg.STUDY

# %%
print(study)
print(baseline)

# %%
df_devices = ubi.get_available_devices_v2(label='bancolombia', level='group', page_size=1000)
#df_vars = ubi.get_available_variables(list(df_devices['device_id']))
df_vars = ubi.get_available_variables2(list(df_devices['device_id']), verify_ssl=False)

# %%
df_vars = df_vars[df_vars['variable_label'].isin(cfg.WHITELISTED_VAR_LABELS)]
VAR_IDS_TO_REQUEST = list(df_vars['variable_id'])
VAR_ID_TO_LABEL = dict(zip(df_vars['variable_id'], df_vars['variable_label']))

# %%
#leer el archivo data_weekly_report.pkl y guardarlo en un dataframe llamado df1
# df1 = pd.read_pickle(r'C:\Users\jpocampo\OneDrive - CELSIA S.A E.S.P\Escritorio\Informe_Bancolombia\CB_informes_Ubi\Informe_semanal_v2\data\data_weekly_report.pkl')


# %%
fecha_minima = df1.index.min()

print("Fecha mínima:", fecha_minima)


# %%
CHUNK_SIZE = 10
DATE_INTERVAL_REQUEST = {'start': study[0], 'end': study[1]}
df = None
lst_responses = []
n_vars = len(VAR_IDS_TO_REQUEST)
print(f"Making request for the following interval: Study:{study[0]}, Study:{study[1]}")
for idx in range(0, ubi.ceildiv(len(VAR_IDS_TO_REQUEST), CHUNK_SIZE)):
    idx_start = idx * CHUNK_SIZE
    idx_end = (idx + 1) * CHUNK_SIZE
    chunk = VAR_IDS_TO_REQUEST[idx_start:idx_end]
    response = ubi.make_request(
        chunk, 
        DATE_INTERVAL_REQUEST, 
    )
    if response.status_code == 204 or response.status_code >= 500:
        print(f"Empty response for chunk {idx}")
        time.sleep(10)
        response = ubi.make_request(
        chunk, 
        DATE_INTERVAL_REQUEST,)
    current_idx = idx_end+1
    if (current_idx > n_vars):
        current_idx = n_vars
    print(f"Progress: {100*(current_idx)/n_vars:0.1f}%")
    print(f"Response status code: {response.status_code}")
    if (response.status_code != 204) and  (len(response.json()['results']) >0 ):
        lst_responses.append(response)
    else: 
        print(f"Empty response for chunk {idx}")
df = ubi.parse_response(lst_responses, VAR_ID_TO_LABEL)

# %%
#Unir el dataframe df y df1 en uno que se llame df_full
df = pd.concat([df1, df], axis=0, ignore_index=False)

# %%
# para quitar el indixe de "datatime" y volverlo columna 
df.reset_index(inplace=True)

# Quitar duplicados 
df = df.drop_duplicates()

# Establecer la columna "datetime" como el índice
df.set_index('datetime', inplace=True)


# %%
# df1 = pd.read_pickle(r'C:\Users\jpocampo\OneDrive - CELSIA S.A E.S.P\Escritorio\Informe_Bancolombia\CB_informes_Ubi\Informe_semanal_v2\data\data_weekly_report.pkl')

# %%
downloader.upload_pkl_file(df_devices, blob_name, blob_container)

# %%
#blob_name = r"data/data_weekly_report.pkl"
downloader.upload_pkl_file(df,blob_name, blob_container)

# %%
pd.to_pickle(df, project_path / 'data'/ _PICKLED_DATA_FILENAME)



