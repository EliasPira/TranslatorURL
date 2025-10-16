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
