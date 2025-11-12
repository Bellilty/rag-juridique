"""
Script d'initialisation du projet RAG Juridique
================================================

Ce script aide à :
1. Installer les dépendances
2. Télécharger des PDFs de démonstration (optionnel)
3. Créer l'index FAISS
4. Vérifier que tout fonctionne

Usage :
    python setup.py
"""

import os
import sys
import subprocess
import requests
from pathlib import Path


def print_header(text):
    """Affiche un en-tête formaté."""
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80 + "\n")


def check_venv():
    """Vérifie si on est dans l'environnement virtuel."""
    if sys.prefix == sys.base_prefix:
        print("⚠️  Tu n'es pas dans l'environnement virtuel!")
        print("\n💡 Active-le avec :")
        print("   source venv/bin/activate  (Linux/Mac)")
        print("   .\\venv\\Scripts\\activate  (Windows)")
        return False
    return True


def install_dependencies():
    """Installe les dépendances."""
    print_header("📦 Installation des dépendances")
    
    if not os.path.exists("requirements.txt"):
        print("❌ Fichier requirements.txt non trouvé!")
        return False
    
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
            check=True
        )
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            check=True
        )
        print("✅ Dépendances installées avec succès!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'installation : {e}")
        return False


def setup_env_file():
    """Configure le fichier .env avec la clé API."""
    print_header("🔑 Configuration de la clé API OpenAI")
    
    if os.path.exists(".env"):
        print("✅ Fichier .env existe déjà")
        with open(".env", "r") as f:
            content = f.read()
            if "OPENAI_API_KEY" in content and "sk-" in content:
                print("   Clé API déjà configurée!")
                return True
    
    print("\n📝 Pour utiliser ce projet, tu as besoin d'une clé API OpenAI")
    print("   1. Va sur https://platform.openai.com/api-keys")
    print("   2. Crée une clé API")
    print("   3. Entre-la ci-dessous (ou appuie sur Entrée pour le faire plus tard)\n")
    
    api_key = input("Clé API OpenAI (commence par 'sk-') : ").strip()
    
    if api_key:
        with open(".env", "w") as f:
            f.write(f"# Configuration de l'API OpenAI\n")
            f.write(f"OPENAI_API_KEY={api_key}\n")
        print("✅ Clé API sauvegardée dans .env")
        return True
    else:
        print("⚠️  Clé API non configurée. Tu peux le faire plus tard en créant un fichier .env")
        return False


def download_sample_pdf(url, filename):
    """Télécharge un PDF de démonstration."""
    output_path = os.path.join("data", "pdfs", filename)
    
    if os.path.exists(output_path):
        print(f"   ✅ {filename} existe déjà")
        return True
    
    try:
        print(f"   📥 Téléchargement de {filename}...")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        with open(output_path, "wb") as f:
            f.write(response.content)
        
        print(f"   ✅ {filename} téléchargé ({len(response.content) // 1024} KB)")
        return True
    except Exception as e:
        print(f"   ⚠️  Erreur : {e}")
        return False


def setup_sample_data():
    """Configure des données de démonstration."""
    print_header("📚 Configuration des données de démonstration")
    
    # Crée le dossier si nécessaire
    os.makedirs("data/pdfs", exist_ok=True)
    
    # Vérifie s'il y a déjà des PDFs
    existing_pdfs = [f for f in os.listdir("data/pdfs") if f.endswith(".pdf")]
    if existing_pdfs:
        print(f"✅ {len(existing_pdfs)} PDF(s) déjà présent(s) :")
        for pdf in existing_pdfs:
            print(f"   - {pdf}")
        return True
    
    print("\n💡 Options pour les données de démonstration :")
    print("   1. Télécharger automatiquement des PDFs publics (GDPR)")
    print("   2. Ajouter manuellement tes propres PDFs dans data/pdfs/")
    print("   3. Passer cette étape (tu pourras le faire plus tard)")
    
    choice = input("\nTon choix (1/2/3) : ").strip()
    
    if choice == "1":
        # URL d'exemple - GDPR en version texte simple
        sample_urls = {
            "GDPR_Info.pdf": "https://gdpr-info.eu/",  # Note: ce lien retourne du HTML, pas un PDF
        }
        
        print("\n⚠️  Note : Pour cette démo, ajoute manuellement un PDF juridique dans data/pdfs/")
        print("    Suggestions :")
        print("    - GDPR : https://gdpr-info.eu/ (sauvegarde la page en PDF)")
        print("    - Constitution US : https://www.archives.gov/founding-docs (PDF disponible)")
        print("    - Code civil français : https://www.legifrance.gouv.fr/")
        
        return False
    
    elif choice == "2":
        print("\n📁 Ajoute tes PDFs dans le dossier : data/pdfs/")
        print("   Puis relance ce script ou lance directement :")
        print("   python src/embeddings.py")
        return False
    
    else:
        print("\n⏭️  Étape ignorée. Tu pourras ajouter des PDFs plus tard.")
        return False


