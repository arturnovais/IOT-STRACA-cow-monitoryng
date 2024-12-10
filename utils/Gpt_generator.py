import os
import openai

class Gpt_generator():
    def __init__(self, api_key=None, model='gpt-4'):
        self.api_key = api_key
        
        if self.api_key is None:
            self.api_key = self.get_api_key()
        
        openai.api_key = self.api_key  # Configura a chave da API
        self.model = model

    def get_api_key(self, file_path='openai_key.txt'):
        with open(file_path, 'r') as file:
            api_key = file.read().strip()
            return api_key

    def invoke_stream(self, prompt):
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                stream=True  # Ativando o streaming
            )
            # Lendo os tokens em tempo real
            for chunk in response:
                if "choices" in chunk and len(chunk["choices"]) > 0:
                    choice = chunk["choices"][0]
                    if "delta" in choice and "content" in choice["delta"]:
                        yield choice["delta"]["content"]  # Retorna os tokens gerados em tempo real
        except Exception as e:
            print(f"Erro ao conectar com a API do OpenAI: {e}")
            raise e
