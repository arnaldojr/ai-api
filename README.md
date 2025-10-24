# Chatbot com Gemini 2.5 Flash

Este projeto implementa um chatbot interativo utilizando o modelo Gemini 2.5 Flash, da Google.
O objetivo é demonstrar como integrar modelos generativos a uma aplicação Flask de forma simples, modular e escalável.

## estrutura do projeto

```bash
chatbot-gemini/
├── src/
│   ├── app.py              # API
├── .env                    # Chaves de API (não versionar!)
├── .gitignore
├── requirements.txt        
├── README.md
└── venv/                   # Ambiente virtual (não versionar)

```

## Passo 1: Configuração do Ambiente

1. **Crie um ambiente virtual**:

   ```bash
   python -m venv venv
   ```

2. **Ative o ambiente virtual**:

   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

3. **Instale as bibliotecas necessárias**:
   ```bash
   pip install -r requirements.txt
   ```

## Passo 2: Obtenção da Chave de API do Gemini

1. **Crie uma conta no Google AI Studio**:

   - Acesse o [Google AI Studio](https://ai.google.dev/).

2. **Obtenha a chave de API**:

   - Siga o guia detalhado disponível neste link: [Gemini API Quickstart](https://ai.google.dev/gemini-api/docs/quickstart?hl=pt-br&lang=python).

3. **Configure a chave de API**:

   - crie um arquivo `.env` na raiz do projeto e adicione sua chave

   ```bash
   GEMINI_API_KEY=sua_api_key
   OPENWEATHER_API_KEY=sua_api_key
   ```

## Passo 3: Execute o servidor Flask:

   - No terminal, execute o seguinte comando para iniciar o servidor:

     ```bash
     python src/app.py
     ```

## Passo 4: Interaja com o chatbot:
   Após iniciar o servidor Flask, você pode testar e interagir com a API do chatbot de diferentes maneiras:

   1. Usando ferramentas de requisição HTTP
      
      - Utilize o Postman, Insomnia ou qualquer outro cliente HTTP para envia requisições POST para o endpoint `/chat`.

      - Isso permite testar diferentes mensagens, visualizar o JSON retornado e simular cenários de integração.

   2. Usando o terminal com `curl`:

      - Execute o comando abaixo para enviar uma mensagem diretamente pelo terminal:

     ```bash
     curl -X POST http://127.0.0.1:5000/chat \
       -H "Content-Type: application/json" \
       -d '{
         "message":"E ai tiozão, como você está?"
         }'
     ```

   3. Integrando com um sistema backend (Java, .NET, Node.js, etc.)

      - Como o chatbot foi implementado como uma API REST, ele pode ser consumido facilmente por aplicações em outras linguagens.
      - Basta que o seu backend envie uma requisição HTTP POST para o endpoint `/chat`, enviando um JSON no formato:

      ```bash
      {
      "message": "Texto da mensagem que deseja enviar ao modelo"
      }
      ```

      - O chatbot retornará um JSON contendo a resposta gerada pelo modelo Gemini.

## Personalizando o chatbot para um Domínio (Assistente de investimentos)

- Use o endpoint `/financas`.

- Como testar: Envie uma requisição com o nome de uma cidade:

```bash
curl -X POST http://127.0.0.1:5000/financas \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Qual a diferença entre reserva de emergência e renda fixa?"
  }'
```

## Integração com API de Terceiros (Consulta de Clima)**

- Para integrar a API com com uma API pública, como a [OpenWeatherMap](https://openweathermap.org/) API.
- Acesse o site, crie uma conta e crie uma API_KEY.
- Como testar: Envie uma requisição com o nome de uma `cidade`:

```bash
curl -X POST http://127.0.0.1:5000/weather \
   -H "Content-Type: application/json" \
   -d '{
      "city": "Cotia"
      }'
```

