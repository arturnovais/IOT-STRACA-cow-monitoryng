import streamlit as st
import pandas as pd
import json
import os
import matplotlib.pyplot as plt

processed_path = "data/processed"

def load_data():
    """
    Carrega os dados processados salvos na pasta 'data/processed'.
    :return: Um dicionário com os dados carregados.
    """
    data = {}

    # Ler arquivos JSON
    for json_file in ["passos.json", "distancia_total.json", "movimentos_descendentes.json", "tempo_movimento.json"]:
        path = os.path.join(processed_path, json_file)
        if os.path.exists(path):
            with open(path, "r") as f:
                data[json_file] = json.load(f)
    
    # Ler arquivos CSV
    for csv_file in ["distancia_por_tempo.csv", "posicao_tempo.csv"]:
        path = os.path.join(processed_path, csv_file)
        if os.path.exists(path):
            data[csv_file] = pd.read_csv(path)
    
    return data

def main():
    # Configuração do título
    st.set_page_config(page_title="Monitoramento de Bovinos", layout="wide")
    st.title("🐄 Monitoramento de Bovinos")

    # Menu lateral
    st.sidebar.header("Menu")
    st.sidebar.write("Escolha o que deseja visualizar:")

    # Carregar dados
    st.write("Carregando dados processados...")
    data = load_data()

    # Layout das métricas principais
    col1, col2, col3 = st.columns(3)

    # Exibir número de passos
    with col1:
        if "passos.json" in data:
            passos = data["passos.json"]["passos"]
            st.metric(label="🐾 Passos Detectados", value=passos)

    # Exibir distância total
    with col2:
        if "distancia_total.json" in data:
            distancia_total = data["distancia_total.json"]["distancia_total_m"]
            st.metric(label="📏 Distância Total (m)", value=f"{distancia_total:.2f}")

    # Exibir movimentos descendentes
    with col3:
        if "movimentos_descendentes.json" in data:
            movimentos_descendentes = data["movimentos_descendentes.json"]["movimentos_descendentes"]
            st.metric(label="📉 Movimentos Descendentes", value=movimentos_descendentes)

    # Exibir tempo em movimento e parado com gráfico
    st.markdown("### ⏳ Tempo em Movimento e Parado")
    col4, col5 = st.columns([2, 1])  # Gráfico maior que os textos

    if "tempo_movimento.json" in data:
        tempo_em_movimento = data["tempo_movimento.json"]["tempo_em_movimento_s"]
        tempo_parado = data["tempo_movimento.json"]["tempo_parado_s"]

        # Criar gráfico de pizza
        labels = ['Tempo em Movimento', 'Tempo Parado']
        valores = [tempo_em_movimento, tempo_parado]
        cores = ['#FFA500', '#FFD580']  # Cores laranja e variação

        fig, ax = plt.subplots()
        ax.pie(valores, labels=labels, autopct='%1.1f%%', colors=cores, startangle=90)
        ax.axis('equal')  # Garantir que o gráfico de pizza seja um círculo

        # Exibir gráfico no Streamlit
        with col4:
            st.pyplot(fig)

        # Exibir métricas na coluna ao lado
        with col5:
            st.metric(label="Tempo em Movimento (s)", value=f"{tempo_em_movimento}")
            st.metric(label="Tempo Parado (s)", value=f"{tempo_parado}")

    # Exibir gráficos adicionais
    st.markdown("### 📊 Análises Adicionais")

    # Gráfico de distância por tempo
    if "distancia_por_tempo.csv" in data:
        with st.expander("📈 Distância Acumulada ao Longo do Tempo"):
            df_distancia = data["distancia_por_tempo.csv"]
            st.line_chart(df_distancia.set_index("UTC_Time")["Distancia Acumulada(m)"])

    # Mapa de posições
    if "posicao_tempo.csv" in data:
        with st.expander("🗺️ Posição Geográfica ao Longo do Tempo"):
            df_posicao = data["posicao_tempo.csv"]

            # Renomear colunas para o formato esperado pelo st.map
            df_posicao = df_posicao.rename(columns={"Latitude": "latitude", "Longitude": "longitude"})
            
            st.map(df_posicao)

if __name__ == "__main__":
    main()
