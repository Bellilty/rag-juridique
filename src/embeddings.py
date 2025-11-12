"""
Module d'embeddings et d'indexation FAISS
==========================================

Ce module gère :
1. La création d'embeddings vectoriels avec OpenAI
2. La construction de l'index FAISS pour la recherche rapide
3. La sauvegarde et le chargement de l'index

Qu'est-ce qu'un embedding ?
- C'est une représentation vectorielle (liste de nombres) d'un texte
- Les textes similaires ont des vecteurs proches
- Permet de faire de la recherche sémantique (par le sens, pas les mots exacts)

Qu'est-ce que FAISS ?
- Bibliothèque Facebook pour la recherche de vecteurs similaires
- Ultra-rapide, même avec des millions de vecteurs
- 100% local et gratuit !
"""

import os
import pickle
import numpy as np
import faiss
from openai import OpenAI
from typing import List, Dict
from dotenv import load_dotenv

# Charge les variables d'environnement depuis .env
load_dotenv()


class EmbeddingManager:
    """
    Classe pour gérer les embeddings OpenAI et l'indexation FAISS.
    """
    
    def __init__(self, api_key: str = None, model: str = "text-embedding-3-small"):
        """
        Initialise le gestionnaire d'embeddings.
        
        Args:
            api_key: Clé API OpenAI (si None, lit depuis .env)
            model: Modèle d'embedding à utiliser
                   text-embedding-3-small : le moins cher (~$0.02/1M tokens)
        """
        # Récupère la clé API
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("❌ Clé API OpenAI manquante! Crée un fichier .env avec OPENAI_API_KEY=...")
        
        # Initialise le client OpenAI
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        
        print(f"✅ Client OpenAI initialisé avec le modèle : {model}")
    
    def create_embedding(self, text: str) -> List[float]:
        """
        Crée un embedding pour un texte donné.
        
        Args:
            text: Le texte à vectoriser
            
        Returns:
            Liste de nombres représentant le vecteur
        """
        # Appel à l'API OpenAI
        response = self.client.embeddings.create(
            model=self.model,
            input=text
        )
        
        # Retourne le vecteur
        return response.data[0].embedding
    
    def create_embeddings_batch(self, texts: List[str], batch_size: int = 100) -> np.ndarray:
        """
        Crée des embeddings pour plusieurs textes en batch.
        
        Pourquoi en batch ?
        - Plus rapide que un par un
        - Réduit le nombre d'appels API
        - Économise de l'argent
        
        Args:
            texts: Liste de textes à vectoriser
            batch_size: Nombre de textes par batch
            
        Returns:
            Matrice numpy contenant tous les vecteurs
        """
        embeddings = []
        total = len(texts)
        
        print(f"\n🔢 Création de {total} embeddings par batch de {batch_size}...")
        
        # Traite par batch
        for i in range(0, total, batch_size):
            batch = texts[i:i + batch_size]
            
            # Appel API pour le batch
            response = self.client.embeddings.create(
                model=self.model,
                input=batch
            )
            
            # Extrait les vecteurs
            batch_embeddings = [item.embedding for item in response.data]
            embeddings.extend(batch_embeddings)
            
            # Affiche la progression
            progress = min(i + batch_size, total)
            print(f"   📊 Progression : {progress}/{total} ({100*progress//total}%)")
        
        # Convertit en numpy array (format attendu par FAISS)
        embeddings_array = np.array(embeddings).astype('float32')
        print(f"✅ Embeddings créés : shape = {embeddings_array.shape}\n")
        
        return embeddings_array
    
    def create_faiss_index(self, embeddings: np.ndarray) -> faiss.Index:
        """
        Crée un index FAISS pour la recherche rapide.
        
        Comment fonctionne FAISS ?
        - IndexFlatL2 : recherche exhaustive par distance euclidienne
        - Simple et précis (parfait pour < 1M de vecteurs)
        - Pour plus de vecteurs, on pourrait utiliser IndexIVF (clustering)
        
        Args:
            embeddings: Matrice des vecteurs (nombre_vecteurs x dimension)
            
        Returns:
            Index FAISS prêt à l'emploi
        """
        # Récupère la dimension des vecteurs
        dimension = embeddings.shape[1]
        
        print(f"🏗️  Création de l'index FAISS...")
        print(f"   Dimension des vecteurs : {dimension}")
        print(f"   Nombre de vecteurs : {embeddings.shape[0]}")
        
        # Crée l'index (IndexFlatL2 = recherche exacte par distance L2)
        index = faiss.IndexFlatL2(dimension)
        
        # Ajoute tous les vecteurs à l'index
        index.add(embeddings)
        
        print(f"✅ Index FAISS créé avec {index.ntotal} vecteurs\n")
        
        return index
    
    def save_index(self, index: faiss.Index, chunks: List[Dict], 
                   index_path: str = "index/legal.faiss", 
                   chunks_path: str = "index/chunks.pkl"):
        """
        Sauvegarde l'index FAISS et les chunks sur le disque.
        
        Pourquoi sauvegarder ?
        - Évite de recréer les embeddings à chaque fois (coûteux!)
        - Chargement instantané au démarrage de l'API
        
        Args:
            index: L'index FAISS à sauvegarder
            chunks: Les chunks de texte correspondants
            index_path: Chemin de sauvegarde de l'index
            chunks_path: Chemin de sauvegarde des chunks
        """
        # Crée le dossier si nécessaire
        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        
        # Sauvegarde l'index FAISS
        faiss.write_index(index, index_path)
        print(f"💾 Index FAISS sauvegardé : {index_path}")
        
        # Sauvegarde les chunks avec pickle
        with open(chunks_path, 'wb') as f:
            pickle.dump(chunks, f)
        print(f"💾 Chunks sauvegardés : {chunks_path}")
        
        # Calcule la taille
        index_size = os.path.getsize(index_path) / (1024 * 1024)  # En MB
        chunks_size = os.path.getsize(chunks_path) / (1024 * 1024)
        print(f"   📦 Taille totale : {index_size + chunks_size:.2f} MB\n")
    
    def load_index(self, index_path: str = "index/legal.faiss", 
                   chunks_path: str = "index/chunks.pkl"):
        """
        Charge l'index FAISS et les chunks depuis le disque.
        
        Args:
            index_path: Chemin de l'index FAISS
            chunks_path: Chemin des chunks
            
        Returns:
            Tuple (index FAISS, liste des chunks)
        """
        print(f"📂 Chargement de l'index existant...")
        
        # Charge l'index FAISS
        index = faiss.read_index(index_path)
        print(f"   ✅ Index chargé : {index.ntotal} vecteurs")
        
        # Charge les chunks
        with open(chunks_path, 'rb') as f:
            chunks = pickle.load(f)
        print(f"   ✅ Chunks chargés : {len(chunks)} chunks\n")
        
        return index, chunks
    
    def index_exists(self, index_path: str = "index/legal.faiss", 
                     chunks_path: str = "index/chunks.pkl") -> bool:
        """
        Vérifie si un index existe déjà.
        
        Returns:
            True si l'index existe, False sinon
        """
        return os.path.exists(index_path) and os.path.exists(chunks_path)


# Exemple d'utilisation si exécuté directement
if __name__ == "__main__":
    from src.extract_pdf import PDFExtractor
    
    print("=== Test du module d'embeddings ===\n")
    
    # 1. Extrait les PDFs
    extractor = PDFExtractor()
    chunks = extractor.process_all_pdfs()
    
    if not chunks:
        print("⚠️  Aucun chunk à traiter. Ajoute des PDFs dans data/pdfs/")
        exit(1)
    
    # 2. Crée les embeddings
    manager = EmbeddingManager()
    texts = [chunk["text"] for chunk in chunks]
    embeddings = manager.create_embeddings_batch(texts)
    
    # 3. Crée l'index FAISS
    index = manager.create_faiss_index(embeddings)
    
    # 4. Sauvegarde
    manager.save_index(index, chunks)
    
    print("✅ Indexation terminée avec succès!")

