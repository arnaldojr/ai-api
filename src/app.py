from flask import Flask, request, jsonify
from google import genai
from pydantic import BaseModel
from typing import List
import os
import requests
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()


app = Flask(__name__)


# Configuração da chave de API
client = genai.Client(api_key=os.getenv("GENAI_API_KEY")) # não é uma boa prática deixar a chave de API hardcoded no código, usar variáveis de ambiente ou serviços de gerenciamento de chave é mais seguro.


#----------------### EXEMPLO SIMPLES ###----------------#
# básico para teste do servidor Flask rodando o gemini 2.5
 
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'error': 'Mensagem não fornecida'}), 400

    # Envio da mensagem ao modelo
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_input,
    )
    return jsonify({'response': response.text})

# ----------------### EXEMPLO COM RESPOSTA JSON ###----------------#
# Exemplo mais elaborado com prompt personalizado e resposta estruturada em JSON
# a documentaçao https://googleapis.github.io/python-genai/#

# Estrutura JSON válida com Pydantic
class ResponseModel(BaseModel):
    answer: str
    next_steps: list[str]
    disclaimer: str


SYSTEM_INSTRUCTION = """
Você é um ASSISTENTE DE INVESTIMENTOS para iniciantes.
Explique conceitos com precisão e equilíbrio, cite riscos e trade-offs.
Não faça recomendações personalizadas ou ordens de compra/venda.
Evite mencionar rentabilidade garantida. Se faltar contexto, peça informações mínimas.
Responda em pt-BR.
"""

@app.route('/financas', methods=['POST'])
def financas():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'error': 'Mensagem não fornecida'}), 400

   # Prompt personalizado para o domínio de finanças
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_input,
        # Todos os parâmetros de configuração devem ser passados juntos
        # dentro de um único dicionário para o argumento 'config'.
        config={
            "system_instruction": SYSTEM_INSTRUCTION,
            "temperature": 0.2,
            "response_mime_type": "application/json",
            "response_schema": ResponseModel,
        }
    )

    # Converta o objeto Pydantic (response.parsed) para um dicionário
    # usando .model_dump() antes de passar para jsonify.
    parsed_data = response.parsed.model_dump()

    return jsonify(parsed_data)




#----------------### EXEMPLO DE INTEGRAÇÃO COM API EXTERNA ###----------------#
# usando o OpenWeatherMap para obter informações do clima


@app.route('/weather', methods=['POST'])
def get_weather():
    city = request.json.get('city')
    if not city:
        return jsonify({'error': 'Cidade não fornecida'}), 400

    # Substitua 'sua_chave_api' pela sua chave da OpenWeatherMap
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=pt_br"

    # Realizar a requisição para a API
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description']
        temp = data['main']['temp']
        return jsonify({
            'city': city,
            'weather': weather,
            'temperature': f"{temp} °C"
        })
    else:
        return jsonify({'error': 'Não foi possível obter o clima'}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

