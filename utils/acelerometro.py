import numpy as np
import pandas as pd

class Acelerometro:
    def __init__(self, data=None):
        """
        Inicializa a classe Acelerometro.
        :param data: Um DataFrame ou array contendo os dados do acelerômetro (x, y, z).
        """
        self.data = None
        if data is not None:
            self.load_data(data)
    
    def load_data(self, data):
        """
        Carrega os dados do acelerômetro.
        :param data: Um DataFrame ou array contendo as colunas x, y, z.
        """
        if isinstance(data, pd.DataFrame):
            self.data = data
        elif isinstance(data, np.ndarray):
            self.data = pd.DataFrame(data, columns=["x", "y", "z"])
        else:
            raise ValueError("Os dados devem ser um DataFrame ou um array NumPy.")
    
    def calculate_magnitude(self):
        """
        Calcula a magnitude do vetor de aceleração para cada registro.
        :return: Um array com as magnitudes calculadas.
        """
        if self.data is None:
            raise ValueError("Nenhum dado carregado. Use 'load_data()' para carregar os dados.")
        
        self.data["magnitude"] = np.sqrt(
            self.data["x"]**2 + self.data["y"]**2 + self.data["z"]**2
        )
        return self.data["magnitude"]
    
    def detect_anomalies(self, threshold=2.0):
        """
        Detecta anomalias baseadas em um limite para a magnitude.
        :param threshold: Limite para considerar uma magnitude como anômala.
        :return: Um DataFrame com os registros anômalos.
        """
        if "magnitude" not in self.data.columns:
            self.calculate_magnitude()
        
        anomalies = self.data[self.data["magnitude"] > threshold]
        return anomalies
    
    def filter_by_time(self, timestamps):
        """
        Filtra os dados por uma lista de timestamps.
        :param timestamps: Lista de timestamps a serem incluídos.
        :return: Um DataFrame com os dados filtrados.
        """
        if "timestamp" not in self.data.columns:
            raise ValueError("Os dados não possuem uma coluna 'timestamp'.")
        
        return self.data[self.data["timestamp"].isin(timestamps)]
    
    def summarize(self):
        """
        Gera um resumo estatístico dos dados do acelerômetro.
        :return: Um DataFrame com estatísticas descritivas.
        """
        if self.data is None:
            raise ValueError("Nenhum dado carregado. Use 'load_data()' para carregar os dados.")
        
        return self.data.describe()
