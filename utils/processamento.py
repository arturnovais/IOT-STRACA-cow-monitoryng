from acelerometro import Acelerometro
from gps import GPS

import pandas as pd


acelerometro_raw_path = "data/raw/acelerometro_example.csv"
GPS_raw_path = "data/raw/gps_example.csv"


class Processamento():
    def __init__(self) -> None:
        data_acelerometro = pd.read_csv(acelerometro_raw_path)
        data_gps = pd.read_csv(GPS_raw_path)
        
        self.AC = Acelerometro(data=data_acelerometro)
        self.GPS = GPS(data=data_gps)

    
    def process(self):
        passos = self.AC.contar_passos()
        distancia_total = self.GPS.calcular_distancia_total()
        distancia_pot_tempo = self.GPS.calcular_distancia_acumulada()
        abaixou_cabeca_total = self.AC.detectar_movimentos_descendentes_y()
