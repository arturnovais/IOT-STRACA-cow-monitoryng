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
    
    
    def detectar_movimentos_descendentes_y(self, threshold=-0.1, duracao_minima=6):
        """
        Detecta movimentos descendentes únicos com base no eixo Y e diferencia movimentos rápidos de movimentos prolongados.
        :param threshold: Valor de aceleração abaixo do qual consideramos um movimento descendente.
        :param duracao_minima: Tempo mínimo (em segundos) para considerar que a cabeça permaneceu abaixada.
        :return: 
            - movimentos_unicos: Número total de movimentos descendentes detectados.
            - movimentos_prolongados: Número de movimentos prolongados (possivelmente comer ou beber).
        """
        # Verificar se a coluna de tempo existe como 'Time(ms)'
        if "Time(ms)" in self.data.columns:
            # Renomear para 'timestamp' para consistência
            self.data.rename(columns={"Time(ms)": "timestamp"}, inplace=True)

        # Validar presença das colunas necessárias
        if "Accel_Y" not in self.data.columns or "timestamp" not in self.data.columns:
            # Exibir as colunas disponíveis para diagnóstico
            print(f"Colunas disponíveis: {self.data.columns}")
            raise ValueError("Os dados precisam conter as colunas 'Accel_Y' e 'timestamp'.")

        # Ordenar os dados pelo timestamp para garantir sequência correta
        self.data = self.data.sort_values("timestamp").reset_index(drop=True)

        # Detectar onde Accel_Y está abaixo do limiar
        movimentos_descendentes = self.data["Accel_Y"] < threshold

        # Inicializar variáveis para análise
        movimentos_unicos = 0
        movimentos_prolongados = 0
        inicio_movimento = None

        # Iterar pelos dados para identificar movimentos
        for i, is_descendente in enumerate(movimentos_descendentes):
            timestamp_atual = self.data["timestamp"].iloc[i]

            if is_descendente:
                if inicio_movimento is None:
                    inicio_movimento = timestamp_atual  # Marcar o início do movimento
            else:
                if inicio_movimento is not None:
                    # Calcular duração do movimento
                    duracao = (timestamp_atual - inicio_movimento) / 1000.0  # Converter ms para segundos
                    movimentos_unicos += 1

                    # Verificar se o movimento é prolongado
                    if duracao >= duracao_minima:
                        movimentos_prolongados += 1

                    # Resetar início do movimento
                    inicio_movimento = None

        # Caso o movimento esteja em andamento no final da série
        if inicio_movimento is not None:
            duracao = (self.data["timestamp"].iloc[-1] - inicio_movimento) / 1000.0
            movimentos_unicos += 1
            if duracao >= duracao_minima:
                movimentos_prolongados += 1

        return movimentos_prolongados


    def calcular_tempo_comendo(self, threshold=-0.1, duracao_minima=6):
        """
        Calcula o tempo total que a vaca passa comendo, baseado em movimentos descendentes prolongados.
        :param threshold: Valor de aceleração abaixo do qual consideramos a cabeça abaixada.
        :param duracao_minima: Tempo mínimo (em segundos) para considerar que a vaca está comendo.
        :return: Tempo total comendo (em segundos).
        """
        # Verificar se a coluna de tempo existe como 'Time(ms)'
        if "Time(ms)" in self.data.columns:
            # Renomear para 'timestamp' para consistência
            self.data.rename(columns={"Time(ms)": "timestamp"}, inplace=True)

        # Validar presença das colunas necessárias
        if "Accel_Y" not in self.data.columns or "timestamp" not in self.data.columns:
            print(f"Colunas disponíveis: {self.data.columns}")
            raise ValueError("Os dados precisam conter as colunas 'Accel_Y' e 'timestamp'.")

        # Ordenar os dados pelo timestamp para garantir sequência correta
        self.data = self.data.sort_values("timestamp").reset_index(drop=True)

        # Detectar onde Accel_Y está abaixo do limiar
        movimentos_descendentes = self.data["Accel_Y"] < threshold

        # Inicializar variáveis para cálculo do tempo total
        tempo_comendo = 0.0
        inicio_movimento = None

        # Iterar pelos dados para calcular períodos prolongados
        for i, is_descendente in enumerate(movimentos_descendentes):
            timestamp_atual = self.data["timestamp"].iloc[i]

            if is_descendente:
                if inicio_movimento is None:
                    inicio_movimento = timestamp_atual  # Marcar o início do movimento
            else:
                if inicio_movimento is not None:
                    # Calcular duração do movimento
                    duracao = (timestamp_atual - inicio_movimento) / 1000.0  # Converter ms para segundos

                    # Acumular tempo se for um movimento prolongado
                    if duracao >= duracao_minima:
                        tempo_comendo += duracao

                    # Resetar início do movimento
                    inicio_movimento = None

        # Caso o movimento esteja em andamento no final da série
        if inicio_movimento is not None:
            duracao = (self.data["timestamp"].iloc[-1] - inicio_movimento) / 1000.0
            if duracao >= duracao_minima:
                tempo_comendo += duracao

        return int(tempo_comendo / 600)


