from math import radians, cos, sin, sqrt, atan2
import pandas as pd
import numpy as np

class GPS:
    def __init__(self, data=None, data_path=None):
        self.data = None
        if data_path:
            self.load_data(data_path=data_path)
        elif data is not None:
            self.load_data(data=data)

    def load_data(self, data_path=None, data=None):
        if data_path:
            try:
                self.data = pd.read_csv(data_path)
            except Exception as e:
                raise ValueError(f"Erro ao carregar dados do caminho {data_path}: {e}")
        elif isinstance(data, pd.DataFrame):
            self.data = data
        elif isinstance(data, np.ndarray):
            self.data = pd.DataFrame(data, columns=[
                "Time(ms)", "Latitude", "Longitude", "Altitude", 
                "Speed", "UTC_Time", "Date", "Sats", "Direction"
            ])
        else:
            raise ValueError("Os dados devem ser um caminho válido, um DataFrame ou um array NumPy.")
        
        required_columns = {"Latitude", "Longitude", "Altitude", "Speed"}
        if not required_columns.issubset(self.data.columns):
            raise ValueError(f"O conjunto de dados deve conter as colunas {required_columns}.")
    
    
    def calcular_distancia_total(self):
        """
        Calcula a distância total percorrida com base nas coordenadas GPS.
        :return: Distância total percorrida em metros.
        """
        if self.data is None or "Latitude" not in self.data.columns or "Longitude" not in self.data.columns:
            raise ValueError("Os dados de GPS não estão carregados ou não possuem colunas de Latitude e Longitude.")

        # Converter latitude e longitude para radianos
        lat = self.data["Latitude"].apply(np.radians)
        lon = self.data["Longitude"].apply(np.radians)

        # Diferenças entre pontos consecutivos
        dlat = lat.diff().fillna(0)
        dlon = lon.diff().fillna(0)

        # Fórmula de Haversine
        a = (np.sin(dlat / 2)**2 +
            np.cos(lat.shift().fillna(lat)) * np.cos(lat) * np.sin(dlon / 2)**2)
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

        # Raio da Terra em metros
        R = 6371000
        distances = R * c

        # Distância total percorrida
        distancia_total = distances.sum()
        return distancia_total
    
    
    
    def calcular_distancia_acumulada(self):
        """
        Calcula a distância acumulada até cada timestep e retorna um DataFrame com 'Time(ms)' e 'Distancia Acumulada(m)'.
        :return: DataFrame com as colunas 'Time(ms)' e 'Distancia Acumulada(m)'.
        """
        if self.data is None or "Latitude" not in self.data.columns or "Longitude" not in self.data.columns:
            raise ValueError("Os dados de GPS não estão carregados ou não possuem colunas de Latitude e Longitude.")

        # Converter latitude e longitude para radianos
        lat = self.data["Latitude"].apply(np.radians)
        lon = self.data["Longitude"].apply(np.radians)

        # Diferenças entre pontos consecutivos
        dlat = lat.diff().fillna(0)
        dlon = lon.diff().fillna(0)

        # Fórmula de Haversine
        a = (np.sin(dlat / 2)**2 +
            np.cos(lat.shift().fillna(lat)) * np.cos(lat) * np.sin(dlon / 2)**2)
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

        # Raio da Terra em metros
        R = 6371000
        self.data["Distancia(m)"] = R * c

        # Calcular a distância acumulada
        self.data["Distancia Acumulada(m)"] = self.data["Distancia(m)"].cumsum()

        # Retornar apenas o DataFrame com timestep e distância acumulada
        return self.data[["UTC_Time", "Distancia Acumulada(m)"]]
    
    
    def calcular_tempo_movimento(self, velocidade_minima=0.5):
        """
        Calcula o tempo total em movimento e parado com base na velocidade.
        :param velocidade_minima: Velocidade mínima para considerar que está em movimento.
        :return: Tuple (tempo_em_movimento, tempo_parado) em segundos.
        """
        if self.data is None or "Speed" not in self.data.columns or "Time(ms)" not in self.data.columns:
            raise ValueError("Os dados de GPS devem conter as colunas 'Speed' e 'Time(ms)'.")

        # Adicionar uma coluna para identificar movimento
        self.data["Em Movimento"] = self.data["Speed"] > velocidade_minima

        # Calcular a diferença de tempo entre amostras
        self.data["Delta Tempo (s)"] = self.data["Time(ms)"].diff().fillna(0) / 1000.0

        # Separar o tempo total em movimento e parado
        tempo_em_movimento = self.data.loc[self.data["Em Movimento"], "Delta Tempo (s)"].sum()
        tempo_parado = self.data.loc[~self.data["Em Movimento"], "Delta Tempo (s)"].sum()

        return tempo_em_movimento, tempo_parado
