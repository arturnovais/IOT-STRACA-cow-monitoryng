import pandas as pd
import numpy as np
from scipy.signal import find_peaks


class Acelerometro:
    def __init__(self, data=None, data_path=None):
        """
        Inicializa a classe Acelerometro e carrega os dados, se fornecidos.
        :param data: Um DataFrame ou array contendo os dados do acelerômetro.
        :param data_path: Caminho para o arquivo de dados (CSV ou similar).
        """
        self.data = None
        if data_path:
            self.load_data(data_path=data_path)
        elif data is not None:
            self.load_data(data=data)

    def load_data(self, data_path=None, data=None):
        """
        Carrega os dados do acelerômetro.
        :param data_path: Caminho para o arquivo CSV contendo os dados.
        :param data: Um DataFrame ou array contendo os dados do acelerômetro.
        """
        if data_path:
            # Tentar carregar o arquivo como CSV
            try:
                self.data = pd.read_csv(data_path)
            except Exception as e:
                raise ValueError(f"Erro ao carregar dados do caminho {data_path}: {e}")
        elif isinstance(data, pd.DataFrame):
            self.data = data
        elif isinstance(data, np.ndarray):
            self.data = pd.DataFrame(data, columns=["Time(ms)", "Accel_X", "Accel_Y", "Accel_Z", 
                                                    "Gyro_X", "Gyro_Y", "Gyro_Z", "Temp_C"])
        else:
            raise ValueError("Os dados devem ser um caminho válido, um DataFrame ou um array NumPy.")
        
        # Verificar se as colunas necessárias estão presentes
        required_columns = {"Accel_X", "Accel_Y", "Accel_Z"}
        if not required_columns.issubset(self.data.columns):
            raise ValueError(f"O conjunto de dados deve conter as colunas {required_columns}.")


    def calculate_magnitude(self):
        if self.data is None:
            raise ValueError("Nenhum dado carregado. Use 'load_data()' para carregar os dados.")
        
        self.data["magnitude"] = np.sqrt(
            self.data["Accel_X"]**2 + self.data["Accel_Y"]**2 + self.data["Accel_Z"]**2
        )
        return self.data["magnitude"]
    
    
    def contar_passos(self, height_threshold=1.0, distance_threshold=20):
        """
        Conta o número de passos baseado em picos na magnitude da aceleração.
        :param height_threshold: Magnitude mínima para considerar um pico (ajustável).
        :param distance_threshold: Distância mínima entre picos consecutivos (em amostras).
        :return: Número estimado de passos.
        """
        if "magnitude" not in self.data.columns:
            self.calculate_magnitude()

        # Detectar picos na magnitude
        peaks, _ = find_peaks(self.data["magnitude"], height=height_threshold, distance=distance_threshold)

        return len(peaks)
    