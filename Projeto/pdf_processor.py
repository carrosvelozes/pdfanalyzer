import pdfplumber
import logging

class PDFProcessor:
    def __init__(self):
        self.pages = []
        self.pdf_loaded = False  # Flag para indicar se o PDF foi carregado

    def process_pdf(self, file_path: str):
        """Lê e extrai texto de um PDF usando pdfplumber"""
        self.pages = []
        try:
            # Suprime avisos específicos do pdfplumber
            logging.getLogger('pdfminer').setLevel(logging.ERROR)
            
            with pdfplumber.open(file_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    # Garante que está usando a MediaBox
                    page.bbox = page.mediabox
                    text = page.extract_text()
                    if text:
                        self.pages.append({
                            "number": i + 1,
                            "content": text,
                            "word_count": len(text.split())
                        })
            self.pdf_loaded = True  # Marca o PDF como carregado com sucesso
            return True, "PDF processado com sucesso!", self.pages
        except Exception as e:
            self.pdf_loaded = False  # Marca como não carregado se ocorrer erro
            return False, f"Erro ao processar PDF: {str(e)}", []

    def is_pdf_loaded(self):
        """Retorna True se o PDF foi carregado corretamente."""
        return self.pdf_loaded

    def get_summary(self):
        """Retorna um resumo simples do conteúdo do PDF"""
        if not self.pages:
            return "Nenhum conteúdo extraído."
        return " ".join([page["content"][:500] for page in self.pages[:3]])  # Exemplo de resumo

    def get_statistics(self):
        """Retorna estatísticas do PDF processado"""
        if not self.pages:
            return {
                "total_pages": 0,
                "total_words": 0,
                "average_words_per_page": 0
            }
        
        total_pages = len(self.pages)
        total_words = sum(page["word_count"] for page in self.pages)
        average_words = total_words / total_pages if total_pages > 0 else 0
        
        return {
            "total_pages": total_pages,
            "total_words": total_words,
            "average_words_per_page": average_words
        }
