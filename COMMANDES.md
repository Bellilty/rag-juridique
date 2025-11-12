# 📝 Aide-mémoire des Commandes

Guide rapide de toutes les commandes utiles pour le projet.

---

## 🚀 Démarrage Rapide

```bash
# 1. Active l'environnement virtuel
source venv/bin/activate

# 2. Installe les dépendances
pip install -r requirements.txt

# 3. Configure la clé API
echo "OPENAI_API_KEY=ta-clé-ici" > .env

# 4. Ajoute des PDFs dans data/pdfs/

# 5. Crée l'index
python -m src.embeddings

# 6. Lance l'API
uvicorn src.api:app --reload
```

---

## 📦 Gestion de l'environnement

### Environnement virtuel

```bash
# Créer (déjà fait)
python3 -m venv venv

# Activer
source venv/bin/activate              # Linux/Mac
.\venv\Scripts\activate               # Windows

# Désactiver
deactivate

# Vérifier qu'il est activé
which python                          # Doit pointer vers venv/bin/python
```

### Installation des dépendances

```bash
# Installation normale
pip install -r requirements.txt

# Installation + mise à jour
pip install --upgrade -r requirements.txt

# Vérifier les packages installés
pip list

# Vérifier une dépendance spécifique
pip show openai
pip show faiss-cpu
```

---

## 🔑 Configuration

### Clé API OpenAI

```bash
# Méthode 1 : Créer le fichier .env
echo "OPENAI_API_KEY=sk-votre-clé" > .env

# Méthode 2 : Copier depuis l'exemple
cp env.example .env
# Puis éditer avec nano/vim/code

# Vérifier
cat .env

# Variable d'environnement temporaire (session uniquement)
export OPENAI_API_KEY="sk-votre-clé"
```

---

## 📄 Gestion des PDFs

### Ajouter des documents

```bash
# Se déplacer dans le dossier
cd data/pdfs/

# Télécharger un PDF (exemple)
curl -O https://example.com/document.pdf
wget https://example.com/document.pdf

# Copier depuis un autre dossier
cp ~/Downloads/GDPR.pdf .

# Lister les PDFs présents
ls -lh *.pdf

# Compter les PDFs
ls *.pdf | wc -l

# Revenir à la racine
cd ../..
```

### Vérifier les PDFs

```bash
# Taille totale des PDFs
du -sh data/pdfs/

# Détails de chaque PDF
ls -lh data/pdfs/*.pdf

# Nombre de pages (nécessite pdfinfo)
pdfinfo data/pdfs/GDPR.pdf | grep Pages
```

---

## 🏗️ Création de l'index

### Commandes principales

```bash
# Créer l'index depuis les PDFs
python -m src.embeddings

# Avec affichage détaillé
python -m src.embeddings --verbose

# Recréer (supprime l'ancien)
rm -rf index/
python -m src.embeddings
```

### Vérifier l'index

```bash
# Vérifier que l'index existe
ls -lh index/

# Devrait afficher :
# legal.faiss  (l'index FAISS)
# chunks.pkl   (les chunks de texte)

# Taille de l'index
du -sh index/

# Informations détaillées
file index/legal.faiss
file index/chunks.pkl
```

---

## 🌐 API FastAPI

### Lancer l'API

```bash
# Lancement standard
uvicorn src.api:app --reload

# Spécifier le port
uvicorn src.api:app --reload --port 8000

# Écouter sur toutes les interfaces (pour accès réseau)
uvicorn src.api:app --reload --host 0.0.0.0 --port 8000

# Sans auto-reload (production)
uvicorn src.api:app --host 0.0.0.0 --port 8000

# Avec plus de workers (production)
uvicorn src.api:app --workers 4
```

### Arrêter l'API

```bash
# Dans le terminal : Ctrl+C

# Si bloqué :
# 1. Trouve le process
ps aux | grep uvicorn

# 2. Tue le process
kill -9 <PID>

# Ou en une ligne
pkill -f uvicorn
```

---

## 🧪 Tests et requêtes

### Test en ligne de commande

```bash
# Script interactif
python test_rag.py

# Test d'un module spécifique
python -m src.extract_pdf
python -m src.embeddings
python -m src.retrieval
```

### Requêtes HTTP

#### Avec curl

```bash
# Question simple
curl "http://localhost:8000/ask?query=What+is+GDPR"

# Avec paramètres
curl "http://localhost:8000/ask?query=What+is+personal+data&k=3&model=gpt-4o-mini"

# Format JSON (jq pour formater)
curl -s "http://localhost:8000/ask?query=What+is+GDPR" | jq

# Health check
curl http://localhost:8000/health

# Statistiques
curl http://localhost:8000/stats
```

#### Avec httpie (plus lisible)

```bash
# Installation
pip install httpie

# Requêtes
http GET localhost:8000/ask query=="What is GDPR" k==3
http GET localhost:8000/health
http GET localhost:8000/stats
```

#### Avec Python

```python
import requests

# GET
response = requests.get(
    "http://localhost:8000/ask",
    params={
        "query": "What is GDPR?",
        "k": 3,
        "model": "gpt-4o-mini"
    }
)
print(response.json())

# POST
response = requests.post(
    "http://localhost:8000/ask_post",
    json={
        "query": "What is personal data?",
        "k": 3,
        "model": "gpt-4o-mini"
    }
)
print(response.json()['answer'])
```

---

## 📊 Monitoring et Debug

### Logs de l'API

