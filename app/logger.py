import csv
import os
from datetime import datetime

LOG_FILE = "logs.csv"

def write_log(evento, detalhe="", usuario=None, rota=None):
    """
    Grava um log em formato CSV.
    :param evento: tipo de evento (ex: ERRO, LOGIN, ACESSO, LOGOUT)
    :param detalhe: descrição do que aconteceu
    :param usuario: nome do usuário (se houver login)
    :param rota: rota acessada
    """
    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # se for a primeira vez, escreve o cabeçalho
        if not file_exists:
            writer.writerow(["data_hora", "evento", "detalhe", "usuario", "rota"])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            evento,
            detalhe,
            usuario if usuario else "-",
            rota if rota else "-"
        ])

def read_logs():
    logs = []
    try:
        with open(LOG_FILE, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                logs.append(row)
    except FileNotFoundError:
        pass
    return logs