# 🤖 Assistant Juridique RAG Local

Un projet pédagogique pour apprendre le **RAG (Retrieval-Augmented Generation)** et **FastAPI** en créant un assistant juridique local qui répond à des questions sur des documents légaux.

## 📚 Table des matières

- [Concept](#-concept)
- [Architecture](#-architecture)
- [Technologies utilisées](#-technologies-utilisées)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Structure du projet](#-structure-du-projet)
- [Explications détaillées](#-explications-détaillées)
- [Coûts](#-coûts)
- [Améliorations possibles](#-améliorations-possibles)

---

## 🎯 Concept

### Qu'est-ce que le RAG ?

**RAG = Retrieval-Augmented Generation**

C'est une technique qui combine :

1. **Retrieval (Récupération)** : Chercher des informations pertinentes dans une base de documents
2. **Augmented (Enrichissement)** : Ajouter ces informations au contexte du LLM
3. **Generation (Génération)** : Le LLM génère une réponse basée sur ce contexte

### Pourquoi le RAG ?

Sans RAG :

- ❌ Le LLM répond avec ses connaissances générales (peut être obsolète)
- ❌ Risque d'hallucinations (inventer des informations)
- ❌ Pas de sources vérifiables

Avec RAG :

- ✅ Le LLM répond avec **VOS** documents
- ✅ Réponses factuelles basées sur des sources réelles
- ✅ Citations des sources
- ✅ Contrôle total sur les données

### Ce que fait ce projet

```
📄 PDFs juridiques (GDPR, Constitution, etc.)
    ↓
🔪 Découpage en chunks (morceaux de texte)
    ↓
🔢 Création d'embeddings (vecteurs)
    ↓
📊 Indexation avec FAISS (recherche rapide)
    ↓
❓ Question utilisateur
    ↓
🔍 Recherche des passages pertinents
    ↓
🤖 Génération de la réponse avec OpenAI
    ↓
💬 Réponse + citations
```

---

## 🏗️ Architecture

### Modules principaux

| Module           | Rôle                                   | Technologies      |
| ---------------- | -------------------------------------- | ----------------- |
| `extract_pdf.py` | Extraction et chunking des PDFs        | PyMuPDF           |
| `embeddings.py`  | Création des embeddings et index FAISS | OpenAI API, FAISS |
| `retrieval.py`   | Recherche et génération RAG            | OpenAI API, FAISS |
| `api.py`         | API REST                               | FastAPI           |

### Flux de données

```
┌─────────────┐
│  data/pdfs/ │  Dossier contenant les PDFs
└──────┬──────┘
       │
       │ extract_pdf.py
       ↓
┌─────────────┐
│   Chunks    │  Texte découpé en morceaux
└──────┬──────┘
       │
       │ embeddings.py + OpenAI
       ↓
┌─────────────┐
│  Embeddings │  Vecteurs numériques
└──────┬──────┘
       │
       │ FAISS
       ↓
┌─────────────┐
│ index/      │  Index FAISS + chunks.pkl
│ legal.faiss │
│ chunks.pkl  │
└──────┬──────┘
       │
       │ api.py
       ↓
┌─────────────┐
│  FastAPI    │  http://localhost:8000
└─────────────┘
```

---

## 🛠️ Technologies utilisées

### Backend

- **Python 3.10+** : Langage principal
- **FastAPI** : Framework web moderne et rapide
- **Uvicorn** : Serveur ASGI pour FastAPI

### RAG & IA

- **OpenAI API** :
  - `text-embedding-3-small` : Création d'embeddings (~$0.02/1M tokens)
  - `gpt-4o-mini` : Génération de réponses (~$0.15/1M tokens input)
- **FAISS** : Recherche vectorielle ultra-rapide (Facebook AI)
- **PyMuPDF (fitz)** : Extraction de texte depuis PDFs

### Utilitaires

- **NumPy** : Calculs sur les vecteurs
- **Pydantic** : Validation des données
- **python-dotenv** : Gestion des variables d'environnement

---

## 📦 Installation

### 1. Prérequis

- Python 3.10 ou supérieur
- pip
- Une clé API OpenAI ([créer une clé](https://platform.openai.com/api-keys))

### 2. Cloner le projet

```bash
cd /chemin/vers/rag-juridique
```

### 3. Créer l'environnement virtuel

```bash
# Création du venv
python3 -m venv venv

# Activation
source venv/bin/activate  # Linux/Mac
# OU
.\venv\Scripts\activate  # Windows
```

### 4. Installation automatique (recommandé)

```bash
python setup.py
```

Ce script va :

- Installer les dépendances
- Configurer la clé API
- Proposer de télécharger des données de démo
- Créer l'index FAISS

### 5. Installation manuelle

```bash
# Installer les dépendances
pip install -r requirements.txt

# Créer le fichier .env


# Ajouter des PDFs dans data/pdfs/
# (par exemple : GDPR, Constitution US, etc.)

# Créer l'index FAISS
python -m src.embeddings
```

---

## 🚀 Utilisation

### 1. Ajouter des documents

Place tes PDFs juridiques dans le dossier `data/pdfs/`.

**Suggestions de sources gratuites :**

- 🇪🇺 [GDPR](https://gdpr-info.eu/) - Règlement européen sur la protection des données
- 🇺🇸 [U.S. Constitution](https://www.archives.gov/founding-docs) - Constitution américaine
- 🇫🇷 [Code civil français](https://www.legifrance.gouv.fr/codes/id/LEGITEXT000006070721/) - Légifrance

### 2. Créer l'index FAISS

```bash
python -m src.embeddings
```

Ce script va :

1. Extraire le texte des PDFs
2. Découper en chunks
3. Créer les embeddings via OpenAI
4. Créer l'index FAISS
5. Sauvegarder dans `index/`

**Durée** : ~1-2 minutes pour 2-3 PDFs de taille moyenne

### 3. Lancer l'API

```bash
uvicorn src.api:app --reload
```

L'API sera accessible sur : `http://localhost:8000`

### 4. Tester l'API

#### Via le navigateur

```
http://localhost:8000/ask?query=What%20is%20GDPR
```

#### Via la documentation Swagger

Ouvre `http://localhost:8000/docs` pour une interface interactive complète !

#### Via curl

```bash
curl "http://localhost:8000/ask?query=What%20is%20GDPR&k=3"
```

#### Via Python

```python
import requests

response = requests.get(
    "http://localhost:8000/ask",
    params={
        "query": "What are the main principles of GDPR?",
        "k": 3,
        "model": "gpt-4o-mini"
    }
)

result = response.json()
print(result['answer'])
```

### 5. Exemples de questions

```
🇫🇷 Français :
- "Quel est l'article sur la responsabilité civile ?"
- "Que dit la loi sur la protection des données ?"

🇺🇸 Anglais :
- "What is Article 5 of GDPR about?"
- "What are data subject rights under GDPR?"
- "Who is the data controller?"
```

---

## 📂 Structure du projet

```
rag-juridique/
│
├── venv/                      # Environnement virtuel Python
│
├── data/
│   └── pdfs/                  # 📄 Place tes PDFs ici
│       ├── GDPR.pdf
│       └── US_Constitution.pdf
│
├── src/
│   ├── __init__.py
│   ├── extract_pdf.py         # 🔪 Extraction et chunking
│   ├── embeddings.py          # 🔢 Embeddings + FAISS
│   ├── retrieval.py           # 🔍 Recherche et génération RAG
│   └── api.py                 # 🌐 API FastAPI
│
├── index/
│   ├── legal.faiss            # 📊 Index FAISS (généré)
│   └── chunks.pkl             # 💾 Chunks sauvegardés (généré)
│
├── requirements.txt           # 📦 Dépendances Python
├── setup.py                   # 🛠️ Script d'installation
├── .env                       # 🔑 Clé API (à créer)
├── .gitignore
└── README.md                  # 📖 Ce fichier
```

---

## 🧠 Explications détaillées

### 1. Extraction et Chunking (`extract_pdf.py`)

#### Pourquoi découper en chunks ?

- Les LLMs ont une **limite de tokens** dans leur contexte
- Les petits morceaux permettent une **recherche plus précise**
- L'**overlap** (chevauchement) évite de couper des phrases importantes

#### Paramètres du chunking

```python
chunk_size = 1000    # Nombre de mots par chunk
overlap = 200        # Mots qui se chevauchent entre chunks
```

**Exemple :**

```
Texte original : "Article 1. [...] Article 2. [...] Article 3. [...]"

Chunk 1 : "Article 1. [...] Article 2. [premiers mots]"
Chunk 2 : "[derniers mots Article 1] Article 2. [...] Article 3. [...]"
         ↑ overlap (évite de perdre du contexte)
```

### 2. Embeddings (`embeddings.py`)

#### Qu'est-ce qu'un embedding ?

Un **embedding** est une représentation vectorielle d'un texte.

```python
texte = "GDPR protects personal data"
embedding = [0.123, -0.456, 0.789, ...]  # 1536 dimensions
```

**Propriété magique** : Les textes similaires ont des vecteurs proches !

```python
"data protection" → [0.1, 0.2, 0.3, ...]
"privacy law"     → [0.12, 0.19, 0.31, ...]  # Proche !
"pizza recipe"    → [0.9, -0.5, 0.1, ...]    # Loin !
```

#### Pourquoi OpenAI `text-embedding-3-small` ?

- ✅ Moins cher (~$0.02/1M tokens)
- ✅ Performance excellente
- ✅ 1536 dimensions (bon équilibre)
- ✅ Multilingue

### 3. FAISS

#### Qu'est-ce que FAISS ?

**FAISS** (Facebook AI Similarity Search) est une bibliothèque pour rechercher des vecteurs similaires **ultra-rapidement**.

**Sans FAISS** :

```python
# Comparer la question avec TOUS les chunks (lent!)
for chunk in chunks:
    distance = calculate_distance(query_vector, chunk_vector)
```

**Avec FAISS** :

```python
# Index optimisé, recherche instantanée même avec 1M de vecteurs
index.search(query_vector, k=3)  # Trouve les 3 plus proches en millisecondes
```

#### Types d'index FAISS

| Index         | Précision | Vitesse     | Usage                     |
| ------------- | --------- | ----------- | ------------------------- |
| `IndexFlatL2` | 100%      | Moyen       | < 1M vecteurs (notre cas) |
| `IndexIVF`    | ~95%      | Rapide      | > 1M vecteurs             |
| `IndexHNSW`   | ~99%      | Très rapide | Production                |

**Pour ce projet** : `IndexFlatL2` suffit largement !

### 4. Retrieval-Augmented Generation (`retrieval.py`)

#### Le processus RAG en détail

```python
# 1. L'utilisateur pose une question
query = "What is GDPR?"

# 2. On vectorise la question
query_vector = create_embedding(query)
# → [0.1, 0.2, 0.3, ...]

# 3. FAISS trouve les chunks les plus proches
distances, indices = index.search(query_vector, k=3)
# → Retourne les 3 chunks les plus pertinents

# 4. On construit le contexte
context = "\n\n".join([chunks[i] for i in indices])

# 5. On construit le prompt pour le LLM
prompt = f"""
You are a legal assistant.
Answer based ONLY on this context:

{context}

Question: {query}
"""

# 6. Le LLM génère la réponse
answer = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)
```

#### Pourquoi `gpt-4o-mini` ?

| Modèle        | Prix (input) | Prix (output) | Qualité            |
| ------------- | ------------ | ------------- | ------------------ |
| gpt-4o-mini   | $0.15/1M     | $0.60/1M      | ⭐⭐⭐⭐ Excellent |
| gpt-3.5-turbo | $0.50/1M     | $1.50/1M      | ⭐⭐⭐ Bon         |
| gpt-4         | $30/1M       | $60/1M        | ⭐⭐⭐⭐⭐ Parfait |

**Verdict** : `gpt-4o-mini` offre le **meilleur rapport qualité/prix** !

### 5. API FastAPI (`api.py`)

#### Pourquoi FastAPI ?

- ✅ **Rapide** : Performance comparable à NodeJS
- ✅ **Documentation auto** : Swagger UI intégré
- ✅ **Validation** : Pydantic vérifie les données automatiquement
- ✅ **Async** : Support natif des opérations asynchrones
- ✅ **Moderne** : Type hints Python 3.6+

#### Endpoints disponibles

| Endpoint    | Méthode | Description                        |
| ----------- | ------- | ---------------------------------- |
| `/`         | GET     | Infos sur l'API                    |
| `/health`   | GET     | Vérifie l'état de l'API            |
| `/stats`    | GET     | Statistiques sur l'index           |
| `/ask`      | GET     | Pose une question (paramètres URL) |
| `/ask_post` | POST    | Pose une question (JSON body)      |
| `/docs`     | GET     | Documentation Swagger              |
| `/redoc`    | GET     | Documentation ReDoc                |

---

## 💰 Coûts

### Estimation des coûts OpenAI

Pour **100 questions** sur **3 PDFs** (~50 pages chacun) :

| Étape                | Opération           | Tokens | Coût unitaire                  | Coût total |
| -------------------- | ------------------- | ------ | ------------------------------ | ---------- |
| **Setup** (une fois) | Embeddings création | ~50K   | $0.02/1M                       | **$0.001** |
| **Par question**     | Embedding query     | ~20    | $0.02/1M                       | $0.0000004 |
| **Par question**     | LLM génération      | ~1000  | $0.15/1M (in) + $0.60/1M (out) | $0.0005    |

**Total pour 100 questions** : ~**$0.05** 💰

### Comparaison avec d'autres solutions

| Solution               | Coût pour 100 questions | Limitations                    |
| ---------------------- | ----------------------- | ------------------------------ |
| **Ce projet (OpenAI)** | $0.05                   | Aucune                         |
| ChatGPT Plus           | $20/mois                | Pas de données custom          |
| Claude Pro             | $20/mois                | Pas de données custom          |
| Ollama (local)         | $0 (gratuit)            | Nécessite GPU, qualité moindre |

---

## 🚀 Améliorations possibles

### 1. Support de plus de formats

```python
# Ajouter support pour .txt, .docx, .html
from docx import Document
from bs4 import BeautifulSoup
```

### 2. Interface utilisateur

```bash
pip install streamlit

# Créer une UI simple
streamlit run ui.py
```

### 3. Mode 100% offline avec Ollama

```python
# Remplacer OpenAI par Ollama (LLM local)
from langchain.llms import Ollama

llm = Ollama(model="mistral")
```

### 4. Métadonnées enrichies

```python
chunk = {
    "text": "...",
    "source": "GDPR.pdf",
    "article": "Article 5",    # ← Nouveau !
    "page": 12,                # ← Nouveau !
    "section": "Principles"    # ← Nouveau !
}
```

### 5. Index multi-lois avec filtres

```python
# Chercher uniquement dans le GDPR
results = retriever.search(
    query="data protection",
    filters={"source": "GDPR.pdf"}
)
```

### 6. Cache des questions fréquentes

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def ask_cached(query: str):
    return retriever.ask(query)
```

### 7. Système de feedback

```python
@app.post("/feedback")
def submit_feedback(query: str, helpful: bool):
    # Stocker pour améliorer le système
    save_feedback(query, helpful)
```

---

## 🎓 Concepts clés appris

En complétant ce projet, tu auras appris :

### RAG

- ✅ Comment fonctionne la recherche sémantique
- ✅ Le principe des embeddings vectoriels
- ✅ L'utilisation de FAISS pour la recherche rapide
- ✅ Comment enrichir un LLM avec des données externes

### FastAPI

- ✅ Créer une API REST moderne
- ✅ Validation automatique avec Pydantic
- ✅ Documentation auto avec Swagger
- ✅ Gestion des erreurs et des états

### Bonnes pratiques

- ✅ Environnements virtuels Python
- ✅ Gestion des secrets (.env)
- ✅ Structure modulaire d'un projet
- ✅ Documentation complète

---

## 🐛 Dépannage

### Problème : "Clé API non trouvée"

```bash
# Vérifie que le fichier .env existe
ls -la .env

# Vérifie le contenu
cat .env

# Doit contenir :
OPENAI_API_KEY=sk-...
```

### Problème : "Index non trouvé"

```bash
# Crée l'index
python -m src.embeddings

# Vérifie qu'il existe
ls -la index/
```

### Problème : "Module not found"

```bash
# Vérifie que le venv est activé
which python  # Doit pointer vers venv/bin/python

# Réinstalle les dépendances
pip install -r requirements.txt
```

### Problème : "FAISS installation failed"

```bash
# Sur Mac avec Apple Silicon
pip install faiss-cpu --no-cache

# Sur Windows
pip install faiss-cpu==1.7.4
```

---

## 📚 Ressources supplémentaires

### Documentation officielle

- [OpenAI API](https://platform.openai.com/docs)
- [FastAPI](https://fastapi.tiangolo.com/)
- [FAISS](https://github.com/facebookresearch/faiss)
- [LangChain](https://python.langchain.com/) (framework RAG plus avancé)

### Tutoriels

- [RAG from Scratch](https://www.youtube.com/watch?v=sVcwVQRHIc8) (vidéo)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Vector Databases Explained](https://www.pinecone.io/learn/vector-database/)

### Alternatives à explorer

- **Pinecone** : Base de données vectorielle cloud
- **Weaviate** : Base de données vectorielle open source
- **ChromaDB** : Alternative simple à FAISS
- **LlamaIndex** : Framework RAG simplifié

---

## 🤝 Contribution

Ce projet est à but pédagogique. N'hésite pas à :

- Expérimenter avec différents paramètres
- Ajouter de nouvelles fonctionnalités
- Tester d'autres modèles (Anthropic Claude, etc.)
- Comparer les performances

---

## 📝 Licence

Ce projet est libre d'utilisation à des fins éducatives.

**Note** : Respecte les conditions d'utilisation d'OpenAI et les licences des documents juridiques que tu utilises.

---

## 🎉 Bravo !

Tu as maintenant un assistant juridique RAG fonctionnel !

**Prochaines étapes suggérées :**

1. Teste avec différents types de documents
2. Expérimente avec les paramètres (chunk_size, k, temperature)
3. Ajoute une interface utilisateur avec Streamlit
4. Essaye d'autres modèles (Claude, Llama, Mistral)
5. Explore les bases de données vectorielles (Pinecone, Weaviate)

**Questions ?** Documente tes expériences et continue à apprendre ! 🚀
