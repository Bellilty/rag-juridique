# Makefile pour le projet RAG Juridique
# ======================================
# 
# Commandes utiles pour gérer le projet facilement
#
# Usage :
#   make help        - Affiche l'aide
#   make install     - Installe les dépendances
#   make index       - Crée l'index FAISS
#   make api         - Lance l'API
#   make test        - Teste le RAG

.PHONY: help install setup index api test clean

# Détection de l'OS
ifeq ($(OS),Windows_NT)
    PYTHON := python
    VENV_ACTIVATE := venv\Scripts\activate
else
    PYTHON := python3
    VENV_ACTIVATE := source venv/bin/activate
endif

help:
	@echo "🤖 Assistant Juridique RAG - Commandes disponibles"
	@echo ""
	@echo "  make install     - Installe les dépendances Python"
	@echo "  make setup       - Lance le script d'installation complet"
	@echo "  make index       - Crée l'index FAISS depuis les PDFs"
	@echo "  make api         - Lance l'API FastAPI (http://localhost:8000)"
	@echo "  make test        - Teste le RAG en ligne de commande"
	@echo "  make clean       - Nettoie les fichiers générés"
	@echo "  make stats       - Affiche les statistiques du projet"
	@echo ""
	@echo "🚀 Workflow typique :"
	@echo "  1. make install"
	@echo "  2. Ajoute des PDFs dans data/pdfs/"
	@echo "  3. Crée un fichier .env avec OPENAI_API_KEY=..."
	@echo "  4. make index"
	@echo "  5. make api"

install:
	@echo "📦 Installation des dépendances..."
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt
	@echo "✅ Installation terminée!"

setup:
	@echo "🛠️  Lancement du script d'installation..."
	$(PYTHON) setup.py

index:
	@echo "🏗️  Création de l'index FAISS..."
	$(PYTHON) -m src.embeddings
	@echo "✅ Index créé!"

api:
	@echo "🚀 Lancement de l'API..."
	@echo "📖 Documentation : http://localhost:8000/docs"
	uvicorn src.api:app --reload --port 8000

test:
	@echo "🧪 Test du système RAG..."
	$(PYTHON) test_rag.py

clean:
	@echo "🧹 Nettoyage des fichiers générés..."
	rm -rf index/*.faiss index/*.pkl
	rm -rf __pycache__ src/__pycache__
	rm -rf .pytest_cache
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	@echo "✅ Nettoyage terminé!"

stats:
	@echo "📊 Statistiques du projet"
	@echo ""
	@echo "📄 PDFs :"
	@if [ -d "data/pdfs" ]; then \
		PDF_COUNT=$$(ls data/pdfs/*.pdf 2>/dev/null | wc -l); \
		if [ $$PDF_COUNT -gt 0 ]; then \
			echo "  $$PDF_COUNT PDF(s) trouvé(s) :"; \
			ls -lh data/pdfs/*.pdf 2>/dev/null; \
		else \
			echo "  ⚠️  Aucun PDF trouvé"; \
		fi \
	else \
		echo "  ⚠️  Dossier data/pdfs/ inexistant"; \
	fi
	@echo ""
	@echo "📊 Index :"
	@if [ -f "index/legal.faiss" ]; then \
		echo "  ✅ Index FAISS : $$(ls -lh index/legal.faiss | awk '{print $$5}')"; \
		echo "  ✅ Chunks : $$(ls -lh index/chunks.pkl | awk '{print $$5}')"; \
	else \
		echo "  ⚠️  Index non créé (lance 'make index')"; \
	fi
	@echo ""
	@echo "🔑 Configuration :"
	@if [ -f ".env" ]; then \
		echo "  ✅ Fichier .env présent"; \
	else \
		echo "  ⚠️  Fichier .env manquant"; \
	fi
	@echo ""
	@echo "📦 Lignes de code :"
	@find src -name "*.py" -exec wc -l {} + | tail -1 | awk '{print "  Python : " $$1 " lignes"}'

# Commandes de développement avancées

dev-install:
	@echo "🔧 Installation en mode développement..."
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) -m pip install pytest black flake8 mypy
	@echo "✅ Installation développeur terminée!"

format:
	@echo "✨ Formatage du code avec Black..."
	black src/ *.py
	@echo "✅ Code formaté!"

lint:
	@echo "🔍 Vérification du code avec Flake8..."
	flake8 src/ --max-line-length=100 --ignore=E203,W503
	@echo "✅ Vérification terminée!"

type-check:
	@echo "🔍 Vérification des types avec MyPy..."
	mypy src/ --ignore-missing-imports
	@echo "✅ Types vérifiés!"

