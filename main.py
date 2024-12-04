from utils.processamento import Processamento

def main():
    """
    Executa o processamento dos dados do acelerômetro e GPS.
    Salva os resultados em arquivos na pasta 'data/processed'.
    """
    print("Iniciando o processamento dos dados...")
    
    try:
        processador = Processamento()
        processador.process()
        
        print("Processamento concluído com sucesso!")
        print("Os arquivos processados foram salvos.")
    except Exception as e:
        print(f"Ocorreu um erro durante o processamento: {e}")

if __name__ == "__main__":
    main()
