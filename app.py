import streamlit as st
from bs4 import BeautifulSoup
import json
import os
import requests
# Load API secrets
from dotenv import load_dotenv
load_dotenv()
CLOUDFLARE_ACCOUNT_ID = os.environ.get("CF_ACCOUNT_ID")
CLOUDFLARE_API_TOKEN= os.environ.get("CF_API_TOKEN")
API_BASE_URL = "https://gateway.ai.cloudflare.com/v1/b70f22c8e75bf434686321ac6f4c7730/uahk/workers-ai/"
# url = f'https://gateway.ai.cloudflare.com/v1/b70f22c8e75bf434686321ac6f4c7730/uahk/workers-ai/@cf/mistral/mistral-7b-instruct-v0.2-lora'
url = f'https://api.cloudflare.com/client/v4/accounts/b70f22c8e75bf434686321ac6f4c7730/ai/run/@cf/facebook/bart-large-cnn'

# Define the headers
headers = {
    'Authorization': f'Bearer ym2fRJa3ZKVMswwA3fAkeQr10u87LJbTC8VG1_TZ',
    'Content-Type': 'application/json'
}

def run(model, input):
    response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=input)
    return response.json()

def main():
    st.markdown("""
        <style>
            .big-font {
                font-size:40px !important;
                color:green;
            }
        </style>
    """, unsafe_allow_html=True)
    st.markdown('<p class="big-font"<p>AI🤖 News🗞️ Summarizer</p>', unsafe_allow_html=True)
    st.write(":blue[This Python🐍 web🕸️ app is built👩🏻‍💻 w/ [Streamlit](https://streamlit.io/) && [Cloudflare Workers AI](https://ai.cloudflare.com/)]")

    news_link = st.text_input('Please enter a news link to summarize') # news_link = "https://www.npr.org/2024/07/08/g-s1-8731/emma-navarro-coco-gauff-wimbeldon"
    tone = st.selectbox(
        ':green[What tone do you want the news summary to take?]',
        ('humorístico', 'majestoso', 'acadêmico', 'inspiracional', 'dramatico', 'geracao Z', 'geracao Y', 'geracao X', 'geracao baby boomer', 'geracao silenciosa', 'geracao centenaria', 'geracao alfa', 'geracao beta', 'geracao gama', 'geracao delta', 'geracao epsilon', 'geracao zeta', 'geracao eta', 'geracao theta', 'geracao iota', 'geracao kappa', 'geracao lambda', 'geracao mu', 'geracao nu', 'geracao xi', 'geracao omicron', 'geracao pi', 'geracao rho', 'geracao sigma', 'geracao tau', 'geracao upsilon', 'geracao phi', 'geracao chi', 'geracao psi', 'geracao omega')
    )
    st.write("You selected: ", tone)
    if st.button('Enter') and tone is not None and news_link is not None:
        with st.spinner('Processing📈...'):
            resp1 = requests.get(news_link)
            soup = BeautifulSoup(resp1.text, 'html.parser')
            # get page title
            title = soup.title.string

            # Extract text data from website
            # get all p under single-content class
            content = soup.find_all('main')
            # Encontrar a div com a classe 'single-content'
            # single_content_div = soup.find('div', class_='single-content')
            single_content_div = soup.find('main')

            # Pegar todas as tags 'p' dentro dessa div
            paragraphs = single_content_div.find_all('p')

            # Extrair o texto de cada parágrafo
            finalText = ''
            for paragraph in paragraphs:
                finalText += paragraph.get_text()

            print('text_data' , finalText)
            print("\n")

            # Define the data
            data = {
                "messages": [
                    {
                        "role": "user",
                        "content": f"Summarize the following content from a news article in a {tone} tone: {finalText}"
                    }
                ]
            }

            dataT = {
                "input_text": finalText,
                "max_length": 2048,
            }

# Você é um assistente com muito conhecimento em literatura, redação e gramática. Você é capaz de resumir textos e fornecer informações sobre o conteúdo. Você também entende de Programação Neurolinguística (PNL), psicologia e inteligência emocional. Você é capaz de se comunicar de forma que capte a atencao do leitor para o conteúdo.
            dataLora = {
                "messages": [
                    {
                        "role": "system",
                        "content": f"Sumarize o conteúdo de um artigo de notícias, use um tom {tone}."
                    },
                    {
                        "role": "assistant",
                        "content": f"Sempre escreva no idioma Português Brasileiro. Seja claro e objetivo. Evite usar palavras muito difíceis. Sempre escreva em terceira pessoa."
                    },
                    {
                        "role": "user",
                        "content": f"{finalText}"
                    },
                ],
                "max_tokens": 1024,
                "repetition_penalty": 0.9,
                "temperature": 0.4,
            }
    

            # sumarization with facebook/bart-large-cnn
            response = run("@cf/facebook/bart-large-cnn", dataT)
            print('response', response)
            summary = response["result"]["summary"]

            # 2 text summarization request
            txtLoraMistral = run("@hf/thebloke/llamaguard-7b-awq", dataLora)
            txtLoraMistral_data = txtLoraMistral["result"]["response"]

            st.header(title)
            st.subheader("Summary 1 (facebook/bart-large-cnn): ", divider=True)
            st.write( summary)
            st.subheader("Summary 2: ", divider=True)
            st.write( txtLoraMistral_data)




if __name__ == "__main__":
    main()