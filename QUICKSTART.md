# 🚀 Guide de Démarrage Rapide

**Temps estimé : 10 minutes** ⏱️

Ce guide te permet de lancer ton assistant juridique RAG en quelques étapes simples.

---

## ✅ Prérequis

Avant de commencer, assure-toi d'avoir :

- [ ] Python 3.10 ou supérieur installé
- [ ] Une clé API OpenAI ([créer ici](https://platform.openai.com/api-keys))
- [ ] ~$0.01 de crédit OpenAI (pour tester)

---

## 📝 Étapes d'installation

### 1️⃣ Active l'environnement virtuel

```bash
# Le venv a déjà été créé, active-le :
source venv/bin/activate

# Sur Windows :
# .\venv\Scripts\activate

# Tu devrais voir (venv) dans ton terminal
```

### 2️⃣ Installe les dépendances

**Option A : Script automatique (recommandé)**

```bash
python setup.py
```

Ce script va tout faire automatiquement ! ✨

**Option B : Installation manuelle**

```bash
# Installe les packages Python
pip install -r requirements.txt

# Crée le fichier .env
echo "OPENAI_API_KEY=ta-clé-ici" > .env
```

### 3️⃣ Ajoute des documents PDF

Place 1-2 PDFs juridiques dans `data/pdfs/` :

```bash
# Exemple : télécharge la Constitution US
cd data/pdfs/
curl -O https://www.archives.gov/files/legislative/resources/us-constitution.pdf
cd ../..
```

**Suggestions :**

- GDPR : https://gdpr-info.eu/ (sauvegarde en PDF)
- U.S. Constitution : https://www.archives.gov/founding-docs
- N'importe quel PDF juridique public !

### 4️⃣ Crée l'index FAISS

```bash
python -m src.embeddings
```

**Ce script va :**

1. Extraire le texte des PDFs ✂️
2. Découper en chunks 🔪
3. Créer les embeddings 🔢
4. Construire l'index FAISS 📊

**Durée :** 1-3 minutes selon le nombre de PDFs

### 5️⃣ Lance l'API

```bash
uvicorn src.api:app --reload
```

**L'API est maintenant disponible sur :**

- API : http://localhost:8000
- Documentation : http://localhost:8000/docs

---

## 🧪 Test rapide

### Via le navigateur

Ouvre cette URL dans ton navigateur :

```
http://localhost:8000/ask?query=What+is+GDPR
```

### Via curl

```bash
curl "http://localhost:8000/ask?query=What+is+the+main+purpose+of+GDPR&k=3"
```

### Via la documentation Swagger

1. Va sur http://localhost:8000/docs
2. Clique sur `/ask` → `Try it out`
3. Entre ta question dans `query`
4. Clique sur `Execute`

### Via Python

```python
import requests

response = requests.get(
    "http://localhost:8000/ask",
    params={"query": "What are personal data?"}
)

print(response.json()['answer'])
```

---

## 🎯 Commandes utiles

Si tu as installé `make` (Linux/Mac) :

```bash
make help      # Affiche toutes les commandes
make api       # Lance l'API
make test      # Test en ligne de commande
make stats     # Statistiques du projet
make clean     # Nettoie les fichiers générés
```

Sinon, utilise directement :

```bash
# Lance l'API
uvicorn src.api:app --reload

# Test interactif
python test_rag.py

# Recrée l'index
python -m src.embeddings
```

---

## 📊 Exemples de questions

### 🇬🇧 Anglais (GDPR)

```
- What is the GDPR?
- What are the main principles of data protection?
- Who is a data controller?
- What are the rights of data subjects?
- What is personal data?
- What are the penalties for non-compliance?
```

### 🇺🇸 Anglais (U.S. Constitution)

```
- What does the First Amendment say?
- What are the branches of government?
- What is the Bill of Rights?
- How can the Constitution be amended?
```

### 🇫🇷 Français (Code civil)

```
- Qu'est-ce que la responsabilité civile ?
- Quels sont les droits de propriété ?
- Qu'est-ce qu'un contrat ?
```

---

## 🐛 Dépannage rapide

### Problème : "Module not found"

```bash
# Vérifie que le venv est activé
which python  # Doit pointer vers venv/bin/python

# Réinstalle
pip install -r requirements.txt
```

### Problème : "OPENAI_API_KEY not found"

```bash
# Vérifie le fichier .env
cat .env

# Doit contenir :
# OPENAI_API_KEY=sk-...

# Si manquant, crée-le :
echo "OPENAI_API_KEY=ta-clé-ici" > .env
```

### Problème : "Index not found"

```bash
# Crée l'index
python -m src.embeddings

# Vérifie qu'il existe
ls -l index/
```

### Problème : "No PDFs found"

```bash
# Vérifie le contenu
ls data/pdfs/

# Ajoute au moins un PDF
# Puis recrée l'index
python -m src.embeddings
```

---

## 💡 Prochaines étapes

### Niveau 1 : Débutant

1. ✅ Lance l'API et teste différentes questions
2. ✅ Ajoute plus de PDFs et recrée l'index
3. ✅ Explore la documentation Swagger
4. ✅ Teste avec `python test_rag.py`

### Niveau 2 : Intermédiaire

1. Modifie les paramètres de chunking dans `extract_pdf.py`
2. Teste différents modèles (gpt-3.5-turbo vs gpt-4o-mini)
3. Expérimente avec le paramètre `k` (nombre de chunks)
4. Regarde les logs pour comprendre le processus

### Niveau 3 : Avancé

1. Ajoute des métadonnées aux chunks (numéro d'article, page, etc.)
2. Implémente un cache pour les questions fréquentes
3. Crée une interface utilisateur avec Streamlit
4. Compare avec d'autres embeddings (Cohere, HuggingFace)
5. Essaye un LLM local avec Ollama (mode 100% offline)

---

## 📚 Comprendre le code

### Architecture en 4 modules

```
src/extract_pdf.py   → Extraction et chunking
        ↓
src/embeddings.py    → Création embeddings + FAISS
        ↓
src/retrieval.py     → Recherche + génération RAG
        ↓
src/api.py          → API FastAPI
```

### Flux d'une question

```
1. Question → /ask?query=...
2. API (api.py) → retriever.ask(query)
3. Retrieval (retrieval.py) → Vectorise la question
4. FAISS → Trouve les 3 chunks les plus proches
5. Retrieval → Construit le prompt avec contexte
6. OpenAI → Génère la réponse
7. API → Retourne JSON avec réponse + métadonnées
```

---

## 💰 Coûts approximatifs

### Setup initial (une fois)

- 50 pages de PDF : ~**$0.001**

### Par question

- Embedding de la question : ~**$0.0000004**
- Génération de la réponse : ~**$0.0005**

### Total pour 100 questions

- ~**$0.05** (5 centimes d'euro) 💰

---

## 🎉 Bravo !

Tu as maintenant un système RAG fonctionnel ! 🚀

**Questions ?** Consulte le [README.md](README.md) complet pour plus de détails.

**Prêt à aller plus loin ?** Explore les améliorations possibles dans le README.

---

## 🆘 Besoin d'aide ?

1. **Erreur Python** → Vérifie que le venv est activé
2. **Erreur API** → Vérifie ta clé OpenAI
3. **Pas de résultats** → Vérifie que l'index existe
4. **Réponse bizarre** → Essaye avec plus de chunks (k=5)

**Commande magique de reset** :

```bash
# Nettoie tout et recommence
rm -rf index/
python -m src.embeddings
uvicorn src.api:app --reload
```

---

**Happy RAG-ing! 🤖✨**