def create_index():
    """Crée l'index FAISS."""
    print_header("🏗️  Création de l'index FAISS")
    
    # Vérifie s'il y a des PDFs
    if not os.path.exists("data/pdfs"):
        print("⚠️  Dossier data/pdfs/ non trouvé")
        return False
    
    pdf_files = [f for f in os.listdir("data/pdfs") if f.endswith(".pdf")]
    if not pdf_files:
        print("⚠️  Aucun PDF trouvé dans data/pdfs/")
        print("   Ajoute des PDFs juridiques puis lance :")
        print("   python src/embeddings.py")
        return False
    
    # Vérifie la clé API
    if not os.path.exists(".env"):
        print("⚠️  Fichier .env manquant. Configure ta clé API d'abord!")
        return False
    
    print(f"📄 {len(pdf_files)} PDF(s) trouvé(s)")
    print("\n⚙️  Lancement de la création de l'index...")
    print("   (Cela peut prendre quelques minutes selon la taille des documents)\n")
    
    try:
        # Lance le script d'embeddings
        result = subprocess.run(
            [sys.executable, "-m", "src.embeddings"],
            check=True,
            capture_output=False
        )
        
        print("\n✅ Index FAISS créé avec succès!")
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erreur lors de la création de l'index : {e}")
        print("\n💡 Tu peux le créer manuellement avec :")
        print("   python src/embeddings.py")
        return False


def test_api():
    """Teste l'API."""
    print_header("🧪 Test de l'API")
    
    # Vérifie si l'index existe
    if not os.path.exists("index/legal.faiss"):
        print("⚠️  Index non trouvé. L'API ne pourra pas démarrer.")
        print("   Crée l'index d'abord avec : python src/embeddings.py")
        return False
    
    print("✅ Tous les fichiers nécessaires sont présents!")
    print("\n🚀 Tu peux maintenant lancer l'API avec :")
    print("   uvicorn src.api:app --reload")
    print("\n📖 Puis ouvre la documentation :")
    print("   http://localhost:8000/docs")
    
    return True


def main():
    """Fonction principale."""
    print("\n" + "🎨"*40)
    print("  ASSISTANT JURIDIQUE RAG - SETUP")
    print("🎨"*40)
    
    # 1. Vérifie l'environnement virtuel
    if not check_venv():
        print("\n❌ Active l'environnement virtuel d'abord!")
        return
    
    # 2. Installe les dépendances
    if not install_dependencies():
        print("\n❌ Impossible d'installer les dépendances")
        return
    
    # 3. Configure la clé API
    api_configured = setup_env_file()
    
    # 4. Configure les données
    data_ready = setup_sample_data()
    
    # 5. Crée l'index (si les données sont prêtes et l'API configurée)
    if api_configured and data_ready:
        index_created = create_index()
    else:
        index_created = False
        print("\n⚠️  Index non créé. Complète les étapes précédentes puis lance :")
        print("   python src/embeddings.py")
    
    # 6. Informations finales
    print_header("✅ Setup terminé!")
    
    print("📋 Prochaines étapes :\n")
    
    if not api_configured:
        print("   1. Configure ta clé API OpenAI dans le fichier .env")
    
    if not data_ready:
        print("   2. Ajoute des PDFs juridiques dans data/pdfs/")
    
    if not index_created:
        print("   3. Crée l'index FAISS : python src/embeddings.py")
    
    print("   4. Lance l'API : uvicorn src.api:app --reload")
    print("   5. Ouvre la doc : http://localhost:8000/docs")
    
    print("\n💡 Exemple de requête :")
    print('   http://localhost:8000/ask?query=What+is+GDPR')
    
    print("\n🎉 Bon apprentissage du RAG!\n")


if __name__ == "__main__":
    main()

