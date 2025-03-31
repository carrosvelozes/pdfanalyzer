import gradio as gr
import os
from datetime import datetime
from model_manager import ModelManager
from pdf_processor import PDFProcessor

# Inicializa os gerenciadores e carrega o modelo imediatamente
model_manager = ModelManager()
pdf_processor = PDFProcessor()

# Carrega o modelo ao iniciar
try:
    model_manager.load_model()
except Exception as e:
    print(f"Erro ao carregar o modelo: {str(e)}")

def process_and_chat(message, history, pdf_file=None):
    try:
        # Processa novo PDF se fornecido
        if pdf_file:
            try:
                success, _, _ = pdf_processor.process_pdf(pdf_file.name)
                if not success:
                    return history + [[None, "Não foi possível processar o PDF. Verifique se o arquivo é válido."]]
                
                # Obtém estatísticas do PDF
                stats = pdf_processor.get_statistics()
                stats_message = f"""=== ESTATÍSTICAS DO PDF ===
Total de páginas: {stats['total_pages']}
Total de palavras: {stats['total_words']}
Média de palavras por página: {stats['average_words_per_page']:.1f}
===========================

Como posso ajudar?"""
                
                return history + [[None, stats_message]]
            except Exception as e:
                return history + [[None, f"Erro ao processar o PDF: {str(e)}"]]

        # Se não há mensagem, retorna o histórico atual
        if not message:
            return history

        # Verifica se há um PDF carregado
        if not pdf_processor.is_pdf_loaded():
            return history + [[message, "Por favor, carregue um PDF primeiro antes de fazer perguntas."]]

        try:
            # Obtém o contexto do PDF e gera a resposta
            pdf_context = pdf_processor.get_summary()
            prompt = model_manager.format_prompt(pdf_context, message)
            response = model_manager.generate_response(prompt)
            
            # Adiciona a interação ao histórico
            return history + [[message, response]]
        except Exception as e:
            return history + [[message, f"Erro ao processar sua pergunta: {str(e)}"]]

    except Exception as e:
        return history + [[message if message else None, f"Erro inesperado: {str(e)}"]]

def show_about():
    return gr.update(visible=True, value="Sobre o projeto...")

def show_credits():
    return gr.update(visible=True, value="Créditos do projeto...")

def process_message(message, history):
    return process_and_chat(message, history, None)

# CSS atualizado
CUSTOM_CSS = """
    /* Cores base */
    :root {
        --chat-bg: #0f0f0f;
        --message-bg: #1a1a1a;
        --user-message-bg: #2a2a2a;
        --border: #333333;
    }

    /* Container principal */
    .gradio-container {
        background-color: var(--chat-bg);
    }

    /* Header simples */
    .header {
        display: flex;
        justify-content: center;
        padding: 1rem;
        gap: 2rem;
        border-bottom: 1px solid var(--border);
    }

    .nav-button {
        background: transparent;
        border: none;
        color: white;
        padding: 8px 16px;
        cursor: pointer;
        opacity: 0.8;
    }

    .nav-button:hover {
        opacity: 1;
    }

    /* Chat container */
    .chat-container {
        max-width: 1000px;
        margin: 0 auto;
        height: calc(100vh - 200px);
        padding: 2rem;
        overflow-y: auto;
    }

    /* Mensagens */
    .message {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        max-width: 80%;
    }

    .bot-message {
        background: var(--message-bg);
        color: white;
        margin-right: auto;
    }

    .user-message {
        background: var(--user-message-bg);
        color: white;
        margin-left: auto;
    }

    /* Área de input */
    .input-area {
        max-width: 1000px;
        margin: 1rem auto;
        padding: 1rem;
        display: flex;
        gap: 1rem;
        align-items: center;
    }

    /* Campo de texto e botões */
    .gr-text-input {
        background: var(--message-bg);
        color: white;
        border: 1px solid var(--border);
        border-radius: 8px;
    }

    .file-upload, .gr-button {
        background: var(--message-bg);
        border: 1px solid var(--border);
        border-radius: 8px;
        color: white;
    }
"""

# Interface principal
with gr.Blocks(css=CUSTOM_CSS, theme=None, analytics_enabled=False) as demo:
    # Header
    with gr.Row(elem_classes="header"):
        with gr.Row(elem_classes="header-nav"):
            analyzer_btn = gr.Button("ANALYZER", elem_classes="nav-button")
            sobre_btn = gr.Button("SOBRE", elem_classes="nav-button")
            creditos_btn = gr.Button("CREDITOS", elem_classes="nav-button")

    # Componentes para Sobre e Créditos
    about_text = gr.Markdown(visible=False)
    credits_text = gr.Markdown(visible=False)

    # Chat principal
    chatbot = gr.Chatbot(
        [],
        elem_classes="chat-container",
        height=None,
        show_label=False
    )
    
    # Área de input
    with gr.Row(elem_classes="input-area"):
        with gr.Row(elem_classes="input-container"):
            pdf_input = gr.File(
                label="",
                type="filepath",
                elem_classes="file-upload",
                file_types=[".pdf"]
            )
            msg = gr.Textbox(
                show_label=False,
                placeholder="Digite sua pergunta sobre o PDF...",
                scale=20
            )
            send_button = gr.Button("→", elem_classes="gr-button")

    # Eventos do PDF
    pdf_input.change(
        fn=process_and_chat,
        inputs=[gr.State(None), chatbot, pdf_input],
        outputs=[chatbot],
        queue=False
    )

    # Eventos do chat
    msg.submit(
        fn=process_message,
        inputs=[msg, chatbot],
        outputs=[chatbot]
    ).then(lambda: "", None, msg)
    
    send_button.click(
        fn=process_message,
        inputs=[msg, chatbot],
        outputs=[chatbot]
    ).then(lambda: "", None, msg)

    # Eventos dos botões do header
    sobre_btn.click(fn=show_about, outputs=about_text)
    creditos_btn.click(fn=show_credits, outputs=credits_text)

# Inicia a interface
if __name__ == "__main__":
    demo.launch()
