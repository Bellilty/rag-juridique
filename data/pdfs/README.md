# 📄 Dossier des PDFs

Place ici les documents juridiques que tu veux interroger.

## 📚 Sources recommandées (gratuites et publiques)

### 🇪🇺 Union Européenne

**GDPR (Règlement Général sur la Protection des Données)**

- Site officiel : https://gdpr-info.eu/
- Téléchargement : Sauvegarde la page en PDF ou utilise un convertisseur
- Taille : ~50 pages
- Langue : Anglais (version FR sur EUR-Lex)

### 🇺🇸 États-Unis

**U.S. Constitution**

- Site officiel : https://www.archives.gov/founding-docs/constitution
- Format : PDF disponible directement
- Taille : ~20 pages
- Langue : Anglais

**Bill of Rights**

- Site : https://www.archives.gov/founding-docs/bill-of-rights
- Taille : ~10 pages
- Langue : Anglais

### 🇫🇷 France

**Code civil français**

- Site : https://www.legifrance.gouv.fr/codes/id/LEGITEXT000006070721/
- Format : Téléchargeable en PDF
- Taille : ~2800 articles (gros fichier!)
- Conseil : Télécharge seulement une section (ex: Livre III sur les biens)

**Déclaration des Droits de l'Homme et du Citoyen**

- Site : https://www.conseil-constitutionnel.fr/
- Taille : 2 pages
- Langue : Français

## 🎯 Pour commencer

**Recommandation pour débuter :**

1. **Télécharge le GDPR** (simple et complet)

   - Va sur https://gdpr-info.eu/
   - Imprime en PDF ou utilise : https://gdpr-info.eu/gdpr.pdf (si disponible)

2. **Ajoute un document court** (U.S. Constitution)
   - Parfait pour tester rapidement

## 📝 Comment ajouter un PDF

1. Télécharge ton document juridique
2. Place-le dans ce dossier (`data/pdfs/`)
3. Lance la création de l'index :
   ```bash
   python -m src.embeddings
   ```

## ⚠️ Notes importantes

- **Formats supportés** : Uniquement PDF pour l'instant
- **Taille recommandée** : 1-100 pages par document
- **Nombre de fichiers** : Commence avec 2-3 documents pour limiter les coûts
- **Qualité** : Privilégie les PDFs avec du texte (pas des scans d'images)

## 💰 Estimation des coûts

| Nombre de PDFs | Pages totales | Coût embeddings | Temps de traitement |
| -------------- | ------------- | --------------- | ------------------- |
| 1-2 PDFs       | ~50 pages     | ~$0.001         | 1-2 minutes         |
| 3-5 PDFs       | ~150 pages    | ~$0.003         | 3-5 minutes         |
| 10 PDFs        | ~500 pages    | ~$0.01          | 10-15 minutes       |

## 🔍 Vérifier tes PDFs

```bash
# Liste les PDFs présents
ls -lh *.pdf

# Compte le nombre de PDFs
ls *.pdf | wc -l
```

## 🚀 Prêt ?

Une fois tes PDFs ajoutés, lance :

```bash
python -m src.embeddings
```

Puis démarre l'API :

```bash
uvicorn src.api:app --reload
```

Bon apprentissage du RAG ! 🎉
