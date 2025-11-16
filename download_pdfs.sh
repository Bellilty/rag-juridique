#!/bin/bash

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║       📥 Téléchargement des PDFs Juridiques                  ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

cd "$(dirname "$0")/data/pdfs"

# 1. Code Civil
echo "📄 1/5 - Téléchargement du Code Civil..."
curl -L -o "Code_Civil_Extraits.pdf" "https://www.courdecassation.fr/files/files/LA%20COUR/Plaquettes%20et%20brochures/extraits_code_civil.pdf" 2>/dev/null
echo "✅ Code Civil téléchargé"
echo ""

# 2. RGPD Officiel
echo "📄 2/5 - Téléchargement du RGPD..."
curl -L -o "RGPD_Officiel.pdf" "https://www.cnil.fr/sites/cnil/files/atoms/files/reglement_europeen_sur_la_protection_des_donnees_personnelles.pdf" 2>/dev/null
echo "✅ RGPD téléchargé"
echo ""

# 3. Loi Informatique et Libertés
echo "📄 3/5 - Téléchargement de la Loi Informatique et Libertés..."
curl -L -o "Loi_Informatique_Libertes.pdf" "https://www.cnil.fr/sites/cnil/files/atoms/files/loi_78-17_du_6_janvier_1978_modifiee.pdf" 2>/dev/null
echo "✅ Loi Informatique et Libertés téléchargée"
echo ""

# 4. Déclaration des Droits de l'Homme
echo "📄 4/5 - Téléchargement de la Déclaration des Droits de l'Homme..."
curl -L -o "Declaration_Droits_Homme.pdf" "https://www.un.org/fr/documents/udhr/UDHR_booklet_FR_web.pdf" 2>/dev/null
echo "✅ Déclaration téléchargée"
echo ""

# 5. Code de la Consommation
echo "📄 5/5 - Téléchargement du Code de la Consommation..."
curl -L -o "Code_Consommation.pdf" "https://www.economie.gouv.fr/files/files/directions_services/dgccrf/documentation/fiches_pratiques/fiches/code_consommation.pdf" 2>/dev/null
echo "✅ Code de la Consommation téléchargé"
echo ""

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║       ✅ Tous les PDFs ont été téléchargés !                 ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Liste les PDFs
echo "📁 PDFs dans le dossier :"
ls -lh *.pdf 2>/dev/null | awk '{print "   - " $9 " (" $5 ")"}'
echo ""

echo "🔨 Prochaine étape : Recrée l'index FAISS avec :"
echo "   cd ../.. && source venv/bin/activate && python -m src.embeddings"

