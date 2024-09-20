import sys
import os

# Adiciona o caminho da pasta RPA - AZURE ao sys.path
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, root)

from module import *

def manage_files():
  user = os.getlogin()
  download_folder_path = f'C:/Users/{user}/Downloads'
  download_folder = os.listdir(download_folder_path)

  os.makedirs('data/input', exist_ok=True)

  for file in download_folder:
    if '.csv' in file and 'SZ - Indicadores' in file:
      from_path = os.path.join(download_folder_path, file)
      to_path = os.path.join("data/input", file)
      try:
        os.rename(from_path, to_path)
      except FileExistsError:
        os.remove(f'data/input/{file}')
        os.rename(from_path, to_path)