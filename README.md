# 🤖 Legal Assistant RAG

> An intelligent legal assistant using RAG (Retrieval-Augmented Generation) to answer questions about French legal documents.

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green.svg)](https://fastapi.tiangolo.com/)
[![Gradio](https://img.shields.io/badge/Gradio-UI-orange.svg)](https://gradio.app/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ Features

- ✅ **RAG Implementation** with OpenAI GPT-4o-mini
- ✅ **Ultra-fast Vector Search** with FAISS
- ✅ **Modern REST API** with FastAPI
- ✅ **Intuitive UI** with Gradio
- ✅ **Source Citations** for every answer
- ✅ **Minimal Cost** (~$0.0006 per question)
- ✅ **100% Local** (except OpenAI API calls)

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- OpenAI API key ([get one here](https://platform.openai.com/api-keys))
- ~$5 OpenAI credit (lasts a long time!)

### Installation

```bash
# Clone the repository
git clone https://github.com/Bellilty/rag-juridique.git
cd rag-juridique

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

```bash
# Create .env file with your OpenAI API key
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

### Add Legal Documents

Place your legal PDF documents in `data/pdfs/`:

- French Constitution
- Civil Code
- GDPR
- Labor Law
- etc.

You can find download links in `data/pdfs/LIENS_TELECHARGEMENT.md`

### Build FAISS Index

```bash
python -m src.embeddings
```

This will:

1. Extract text from PDFs
2. Split into chunks
3. Create embeddings via OpenAI
4. Build FAISS index
5. Save to `index/`

### Launch the Application

**Option A - Gradio UI (Recommended):**

```bash
python ui.py
```

Then open http://localhost:7860

**Option B - FastAPI:**

```bash
uvicorn src.api:app --reload
```

Then open http://localhost:8000/docs

## 🎯 Usage Examples

### Via Gradio UI

Open http://localhost:7860 and ask questions like:

- "What is the French Constitution?"
- "What are the powers of the President?"
- "What is labor law?"

### Via API

```bash
curl "http://localhost:8000/ask?query=What+is+the+Constitution&k=3"
```

### Via Python

```python
import requests

response = requests.get(
    "http://localhost:8000/ask",
    params={
        "query": "What are personal data?",
        "k": 3,
        "model": "gpt-4o-mini"
    }
)

print(response.json()['answer'])
```

## 🏗️ Architecture

```
RAG Pipeline:
PDF → Chunking → Embeddings (OpenAI) → FAISS Index → Retrieval → LLM (GPT-4o-mini) → Answer
```

### Project Structure

```
rag-juridique/
├── src/
│   ├── extract_pdf.py    # PDF extraction and chunking
│   ├── embeddings.py     # Embeddings creation and FAISS indexing
│   ├── retrieval.py      # RAG search and generation
│   └── api.py            # FastAPI REST API
├── data/
│   └── pdfs/             # Your legal documents
├── index/                # FAISS index (generated)
├── ui.py                 # Gradio interface
└── requirements.txt      # Python dependencies
```

## 🛠️ Technologies

- **Python 3.11** - Main language
- **FastAPI** - Modern REST API framework
- **Gradio** - User interface
- **OpenAI API** - Embeddings (text-embedding-3-small) + LLM (gpt-4o-mini)
- **FAISS** - Ultra-fast vector search (Facebook AI)
- **PyMuPDF** - PDF text extraction

## 💰 Cost Estimation

### Models Used (most economical):

- **text-embedding-3-small**: $0.02 / 1M tokens
- **gpt-4o-mini**: $0.15 / 1M tokens (input), $0.60 / 1M tokens (output)

### Pricing:

- Initial setup (3 PDFs ~150 pages): ~$0.001
- Per question: ~$0.0005
- 100 questions: ~$0.05 (5 cents!)

## 📖 How It Works

1. **Documents** → Legal PDFs are placed in `data/pdfs/`
2. **Chunking** → Text is split into ~1000 word chunks with 200 word overlap
3. **Embeddings** → Each chunk is converted to a 1536-dimensional vector via OpenAI
4. **Indexing** → Vectors are indexed with FAISS for fast similarity search
5. **Query** → User asks a question
6. **Retrieval** → FAISS finds the 3 most relevant chunks
7. **Generation** → GPT-4o-mini generates an answer based on these chunks
8. **Response** → Answer is returned with source citations

## 🔧 Useful Commands

```bash
# Create/update index
python -m src.embeddings

# Launch API
uvicorn src.api:app --reload

# Launch Gradio UI
python ui.py

# Test API
curl "http://localhost:8000/ask?query=What+is+GDPR"

# View statistics
curl http://localhost:8000/stats
```

## 🌐 API Endpoints

| Endpoint    | Method | Description                       |
| ----------- | ------ | --------------------------------- |
| `/`         | GET    | API information                   |
| `/health`   | GET    | Health check                      |
| `/stats`    | GET    | Index statistics                  |
| `/ask`      | GET    | Ask a question (URL params)       |
| `/ask_post` | POST   | Ask a question (JSON body)        |
| `/docs`     | GET    | Interactive Swagger documentation |

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Report bugs
- Suggest improvements
- Add new features
- Improve documentation

## 📝 License

MIT License - Free to use for personal and educational projects.

## ⚠️ Disclaimers

- This assistant is for educational and demonstration purposes
- Always verify legal information with official sources
- Respect OpenAI's terms of service
- Answers are limited to indexed documents

## 🎓 Learning Objectives

This project is perfect for learning:

- RAG (Retrieval-Augmented Generation)
- Vector embeddings
- Similarity search with FAISS
- REST APIs with FastAPI
- User interfaces with Gradio
- PDF document processing

## 🙏 Credits

Built with ❤️ to learn RAG and FastAPI.

Technologies used:

- OpenAI for embeddings and LLM
- Facebook AI for FAISS
- Gradio for UI
- FastAPI for API

## 📞 Support

For questions or issues, check the documentation or open an issue on GitHub.

---

**Made with 🤖 and ⚖️ to make law accessible**
