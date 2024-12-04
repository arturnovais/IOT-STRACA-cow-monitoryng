import subprocess

from utils.processamento import Processamento

def main():
    """
    Executa o processamento dos dados e inicia a interface do Streamlit.
    """
    print("Iniciando o processamento dos dados...")
    
    try:
        # Instancia e executa o processamento
        processador = Processamento()
        processador.process()
        print("Processamento concluído com sucesso!")

        # Iniciar a interface Streamlit
        print("Iniciando a interface...")
        subprocess.run(["streamlit", "run", "interface/app.py"])
    except Exception as e:
        print(f"Ocorreu um erro durante o processamento ou execução da interface: {e}")

if __name__ == "__main__":
    """_summary_
    """   
    main()
