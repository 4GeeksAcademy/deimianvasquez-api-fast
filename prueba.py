import os 


path = "data/users.csv"

if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
        data = f.read()
else:
    print(f"Archivo no encontrado: {path}")


# ./data/users.csv
# ./app/models
# ../../data/users.csv


# home/data/users.csv
# home/app/