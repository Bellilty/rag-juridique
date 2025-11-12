# 🤖 Assistant Juridique RAG

Assistant juridique intelligent utilisant RAG (Retrieval-Augmented Generation) pour répondre aux questions sur des documents juridiques français.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![Gradio](https://img.shields.io/badge/Gradio-UI-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🎯 Fonctionnalités

- ✅ **RAG (Retrieval-Augmented Generation)** avec OpenAI GPT-4o-mini
- ✅ **Recherche vectorielle** ultra-rapide avec FAISS
- ✅ **API REST** moderne avec FastAPI
- ✅ **Interface graphique** intuitive avec Gradio
- ✅ **Citations des sources** pour chaque réponse
- ✅ **Coûts minimaux** (~$0.0006 par question)
- ✅ **100% local** (sauf appels API OpenAI)

## 🚀 Démarrage Rapide

### 1️⃣ Installation

```bash
# Clone le projet
git clone https://github.com/TON-USERNAME/rag-juridique.git
cd rag-juridique

# Crée l'environnement virtuel
python3.11 -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installe les dépendances
pip install -r requirements.txt
```

### 2️⃣ Configuration

```bash
# Crée le fichier .env avec ta clé API OpenAI
echo "OPENAI_API_KEY=sk-ta-clé-ici" > .env
```

### 3️⃣ Ajoute des documents PDF

Place tes documents juridiques dans `data/pdfs/`:
- Constitution française
- Code civil
- RGPD
- Etc.

### 4️⃣ Crée l'index FAISS

```bash
python -m src.embeddings
```

### 5️⃣ Lance l'application

**Option A - Interface Gradio (recommandée) :**
```bash
python ui.py
```
Puis ouvre http://localhost:7860

**Option B - API FastAPI :**
```bash
uvicorn src.api:app --reload
```
Puis ouvre http://localhost:8000/docs

## 📸 Captures d'écran

### Interface Gradio
Interface utilisateur moderne et intuitive pour poser des questions.

### API FastAPI
Documentation interactive Swagger pour intégration facile.

## 🏗️ Architecture

```
RAG Pipeline:
PDF → Chunking → Embeddings (OpenAI) → FAISS Index → Retrieval → LLM (GPT-4o-mini) → Réponse
```

## 📁 Structure du Projet

```
rag-juridique/
├── src/
│   ├── extract_pdf.py    # Extraction et chunking des PDFs
│   ├── embeddings.py     # Création des embeddings et index FAISS
│   ├── retrieval.py      # Recherche et génération RAG
│   └── api.py            # API FastAPI
├── data/
│   └── pdfs/             # Dossier pour tes documents PDF
├── index/                # Index FAISS (généré)
├── ui.py                 # Interface Gradio
├── requirements.txt      # Dépendances Python
└── README.md            # Documentation
```

## 🛠️ Technologies

- **Python 3.11**
- **FastAPI** - API REST moderne
- **Gradio** - Interface utilisateur
- **OpenAI API** - Embeddings (text-embedding-3-small) + LLM (gpt-4o-mini)
- **FAISS** - Recherche vectorielle ultra-rapide
- **PyMuPDF** - Extraction de texte des PDFs

## 💰 Coûts

### Modèles utilisés (les moins chers) :
- **text-embedding-3-small** : $0.02 / 1M tokens
- **gpt-4o-mini** : $0.15 / 1M tokens (input), $0.60 / 1M tokens (output)

### Estimation :
- Setup initial (3 PDFs ~150 pages) : ~$0.001
- Par question : ~$0.0005
- 100 questions : ~$0.05 (5 centimes !)

## 📖 Documentation Complète

Consulte les guides dans le projet :
- `QUICKSTART.md` - Guide de démarrage rapide (10 min)
- `README.md` - Documentation complète
- `CONCEPTS.md` - Explications détaillées du RAG
- `COMMANDES.md` - Aide-mémoire des commandes

## 🧪 Exemples de Questions

```
- Qu'est-ce que la Constitution française ?
- Quels sont les pouvoirs du Président de la République ?
- Qu'est-ce que le droit du travail ?
- Quelle est la devise de la République française ?
- Comment est organisé le Parlement français ?
```

## 🔧 Commandes Utiles

```bash
# Créer l'index
python -m src.embeddings

# Lancer l'API
uvicorn src.api:app --reload

# Lancer l'interface Gradio
python ui.py

# Tester l'API
curl "http://localhost:8000/ask?query=Qu'est-ce+que+la+Constitution"

# Voir les statistiques
curl http://localhost:8000/stats
```

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésite pas à :
- Signaler des bugs
- Proposer des améliorations
- Ajouter de nouvelles fonctionnalités

## 📝 License

MIT License - Utilise librement pour tes projets personnels et éducatifs.

## ⚠️ Disclaimers

- Cet assistant est à but éducatif et de démonstration
- Toujours vérifier les informations juridiques avec des sources officielles
- Respecte les conditions d'utilisation d'OpenAI
- Les réponses sont limitées aux documents indexés

## 🎓 Apprentissage

Ce projet est parfait pour apprendre :
- Le RAG (Retrieval-Augmented Generation)
- Les embeddings vectoriels
- La recherche de similarité avec FAISS
- Les APIs REST avec FastAPI
- L'interface utilisateur avec Gradio
- Le traitement de documents PDF

## 🙏 Crédits

Développé avec ❤️ pour apprendre le RAG et FastAPI.

Technologies utilisées :
- OpenAI pour les embeddings et LLM
- Facebook AI pour FAISS
- Gradio pour l'interface
- FastAPI pour l'API

## 📞 Support

Pour toute question ou problème, consulte la documentation ou ouvre une issue.

---

**Fait avec 🤖 et ⚖️ pour rendre le droit accessible**

