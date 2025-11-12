"""
Module de recherche et génération RAG
======================================

Ce module gère :
1. La recherche de chunks pertinents avec FAISS
2. La génération de réponses avec OpenAI (RAG)
3. L'intégration du contexte récupéré dans le prompt

Qu'est-ce que le RAG (Retrieval-Augmented Generation) ?
- Retrieval : On cherche les passages pertinents dans nos documents
- Augmented : On enrichit le prompt du LLM avec ces passages
- Generation : Le LLM génère une réponse basée sur ce contexte

Avantages du RAG :
- Le LLM répond avec VOS données (pas ses connaissances générales)
- Réduit les hallucinations
- Permet de citer les sources
"""

import numpy as np
import faiss
from openai import OpenAI
from typing import List, Dict, Tuple
import os
from dotenv import load_dotenv

load_dotenv()


class RAGRetriever:
    """
    Classe pour la recherche et la génération avec RAG.
    """
    
    def __init__(self, index: faiss.Index, chunks: List[Dict], api_key: str = None):
        """
        Initialise le retriever RAG.
        
        Args:
            index: Index FAISS chargé
            chunks: Liste des chunks de texte
            api_key: Clé API OpenAI
        """
        self.index = index
        self.chunks = chunks
        
        # Initialise le client OpenAI
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("❌ Clé API OpenAI manquante!")
        
        self.client = OpenAI(api_key=api_key)
        
        print(f"✅ RAG Retriever initialisé")
        print(f"   📚 {len(chunks)} chunks disponibles")
        print(f"   🔍 Index avec {index.ntotal} vecteurs\n")
    
    def create_query_embedding(self, query: str, model: str = "text-embedding-3-small") -> np.ndarray:
        """
        Crée l'embedding de la question de l'utilisateur.
        
        Args:
            query: La question posée
            model: Modèle d'embedding (doit être le même que pour l'index!)
            
        Returns:
            Vecteur numpy de la question
        """
        response = self.client.embeddings.create(
            model=model,
            input=query
        )
        
        # Convertit en numpy array
        embedding = np.array([response.data[0].embedding]).astype('float32')
        return embedding
    
    def search(self, query: str, k: int = 3) -> List[Dict]:
        """
        Recherche les k chunks les plus pertinents pour la question.
        
        Comment ça marche ?
        1. On vectorise la question
        2. FAISS trouve les k vecteurs les plus proches dans l'index
        3. On récupère les chunks correspondants
        
        Args:
            query: La question de l'utilisateur
            k: Nombre de chunks à retourner
            
        Returns:
            Liste des k chunks les plus pertinents avec leurs scores
        """
        print(f"🔍 Recherche pour : '{query}'")
        
        # Crée l'embedding de la question
        query_embedding = self.create_query_embedding(query)
        
        # Recherche dans FAISS
        # D = distances (plus petit = plus proche)
        # I = indices des chunks dans notre liste
        distances, indices = self.index.search(query_embedding, k)
        
        # Prépare les résultats
        results = []
        for i, (idx, distance) in enumerate(zip(indices[0], distances[0])):
            chunk = self.chunks[idx].copy()
            chunk['distance'] = float(distance)
            chunk['rank'] = i + 1
            results.append(chunk)
            
            print(f"   {i+1}. [Distance: {distance:.2f}] {chunk['source']} - Chunk {chunk['chunk_id']}")
        
        print()
        return results
    
    def generate_answer(self, query: str, context_chunks: List[Dict], 
                       model: str = "gpt-4o-mini", max_tokens: int = 500) -> Dict:
        """
        Génère une réponse en utilisant le RAG.
        
        Processus :
        1. On récupère les chunks pertinents (déjà fait avec search())
        2. On construit un prompt avec le contexte
        3. On demande au LLM de répondre UNIQUEMENT basé sur ce contexte
        4. Le LLM génère une réponse avec citations
        
        Args:
            query: Question de l'utilisateur
            context_chunks: Chunks pertinents trouvés
            model: Modèle OpenAI à utiliser
                   gpt-4o-mini : le meilleur rapport qualité/prix (~$0.15/1M tokens output)
                   gpt-3.5-turbo : encore moins cher mais moins bon
            max_tokens: Nombre max de tokens dans la réponse
            
        Returns:
            Dictionnaire avec la réponse et les métadonnées
        """
        # Construit le contexte à partir des chunks
        context = ""
        for i, chunk in enumerate(context_chunks, 1):
            context += f"[Extrait {i} - Source: {chunk['source']}]\n"
            context += chunk['text']
            context += "\n\n"
        
        # Construit le prompt pour le LLM
        # C'est ici qu'on "programme" le comportement du LLM
        system_prompt = """Tu es un assistant juridique expert.
Réponds UNIQUEMENT en te basant sur les extraits de documents fournis.
Si la réponse n'est pas dans les extraits, dis clairement "Je ne trouve pas cette information dans les documents fournis."
Cite toujours la source (ex: [Source: GDPR.pdf]).
Sois précis et professionnel."""

        user_prompt = f"""Contexte (extraits de documents juridiques) :

{context}

Question : {query}

Réponds de manière claire et cite tes sources."""

        print(f"🤖 Génération de la réponse avec {model}...")
        
        # Appel à l'API OpenAI
        completion = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.3  # Température basse = réponses plus déterministes et factuelles
        )
        
        # Extrait la réponse
        answer = completion.choices[0].message.content
        
        # Prépare le résultat avec métadonnées
        result = {
            "query": query,
            "answer": answer,
            "sources": [chunk['source'] for chunk in context_chunks],
            "num_chunks_used": len(context_chunks),
            "model": model,
            "tokens_used": {
                "prompt": completion.usage.prompt_tokens,
                "completion": completion.usage.completion_tokens,
                "total": completion.usage.total_tokens
            }
        }
        
        print(f"✅ Réponse générée ({result['tokens_used']['total']} tokens utilisés)\n")
        
        return result
    
    def ask(self, query: str, k: int = 3, model: str = "gpt-4o-mini") -> Dict:
        """
        Méthode principale : pose une question et obtient une réponse RAG.
        
        C'est la méthode "tout-en-un" qui :
        1. Cherche les chunks pertinents
        2. Génère la réponse
        
        Args:
            query: Question de l'utilisateur
            k: Nombre de chunks à utiliser comme contexte
            model: Modèle OpenAI pour la génération
            
        Returns:
            Dictionnaire avec la réponse complète
        """
        # 1. Recherche les chunks pertinents
        relevant_chunks = self.search(query, k=k)
        
        # 2. Génère la réponse
        result = self.generate_answer(query, relevant_chunks, model=model)
        
        return result


