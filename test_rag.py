"""
Script de test rapide du système RAG
=====================================

Ce script permet de tester rapidement le RAG sans passer par l'API.
Utile pour déboguer ou expérimenter.

Usage :
    python test_rag.py
"""

import os
import sys
from dotenv import load_dotenv

# Charge les variables d'environnement
load_dotenv()

# Vérifie que la clé API existe
if not os.getenv("OPENAI_API_KEY"):
    print("❌ Erreur : Variable OPENAI_API_KEY manquante dans .env")
    sys.exit(1)

# Import des modules
try:
    from src.embeddings import EmbeddingManager
    from src.retrieval import RAGRetriever, estimate_cost
except ImportError as e:
    print(f"❌ Erreur d'import : {e}")
    print("Assure-toi d'avoir installé les dépendances :")
    print("   pip install -r requirements.txt")
    sys.exit(1)


def main():
    """Fonction principale de test."""
    
    print("\n" + "="*80)
    print("  🧪 TEST DU SYSTÈME RAG")
    print("="*80 + "\n")
    
    # 1. Vérifie que l'index existe
    manager = EmbeddingManager()
    
    if not manager.index_exists():
        print("❌ Index FAISS non trouvé!")
        print("\n💡 Crée l'index avec :")
        print("   python -m src.embeddings")
        print("\n   Ou ajoute des PDFs dans data/pdfs/ puis relance.")
        return
    
    # 2. Charge l'index
    print("📂 Chargement de l'index...")
    index, chunks = manager.load_index()
    
    # 3. Initialise le retriever
    retriever = RAGRetriever(index, chunks)
    
    # 4. Questions de test
    test_questions = [
        "What is the purpose of GDPR?",
        "What are personal data?",
        "Who is a data controller?",
    ]
    
    print("📝 Questions de test disponibles :")
    for i, q in enumerate(test_questions, 1):
        print(f"   {i}. {q}")
    
    print("\n💡 Tu peux aussi poser ta propre question!\n")
    
    # 5. Permet à l'utilisateur de choisir
    choice = input("Choisis un numéro (1-3) ou tape ta question : ").strip()
    
    # Détermine la question
    if choice.isdigit() and 1 <= int(choice) <= len(test_questions):
        query = test_questions[int(choice) - 1]
    else:
        query = choice
    
    if not query:
        print("⚠️  Aucune question fournie.")
        return
    
    # 6. Pose la question
    print("\n" + "="*80)
    print(f"❓ Question : {query}")
    print("="*80 + "\n")
    
    print("🔍 Recherche en cours...")
    result = retriever.ask(query, k=3, model="gpt-4o-mini")
    
    # 7. Affiche les résultats
    print("\n" + "="*80)
    print("💬 RÉPONSE")
    print("="*80 + "\n")
    print(result['answer'])
    
    print("\n" + "="*80)
    print("📊 MÉTADONNÉES")
    print("="*80)
    print(f"\n📚 Sources utilisées :")
    for source in set(result['sources']):
        print(f"   - {source}")
    
    print(f"\n🔢 Chunks utilisés : {result['num_chunks_used']}")
    print(f"🤖 Modèle : {result['model']}")
    print(f"📝 Tokens utilisés : {result['tokens_used']['total']}")
    print(f"   - Input : {result['tokens_used']['prompt']}")
    print(f"   - Output : {result['tokens_used']['completion']}")
    
    # Calcule le coût
    cost = estimate_cost(result['tokens_used'], result['model'])
    print(f"\n💰 Coût estimé : ${cost['total_cost_usd']:.6f} USD")
    
    print("\n" + "="*80 + "\n")
    
    # 8. Propose de continuer
    while True:
        continue_choice = input("Poser une autre question ? (o/n) : ").strip().lower()
        
        if continue_choice in ['n', 'non', 'no']:
            print("\n👋 Au revoir!\n")
            break
        elif continue_choice in ['o', 'oui', 'y', 'yes']:
            next_query = input("\n❓ Ta question : ").strip()
            if next_query:
                print("\n🔍 Recherche en cours...\n")
                result = retriever.ask(next_query, k=3, model="gpt-4o-mini")
                
                print("="*80)
                print("💬 RÉPONSE")
                print("="*80 + "\n")
                print(result['answer'])
                
                cost = estimate_cost(result['tokens_used'], result['model'])
                print(f"\n💰 Coût : ${cost['total_cost_usd']:.6f} USD\n")
        else:
            print("⚠️  Réponse non reconnue. Tape 'o' ou 'n'")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interruption. Au revoir!\n")
    except Exception as e:
        print(f"\n❌ Erreur : {e}\n")
        import traceback
        traceback.print_exc()

