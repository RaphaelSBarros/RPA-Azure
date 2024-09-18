from module import *

user = os.getlogin()
download_folder_path = f'C:/Users/{user}/Downloads'
download_folder = os.listdir(download_folder_path)
count=0

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