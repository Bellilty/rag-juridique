"""
Module d'extraction et de chunking des PDFs
============================================

Ce module gère :
1. L'extraction du texte depuis des fichiers PDF
2. Le nettoyage du texte (espaces, sauts de ligne, etc.)
3. Le découpage (chunking) en morceaux optimaux pour la recherche

Pourquoi le chunking ?
- Les LLMs ont une limite de tokens
- Les petits morceaux permettent une recherche plus précise
- L'overlap évite de couper des phrases importantes
"""

import fitz  # PyMuPDF
import re
import os
from typing import List, Dict


class PDFExtractor:
    """
    Classe pour extraire et traiter le texte des PDFs juridiques.
    """
    
    def __init__(self, pdf_directory: str = "data/pdfs"):
        """
        Initialise l'extracteur de PDF.
        
        Args:
            pdf_directory: Chemin vers le dossier contenant les PDFs
        """
        self.pdf_directory = pdf_directory
        
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extrait tout le texte d'un fichier PDF.
        
        Args:
            pdf_path: Chemin vers le fichier PDF
            
        Returns:
            Le texte complet extrait du PDF
        """
        print(f"📄 Extraction du PDF : {pdf_path}")
        
        # Ouvre le document PDF
        doc = fitz.open(pdf_path)
        text = ""
        
        # Parcourt chaque page
        for page_num, page in enumerate(doc, 1):
            # Extrait le texte de la page
            page_text = page.get_text("text")
            text += page_text
            
        doc.close()
        print(f"   ✅ {len(text)} caractères extraits")
        return text
    
    def clean_text(self, text: str) -> str:
        """
        Nettoie le texte extrait :
        - Supprime les espaces multiples
        - Normalise les sauts de ligne
        - Supprime les caractères spéciaux inutiles
        
        Args:
            text: Texte brut à nettoyer
            
        Returns:
            Texte nettoyé
        """
        # Remplace les multiples espaces par un seul
        text = re.sub(r'\s+', ' ', text)
        
        # Supprime les espaces en début et fin
        text = text.strip()
        
        # Remplace les doubles sauts de ligne par un seul
        text = re.sub(r'\n\n+', '\n\n', text)
        
        return text
    
    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[Dict[str, any]]:
        """
        Découpe le texte en morceaux (chunks) avec chevauchement.
        
        Pourquoi le chevauchement (overlap) ?
        - Évite de couper des informations importantes entre 2 chunks
        - Assure la continuité du contexte
        
        Args:
            text: Texte à découper
            chunk_size: Taille approximative de chaque chunk (en mots)
            overlap: Nombre de mots qui se chevauchent entre chunks
            
        Returns:
            Liste de dictionnaires contenant les chunks et leurs métadonnées
        """
        # Divise le texte en mots
        words = text.split()
        chunks = []
        
        # Crée les chunks avec chevauchement
        for i in range(0, len(words), chunk_size - overlap):
            chunk_words = words[i:i + chunk_size]
            chunk_text = " ".join(chunk_words)
            
            # Stocke le chunk avec ses métadonnées
            chunks.append({
                "text": chunk_text,
                "chunk_id": len(chunks),
                "start_word": i,
                "end_word": min(i + chunk_size, len(words))
            })
        
        print(f"🔪 Texte découpé en {len(chunks)} chunks")
        print(f"   📏 Taille moyenne : {sum(len(c['text']) for c in chunks) // len(chunks)} caractères")
        
        return chunks
    
    def extract_text_from_txt(self, txt_path: str) -> str:
        """
        Extrait le texte d'un fichier TXT.
        
        Args:
            txt_path: Chemin vers le fichier TXT
            
        Returns:
            Le texte du fichier
        """
        print(f"📄 Extraction du TXT : {txt_path}")
        
        with open(txt_path, 'r', encoding='utf-8') as f:
            text = f.read()
            
        print(f"   ✅ {len(text)} caractères extraits")
        return text
    
    def process_all_pdfs(self, chunk_size: int = 1000, overlap: int = 200) -> List[Dict[str, any]]:
        """
        Traite tous les PDFs et TXTs du dossier et retourne tous les chunks.
        
        Args:
            chunk_size: Taille des chunks en mots
            overlap: Chevauchement entre chunks
            
        Returns:
            Liste de tous les chunks de tous les fichiers
        """
        all_chunks = []
        
        # Vérifie si le dossier existe
        if not os.path.exists(self.pdf_directory):
            print(f"⚠️  Le dossier {self.pdf_directory} n'existe pas!")
            return all_chunks
        
        # Récupère tous les fichiers PDF et TXT
        pdf_files = [f for f in os.listdir(self.pdf_directory) if f.endswith('.pdf')]
        txt_files = [f for f in os.listdir(self.pdf_directory) if f.endswith('.txt')]
        all_files = pdf_files + txt_files
        
        if not all_files:
            print(f"⚠️  Aucun fichier PDF/TXT trouvé dans {self.pdf_directory}")
            return all_chunks
        
        print(f"\n📚 Traitement de {len(pdf_files)} PDF(s) et {len(txt_files)} TXT(s)...\n")
        
        # Traite chaque PDF
        for pdf_file in pdf_files:
            pdf_path = os.path.join(self.pdf_directory, pdf_file)
            
            # Extraction
            raw_text = self.extract_text_from_pdf(pdf_path)
            
            # Nettoyage
            clean_text = self.clean_text(raw_text)
            
            # Chunking
            chunks = self.chunk_text(clean_text, chunk_size, overlap)
            
            # Ajoute la source à chaque chunk
            for chunk in chunks:
                chunk["source"] = pdf_file
            
            all_chunks.extend(chunks)
            print()
        
        # Traite chaque TXT
        for txt_file in txt_files:
            txt_path = os.path.join(self.pdf_directory, txt_file)
            
            # Extraction
            raw_text = self.extract_text_from_txt(txt_path)
            
            # Nettoyage
            clean_text = self.clean_text(raw_text)
            
            # Chunking
            chunks = self.chunk_text(clean_text, chunk_size, overlap)
            
            # Ajoute la source à chaque chunk
            for chunk in chunks:
                chunk["source"] = txt_file
            
            all_chunks.extend(chunks)
            print()
        
        print(f"✅ Total : {len(all_chunks)} chunks créés depuis {len(all_files)} fichier(s)\n")
        
        return all_chunks


# Exemple d'utilisation si exécuté directement
if __name__ == "__main__":
    extractor = PDFExtractor()
    chunks = extractor.process_all_pdfs()
    
    # Affiche un exemple de chunk
    if chunks:
        print("📋 Exemple de chunk :")
        print(f"   Source : {chunks[0]['source']}")
        print(f"   ID : {chunks[0]['chunk_id']}")
        print(f"   Texte (100 premiers caractères) : {chunks[0]['text'][:100]}...")

