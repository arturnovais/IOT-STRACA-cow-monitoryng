from acelerometro import Acelerometro
from gps import GPS

import pandas as pd
import os


acelerometro_raw_path = "data/raw/acelerometro_example.csv"
GPS_raw_path = "data/raw/gps_example.csv"

processed_path = "data/processed"


class Processamento():
    def __init__(self) -> None:
        data_acelerometro = pd.read_csv(acelerometro_raw_path)
        data_gps = pd.read_csv(GPS_raw_path)
        
        self.AC = Acelerometro(data=data_acelerometro)
        self.GPS = GPS(data=data_gps)

    
    def process(self):
        passos = self.AC.contar_passos()
        distancia_total = self.GPS.calcular_distancia_total()
        distancia_por_tempo = self.GPS.calcular_distancia_acumulada()
        abaixou_cabeca_total = self.AC.detectar_movimentos_descendentes_y()
        posicao_tempo = self.GPS.data[['Latitude', 'Longitude', 'UTC_Time']]
        tempo_em_movimento, tempo_parado = self.GPS.calcular_tempo_movimento()
        
        os.makedirs(processed_path, exist_ok=True)

        # Salvar os dados processados
        self.salvar_dados("passos.json", {"passos": passos})
        self.salvar_dados("distancia_total.json", {"distancia_total_m": distancia_total})
        self.salvar_dados("distancia_por_tempo.csv", distancia_por_tempo)
        self.salvar_dados("movimentos_descendentes.json", {"movimentos_descendentes": abaixou_cabeca_total})
        self.salvar_dados("posicao_tempo.csv", posicao_tempo)
        self.salvar_dados(
            "tempo_movimento.json",
            {"tempo_em_movimento_s": tempo_em_movimento, "tempo_parado_s": tempo_parado}
        )
        
        
    def salvar_dados(self, filename, data):
        """
        Salva os dados processados em arquivos.
        :param filename: Nome do arquivo a ser salvo (com extensão .csv ou .json).
        :param data: Dados a serem salvos. Pode ser um DataFrame, dicionário ou lista.
        """
        filepath = os.path.join(processed_path, filename)
        
        # Verificar extensão e salvar de acordo
        if filename.endswith(".csv") and isinstance(data, pd.DataFrame):
            data.to_csv(filepath, index=False)
        elif filename.endswith(".json") and isinstance(data, dict):
            with open(filepath, "w") as f:
                import json
                json.dump(data, f, indent=4)
        else:
            raise ValueError(f"Formato de arquivo ou tipo de dados não suportado para {filename}")
