# PDF ANALYZER 📄

Um analisador de PDF inteligente que utiliza o modelo Gemma 2B para responder perguntas sobre documentos PDF através de uma interface web interativa.

## 🚀 Funcionalidades

- 📎 Upload de arquivos PDF
- 📊 Análise automática de documentos
- 💬 Chat interativo com IA
- 📈 Estatísticas detalhadas do documento
- 🌙 Interface moderna com tema escuro

## 🛠️ Tecnologias

- Python 3.x
- Gemma 2B
- Gradio
- pdfplumber
- PyTorch
- Transformers

## 📋 Pré-requisitos

- Python 3.x
- GPU recomendada
- Mínimo 8GB RAM
- Conexão com internet (primeiro uso)

## ⚙️ Instalação

1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/pdf-analyzer.git
cd pdf-analyzer
```

2. Instale as dependências
```bash
pip install -r requirements.txt
```

3. Execute a aplicação
```bash
python interface.py
```

## 📦 Dependências

```
gradio
pdfplumber
transformers
torch
sentencepiece
```

## 🎯 Como Usar

1. Inicie a aplicação
2. Faça upload do seu PDF
3. Aguarde o processamento inicial
4. Visualize as estatísticas do documento
5. Faça perguntas sobre o conteúdo
6. Receba respostas contextualizadas

## 🏗️ Estrutura do Projeto

```
pdf-analyzer/
├── interface.py        # Interface web com Gradio
├── model_manager.py    # Gerenciamento do modelo Gemma 2B
├── pdf_processor.py    # Processamento de PDFs
├── requirements.txt    # Dependências do projeto
└── README.md          # Documentação
```

## ✨ Recursos

### Processamento de PDF
- Extração de texto
- Análise estatística
- Contagem de páginas e palavras

### Chat Interativo
- Interface de um ChatBot
- Respostas contextualizadas

### Interface
- Design responsivo
- Elementos interativos

## 📈 Status do Desenvolvimento

### Implementado ✅
- Interface básica com Gradio
- Processamento de PDF
- Integração com Gemma 2B
- Design responsivo
- Estatísticas do documento

### Em Desenvolvimento 🔄
- Melhorias na precisão das respostas
- Otimização para PDFs grandes

### Planejado ⏳
- Suporte multilíngue
- Exportação de conversas
- Análise avançada
- Customização de interface
- RAG
- Historico de chat

## ⚠️ Limitações Atuais

- Processamento limitado a texto
- Sem suporte a imagens/gráficos
- Tamanho máximo de documento não definido

## 🤝 Contribuição

Contribuições são bem-vindas! Áreas principais:
- Otimização de performance
- Melhorias na interface
- Documentação
- Testes automatizados


## 👥 Autores

* **Leonardo Moraes** - *Desenvolvimento Inicial* - [carrosvelozes](https://github.com/carrosvelozes)
  
---

