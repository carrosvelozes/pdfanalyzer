from transformers import pipeline

# Carregar o modelo Gemma 3 (substituir pelo correto quando disponível)
model_pipeline = pipeline("text-generation", model="google/gemma-3b")

def ask_llm(question, context):
    """Envia uma pergunta ao modelo com o contexto do PDF."""
    prompt = f"Baseando-se no seguinte conteúdo, responda:\n\n{context}\n\nPergunta: {question}"
    response = model_pipeline(prompt, max_length=200, truncation=True)
    return response[0]["generated_text"]

if __name__ == "__main__":
    sample_text = "O céu é azul devido à dispersão da luz."
    question = "Por que o céu é azul?"
    print(ask_llm(question, sample_text))
