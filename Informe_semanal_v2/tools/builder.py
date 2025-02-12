# %%
# this cell enables relative path imports
# this cell enables relative path imports
import os
from dotenv import load_dotenv
load_dotenv()
_PROJECT_PATH: str = os.environ["_project_path"]
_PICKLED_DATA_FILENAME: str = os.environ["_pickled_data_filename"]

import sys
from pathlib import Path
project_path = Path(_PROJECT_PATH)
sys.path.append(str(project_path))

# %%
# import all your modules here
import pandas as pd
import nbformat as nbf

import config_v2 as cfg
from library_report_v2 import Processing as pro

# %%
df = pd.read_pickle(project_path / 'data' / _PICKLED_DATA_FILENAME)
df_bl, df_st = pro.split_into_baseline_and_study(df, baseline=cfg.BASELINE, study=cfg.STUDY, inclusive='both')

# %%
#datos_csv = pd.DataFrame(df)
#datos_csv.to_csv(r'C:\Users\jpocampo\Desktop\Infome_Semanal_bc\CB_informes_Ubi\Informe_semanal_v2\data\datos_informe_3_semana_julio.csv', index=True)

# %%
set_devices_bl = set(df_bl['device_name'])
set_devices_st = set(df_st['device_name'])

set_devices = set_devices_bl.intersection(set_devices_st)

df_bl = None
df_st = None
df = None

blueprint_filepath = project_path / 'tools' / 'modelo.ipynb'
nb_blueprint = nbf.read(blueprint_filepath, as_version=4)

# %%
df_notebooks = pd.DataFrame(set_devices, columns=['device'])

# %%
df_notebooks['code'] = df_notebooks['device'].str.split('-',expand=True)[0]

df_notebooks['number'] = df_notebooks['code'].str.strip('BC ')
df_notebooks['number'] = pd.to_numeric(df_notebooks['number'], errors='coerce')

df_notebooks = df_notebooks.sort_values(by='number')
sorted_devices = list(df_notebooks['device'])

# %%
for device_name in sorted_devices:
    nb = nb_blueprint.copy()
    nb_cells = nb['cells']
    cell_0 = nb_cells[0]
    cell_1 = nb_cells[1]
    cell_rest = nb_cells[2:]

    cell_0['source'] = f'# {device_name}'
    cell_1['source'] = f'DEVICE_NAME = \'{device_name}\'\nimport warnings\nwarnings.filterwarnings("ignore")'
    new_cells = [cell_0] + [cell_1] + cell_rest
    nb['cells'] = new_cells

    filename = f"Notebook {device_name}"
    write_path = project_path/'main'/'notebooks'/'individual'/f"{filename}.ipynb"
    nbf.write(nb, write_path)

    print(f"  - file: notebooks/individual/{filename}")



