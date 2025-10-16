import requests
from bs4 import BeautifulSoup
from langchain_openai.chat_models.azure import AzureChatOpenAI

def extract_text_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()
        texto = soup.get_text(separator=' ')
        linhas = (line.strip() for line in texto.splitlines())
        parts = (phrase.strip() for line in linhas for phrase in line.split("  "))
        texto_limpo = '\n'.join(part for part in parts if part)
        return texto_limpo
    else:
        raise Exception(f"Erro ao acessar URL. Código: {response.status_code}")

def translate_article(text, lang):
    client = AzureChatOpenAI(
        azure_endpoint="https://azureopenai-dio-translator.openai.azure.com/",
        api_key="SUA_CHAVE_AQUI",
        api_version="2024-02-15-preview",
        deployment_name="gpt-4o-mini",
        max_retries=0
    )

    messages = [
        ("system", "Você atua como tradutor de textos"),
        ("user", f"Traduza o seguinte conteúdo para o idioma {lang} e responda em markdown:\n\n{text}")
    ]

    response = client.invoke(messages)
    return response.content

!pip install requests beautifulsoup4 openai langchain-openai

from src.translator import extract_text_from_url, translate_article

# URL do artigo técnico
url = 'https://dev.to/johnnyreilly/azure-open-ai-handling-capacity-and-quota-limits-with-bicep-4n3k'

# Extração do texto
text = extract_text_from_url(url)

# Tradução
article = translate_article(text, "pt-br")

# Salvar em arquivo markdown
with open("translated_articles/artigo_traduzido.md", "w", encoding="utf-8") as f:
    f.write(article)

print("✅ Tradução concluída e salva em translated_articles/artigo_traduzido.md")
