from transformers import AutoModelForCausalLM, AutoTokenizer, PreTrainedTokenizer
import torch
from typing import List, Dict, Tuple
import json
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class ModelManager:
    def __init__(self):
        self.model_name = "google/gemma-2b-it"
        self.tokenizer = None
        self.conversation_history = []
        self.max_length = 2048
        self.temperature = 0.7
        self.top_p = 0.95
        self.top_k = 50
        self.repetition_penalty = 1.1
        self.hf_token = "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"
        os.environ["HUGGING_FACE_HUB_TOKEN"] = self.hf_token
        os.environ["TOKENIZERS_PARALLELISM"] = "false"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.max_history_length = 5
        self.max_context_length = 2000

        # FAISS Index
        self.text_chunks = []
        self.index = None
        self.embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    def load_model(self):
        """Carrega o modelo e o tokenizer"""
        try:
            print("Iniciando carregamento do modelo...")
            print(f"Usando dispositivo: {self.device}")
            
            print("Tentando carregar o tokenizer...")
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                token=self.hf_token,
                trust_remote_code=True
            )
            
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                
            print("Tokenizer carregado com sucesso")
            
            print("Carregando o modelo...")
            # Ajuste o tipo de dados baseado no dispositivo
            dtype = torch.float16 if self.device == "cuda" else torch.float32
            
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                token=self.hf_token,
                torch_dtype=dtype,  # Usa float32 para CPU
                device_map="auto",
                trust_remote_code=True,
                low_cpu_mem_usage=True
            )
            
            print(f"Modelo {self.model_name} carregado com sucesso!")
            return True
            
        except Exception as e:
            print(f"Erro detalhado ao carregar o modelo: {str(e)}")
            import traceback
            print(traceback.format_exc())
            self.model = None
            self.tokenizer = None
            return False
    
    def index_pdf(self, pages):
        """Cria um índice vetorial do PDF"""
        self.text_chunks = [page["content"] for page in pages]
        embeddings = np.array([self.embedding_model.encode(text) for text in self.text_chunks])
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)

    def search_pdf(self, query, top_k=3):
        """Busca os trechos mais relevantes para a pergunta"""
        query_emb = self.embedding_model.encode(query).reshape(1, -1)
        distances, indices = self.index.search(query_emb, top_k)
        results = [self.text_chunks[idx] for idx in indices[0]]
        return " ".join(results)
    
    def format_prompt(self, pdf_content: str, user_question: str) -> str:
        """Formata o prompt para o modelo com contexto do PDF e histórico"""
        pdf_content = self.truncate_context(pdf_content)
        history = self.format_history()
        prompt = f"""Você é um assistente especializado em analisar documentos PDF.\n\n"""
        prompt += f"Contexto do PDF:\n{pdf_content}\n\n{history}\n\n"
        prompt += f"Pergunta atual: {user_question}\n\nResposta:"
        return prompt
    
    def generate_response(self, prompt: str) -> str:
        """Gera uma resposta usando o modelo"""
        try:
            if self.model is None or self.tokenizer is None:
                print("Modelo não inicializado. Tentando carregar novamente...")
                if not self.load_model():
                    return "Erro: Não foi possível carregar o modelo."

            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                truncation=True,
                max_length=self.max_length,
                padding=True
            ).to(self.device)

            generation_config = {
                "max_length": self.max_length,
                "temperature": self.temperature,
                "top_p": self.top_p,
                "top_k": self.top_k,
                "repetition_penalty": self.repetition_penalty,
                "do_sample": True,
                "pad_token_id": self.tokenizer.pad_token_id,
                "eos_token_id": self.tokenizer.eos_token_id,
            }

            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    **generation_config
                )

            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            response = response[len(prompt):].strip()
            self.add_to_history(prompt.split("Pergunta atual: ")[-1].strip(), response)
            return response

        except Exception as e:
            print(f"Erro detalhado na geração de resposta: {str(e)}")
            return f"Erro ao gerar resposta: {str(e)}"

    def truncate_context(self, text: str) -> str:
        """Trunca o contexto para o tamanho máximo permitido"""
        if len(text) > self.max_context_length:
            return text[:self.max_context_length]
        return text

    def add_to_history(self, question: str, answer: str):
        """Adiciona uma interação ao histórico"""
        self.conversation_history.append({"question": question, "answer": answer})
        if len(self.conversation_history) > self.max_history_length:
            self.conversation_history.pop(0)

    def format_history(self) -> str:
        """Formata o histórico de conversas"""
        if not self.conversation_history:
            return ""
        
        history = "Histórico de conversas:\n"
        for interaction in self.conversation_history:
            history += f"Pergunta: {interaction['question']}\n"
            history += f"Resposta: {interaction['answer']}\n\n"
        return history