# Fonction utilitaire pour calculer le coût approximatif
def estimate_cost(tokens_used: Dict, model: str = "gpt-4o-mini") -> Dict:
    """
    Estime le coût d'une requête RAG.
    
    Prix approximatifs (novembre 2024) :
    - gpt-4o-mini : $0.15/1M input tokens, $0.60/1M output tokens
    - gpt-3.5-turbo : $0.50/1M input, $1.50/1M output
    - text-embedding-3-small : $0.02/1M tokens
    
    Args:
        tokens_used: Dict avec 'prompt' et 'completion'
        model: Modèle utilisé
        
    Returns:
        Dict avec le coût estimé
    """
    # Prix par 1M de tokens
    prices = {
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
        "gpt-4": {"input": 30.00, "output": 60.00}
    }
    
    if model not in prices:
        model = "gpt-4o-mini"  # Par défaut
    
    # Calcule le coût
    input_cost = (tokens_used["prompt"] / 1_000_000) * prices[model]["input"]
    output_cost = (tokens_used["completion"] / 1_000_000) * prices[model]["output"]
    total_cost = input_cost + output_cost
    
    return {
        "input_cost_usd": round(input_cost, 6),
        "output_cost_usd": round(output_cost, 6),
        "total_cost_usd": round(total_cost, 6),
        "model": model
    }


# Exemple d'utilisation si exécuté directement
if __name__ == "__main__":
    from embeddings import EmbeddingManager
    
    print("=== Test du module de retrieval ===\n")
    
    # Charge l'index existant
    manager = EmbeddingManager()
    
    if not manager.index_exists():
        print("❌ Aucun index trouvé. Lance d'abord embeddings.py pour créer l'index.")
        exit(1)
    
    index, chunks = manager.load_index()
    
    # Crée le retriever
    retriever = RAGRetriever(index, chunks)
    
    # Pose une question test
    test_query = "What are the main principles of data protection?"
    result = retriever.ask(test_query, k=3)
    
    # Affiche les résultats
    print("=" * 80)
    print(f"❓ Question : {result['query']}")
    print("=" * 80)
    print(f"\n💬 Réponse :\n{result['answer']}\n")
    print("=" * 80)
    print(f"📚 Sources : {', '.join(set(result['sources']))}")
    print(f"🔢 Tokens utilisés : {result['tokens_used']['total']}")
    
    # Estime le coût
    cost = estimate_cost(result['tokens_used'], result['model'])
    print(f"💰 Coût estimé : ${cost['total_cost_usd']} USD")
    print("=" * 80)

