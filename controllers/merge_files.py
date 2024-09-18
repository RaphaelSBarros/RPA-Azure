from module import *

folder_path= 'data/input'
folder = os.listdir(folder_path)
print(folder)

data = {}

for file in folder:
  name = file.replace('.', ' ').split(' ')
  name = f"{name[3]} {name[4] if name[4] != 'csv' else ''}"
  print(name)
  dataframe = pd.read_csv(f'{folder_path}/{file}', index_col='ID')
  data.update({name: dataframe})
  
merged_data = pd.concat([df for df in data.values()], axis=0)
merged_data = merged_data.rename(columns={'Area Level 2': 'Client', 'Area Level 1': 'Product'})
output_folder = 'data/output'
os.makedirs(output_folder, exist_ok=True)
merged_data.to_excel(f'{output_folder}/merged_files.xlsx')