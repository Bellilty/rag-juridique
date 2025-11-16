# 📥 Liens pour télécharger des PDFs juridiques français

## 🇫🇷 Sources officielles

### 1. Code Civil
```bash
curl -L -o "data/pdfs/Code_Civil_Extraits.pdf" "https://www.courdecassation.fr/files/files/LA%20COUR/Plaquettes%20et%20brochures/extraits_code_civil.pdf"
```

### 2. Code Pénal (extraits)
```bash
curl -L -o "data/pdfs/Code_Penal_Sanctions.pdf" "https://www.justice.gouv.fr/sites/default/files/migrations/portail/art_pix/code_penal.pdf"
```

### 3. RGPD officiel français
```bash
curl -L -o "data/pdfs/RGPD_Officiel.pdf" "https://www.cnil.fr/sites/cnil/files/atoms/files/reglement_europeen_sur_la_protection_des_donnees_personnelles.pdf"
```

### 4. Code du Travail (INRS)
```bash
curl -L -o "data/pdfs/Code_Travail_Securite.pdf" "https://www.inrs.fr/publications/bdd/doc/ficheDoc.html?refINRS=ED%206109"
```

### 5. Droits de l'Homme (ONU)
```bash
curl -L -o "data/pdfs/Declaration_Droits_Homme.pdf" "https://www.un.org/fr/documents/udhr/UDHR_booklet_FR_web.pdf"
```

### 6. Charte de l'environnement
```bash
curl -L -o "data/pdfs/Charte_Environnement.pdf" "https://www.ecologie.gouv.fr/sites/default/files/Charte%20de%20l%27environnement.pdf"
```

### 7. Code de la Consommation
```bash
curl -L -o "data/pdfs/Code_Consommation.pdf" "https://www.economie.gouv.fr/files/files/directions_services/dgccrf/documentation/fiches_pratiques/fiches/code_consommation.pdf"
```

### 8. Loi Informatique et Libertés
```bash
curl -L -o "data/pdfs/Loi_Informatique_Libertes.pdf" "https://www.cnil.fr/sites/cnil/files/atoms/files/loi_78-17_du_6_janvier_1978_modifiee.pdf"
```

## 📋 Alternative : Sites pour télécharger manuellement

1. **Légifrance** : https://www.legifrance.gouv.fr/
2. **CNIL** : https://www.cnil.fr/
3. **Justice.gouv.fr** : https://www.justice.gouv.fr/
4. **EUR-Lex (UE)** : https://eur-lex.europa.eu/

## 🚀 Télécharger tous les PDFs d'un coup

Copie-colle dans ton terminal (dans le dossier du projet) :

```bash
cd /Users/simonbellilty/VSproject/rag-juridique

# Télécharge les PDFs
curl -L -o "data/pdfs/Code_Civil_Extraits.pdf" "https://www.courdecassation.fr/files/files/LA%20COUR/Plaquettes%20et%20brochures/extraits_code_civil.pdf"

curl -L -o "data/pdfs/RGPD_Officiel.pdf" "https://www.cnil.fr/sites/cnil/files/atoms/files/reglement_europeen_sur_la_protection_des_donnees_personnelles.pdf"

curl -L -o "data/pdfs/Loi_Informatique_Libertes.pdf" "https://www.cnil.fr/sites/cnil/files/atoms/files/loi_78-17_du_6_janvier_1978_modifiee.pdf"

echo "✅ PDFs téléchargés !"
```

Ensuite, recrée l'index :
```bash
source venv/bin/activate
python -m src.embeddings
```