```bash
# Lancer avec logs détaillés
uvicorn src.api:app --reload --log-level debug

# Sauvegarder les logs
uvicorn src.api:app --reload > logs.txt 2>&1

# Suivre les logs en temps réel
tail -f logs.txt
```

### Statistiques du projet

```bash
# Via Make
make stats

# Manuellement
echo "=== PDFs ==="
ls -lh data/pdfs/*.pdf
echo "=== Index ==="
ls -lh index/
echo "=== Code ==="
find src -name "*.py" -exec wc -l {} + | tail -1
```

### Vérifications

```bash
# Python version
python --version

# Packages installés
pip list | grep -E "openai|faiss|fastapi"

# Variables d'environnement
env | grep OPENAI

# Espace disque
df -h .

# Processus Python en cours
ps aux | grep python
```

---

## 🧹 Nettoyage

### Nettoyer l'index

```bash
# Supprimer l'index
rm -rf index/

# Supprimer + recréer
rm -rf index/ && python -m src.embeddings
```

### Nettoyer les fichiers Python

```bash
# Via Make
make clean

# Manuellement
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete
```

### Nettoyage complet

```bash
# Tout sauf les PDFs et le code
rm -rf index/
rm -rf __pycache__ src/__pycache__
rm -f .env
```

---

## 🛠️ Makefile (si disponible)

```bash
# Aide
make help

# Installation
make install

# Setup complet
make setup

# Créer l'index
make index

# Lancer l'API
make api

# Test
make test

# Statistiques
make stats

# Nettoyer
make clean
```

---

## 🐛 Dépannage

### Problème : Module not found

```bash
# Vérifier l'activation du venv
which python
# Si ne pointe pas vers venv/, active-le :
source venv/bin/activate

# Réinstaller
pip install -r requirements.txt
```

### Problème : FAISS installation failed

```bash
# Mac avec Apple Silicon
pip install faiss-cpu --no-cache-dir

# Linux
pip install faiss-cpu==1.8.0

# Windows
pip install faiss-cpu==1.7.4
```

### Problème : Port déjà utilisé

```bash
# Trouver quel process utilise le port 8000
lsof -i :8000

# Tuer le process
kill -9 <PID>

# Ou utiliser un autre port
uvicorn src.api:app --reload --port 8001
```

### Problème : API ne démarre pas

```bash
# Vérifier l'index
ls -l index/

# Vérifier la clé API
cat .env

# Tester manuellement
python -c "from src.embeddings import EmbeddingManager; m = EmbeddingManager(); print(m.index_exists())"
```

---

## 📚 Documentation

### Accès aux docs

```bash
# Lancer l'API puis ouvrir :
open http://localhost:8000/docs        # Swagger UI
open http://localhost:8000/redoc       # ReDoc
open http://localhost:8000              # Info de base
```

### Générer de la doc (si sphinx installé)

```bash
# Installer sphinx
pip install sphinx sphinx-rtd-theme

# Générer la doc
cd docs/
sphinx-quickstart
sphinx-apidoc -o source/ ../src/
make html

# Ouvrir
open build/html/index.html
```

---

## 🔄 Workflow Typique

### Développement quotidien

```bash
# 1. Active l'environnement
source venv/bin/activate

# 2. Lance l'API
uvicorn src.api:app --reload

# 3. Dans un autre terminal, teste
python test_rag.py

# 4. Modifie le code (l'API recharge automatiquement)

# 5. Désactive quand tu as fini
deactivate
```

### Ajouter un nouveau document

```bash
# 1. Ajoute le PDF
cp ~/Downloads/nouveau-doc.pdf data/pdfs/

# 2. Recrée l'index
python -m src.embeddings

# 3. Relance l'API (elle recharge l'index)
# Ctrl+C puis :
uvicorn src.api:app --reload
```

### Expérimenter avec les paramètres

```bash
# Tester différentes tailles de chunks
# Édite src/extract_pdf.py :
# chunk_size = 500  # au lieu de 1000

# Recrée l'index
rm -rf index/
python -m src.embeddings

# Compare les résultats
python test_rag.py
```

---

## 🚀 Commandes de production

### Préparer pour la production

```bash
# Créer un fichier requirements-prod.txt
pip freeze > requirements-prod.txt

# Configuration production dans .env
cat > .env << EOF
OPENAI_API_KEY=sk-prod-key
ENVIRONMENT=production
LOG_LEVEL=info
EOF

# Lancer en production
uvicorn src.api:app --host 0.0.0.0 --port 8000 --workers 4
```

### Avec Docker (si configuré)

```bash
# Build
docker build -t rag-juridique .

# Run
docker run -p 8000:8000 -v $(pwd)/data:/app/data rag-juridique

# Compose
docker-compose up -d
```

---

## 💡 Raccourcis utiles

### Aliases (à ajouter dans ~/.bashrc ou ~/.zshrc)

```bash
# Ajoute ces lignes dans ton fichier de config :
alias rag-activate='source venv/bin/activate'
alias rag-api='uvicorn src.api:app --reload'
alias rag-test='python test_rag.py'
alias rag-index='python -m src.embeddings'
alias rag-clean='rm -rf index/ __pycache__ src/__pycache__'

# Puis recharge :
source ~/.bashrc  # ou ~/.zshrc
```

Maintenant tu peux simplement taper :
```bash
rag-activate
rag-api
```

---

## 📖 Ressources

- **README.md** : Documentation complète
- **QUICKSTART.md** : Guide de démarrage rapide
- **CONCEPTS.md** : Explications détaillées des concepts
- **docs/** : Documentation Swagger automatique

---

**Garde ce fichier sous la main pour référence rapide ! 📌**

