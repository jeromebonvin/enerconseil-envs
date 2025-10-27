# 🚀 GUIDE DE DÉPLOIEMENT STREAMLIT

## 📋 Vue d'ensemble

Votre application Streamlit permet à vos collègues de :
- 📤 Uploader des PDF EN-VS
- 🏛️ Choisir la commune destinataire (7 communes)
- 👤 Sélectionner le signataire (5 utilisateurs)
- 🤖 Extraire les données automatiquement
- 📄 Générer un rapport Word professionnel
- 🔴 Visualiser les alertes de non-conformité

---

## 🆓 OPTION 1 : STREAMLIT COMMUNITY CLOUD (Recommandé)

### ✅ Avantages
- **Gratuit** pour toujours
- Hébergement inclus
- HTTPS automatique
- Accessible mondialement
- Mises à jour automatiques

### 📝 Étapes de déploiement

#### 1. Créer un compte GitHub (si nécessaire)
1. Allez sur https://github.com
2. Créez un compte gratuit
3. Confirmez votre email

#### 2. Créer un dépôt GitHub
1. Cliquez sur "New repository"
2. Nom : `enerconseil-envs` (ou votre choix)
3. Cochez "Public" (nécessaire pour version gratuite)
4. Cliquez "Create repository"

#### 3. Uploader les fichiers
Uploadez ces fichiers dans votre dépôt :
```
enerconseil-envs/
├── app_streamlit.py          # Application principale
├── export_word.py             # Génération Word
├── extract.py                 # Extraction PDF
├── utils.py                   # Utilitaires
├── requirements.txt           # Dépendances
├── .streamlit/
│   └── config.toml           # Configuration
└── README.md                  # Documentation (optionnel)
```

**Comment uploader :**
- Option A : Glisser-déposer les fichiers sur GitHub.com
- Option B : Utiliser GitHub Desktop
- Option C : Ligne de commande Git

#### 4. Créer un compte Streamlit Cloud
1. Allez sur https://share.streamlit.io
2. Connectez-vous avec votre compte GitHub
3. Autorisez l'accès à vos dépôts

#### 5. Déployer l'application
1. Cliquez sur "New app"
2. Sélectionnez votre dépôt : `enerconseil-envs`
3. Fichier principal : `app_streamlit.py`
4. Cliquez "Deploy!"

#### 6. Configurer la clé API Claude
1. Dans Streamlit Cloud, allez dans "Settings" > "Secrets"
2. Ajoutez :
```toml
CLAUDE_API_KEY = "votre-clé-api-claude-ici"
```
3. Sauvegardez

#### 7. C'est prêt ! 🎉
Votre application est accessible à l'URL :
```
https://enerconseil-envs.streamlit.app
```

---

## 💻 OPTION 2 : DÉPLOIEMENT LOCAL (Pour tests)

### Installation

```bash
# 1. Installer Python 3.9+
# Téléchargez depuis https://python.org

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Configurer la clé API
# Créez un fichier .env :
echo "CLAUDE_API_KEY=votre-clé-api" > .env

# 4. Lancer l'application
streamlit run app_streamlit.py
```

### Accès
L'application s'ouvre automatiquement sur :
```
http://localhost:8501
```

---

## 🔧 CONFIGURATION

### Modifier les communes
Éditez `app_streamlit.py`, section `COMMUNES` :

```python
COMMUNES = {
    "Votre-Commune": {
        "nom": "Commune de Votre-Commune",
        "adresse": "Rue Exemple 1\n1234 Ville"
    },
    # Ajoutez d'autres communes...
}
```

### Modifier les utilisateurs
Éditez `app_streamlit.py`, section `UTILISATEURS` :

```python
UTILISATEURS = {
    "Prénom Nom": {
        "prenom": "Prénom",
        "nom": "Nom",
        "titre": "Titre/Fonction"
    },
    # Ajoutez d'autres utilisateurs...
}
```

### Ajouter un logo personnalisé
1. Ajoutez `logo.png` dans le dossier principal
2. L'application l'utilisera automatiquement

---

## 👥 PARTAGE AVEC VOS COLLÈGUES

### Instructions à envoyer

```
📧 Email type :

Bonjour,

Notre nouvel outil de génération de rapports EN-VS est disponible !

🔗 Lien : https://enerconseil-envs.streamlit.app

📖 Mode d'emploi :
1. Sélectionnez la commune et le signataire (menu gauche)
2. Uploadez votre fichier PDF EN-VS
3. Cliquez sur "Traiter et générer le rapport"
4. Téléchargez le document Word

✨ Fonctionnalités :
- Extraction automatique des données
- Mise en forme professionnelle
- Détection des non-conformités (alertes rouges)
- Personnalisation commune/signataire

💡 Support : [votre-email@enerconseil.ch]

Cordialement,
[Votre nom]
```

---

## 🔐 SÉCURITÉ

### Clé API Claude
- ✅ Stockée en secret (pas visible dans le code)
- ✅ Jamais commitée sur GitHub
- ✅ Accessible uniquement à vous

### Données des utilisateurs
- ✅ Les PDF ne sont jamais sauvegardés
- ✅ Traitement en mémoire temporaire
- ✅ Suppression automatique après génération

---

## 📊 MONITORING

### Streamlit Cloud Dashboard
Accédez aux statistiques :
- Nombre d'utilisations
- Temps de réponse
- Erreurs éventuelles

### Logs
Consultez les logs en temps réel dans le dashboard Streamlit

---

## 🆘 SUPPORT ET MAINTENANCE

### Mettre à jour l'application
1. Modifiez les fichiers sur GitHub
2. Streamlit redéploie automatiquement (sous 2 min)

### En cas de problème
1. Vérifiez les logs dans Streamlit Cloud
2. Testez localement avec `streamlit run app_streamlit.py`
3. Vérifiez que la clé API Claude est configurée

### Limites Streamlit Community Cloud
- ✅ Gratuit pour toujours
- ⚠️ L'app s'endort après 7 jours d'inactivité
- ⚠️ Réveil automatique à la première visite (20 secondes)
- ✅ Pas de limite d'utilisateurs
- ✅ Bande passante suffisante

---

## 💰 COÛTS

### Streamlit Community Cloud
**0€** - Gratuit

### API Claude (Anthropic)
- Modèle : Claude Sonnet 4.5
- Coût estimé : **~0.10€ par rapport généré**
- 100 rapports/mois = **~10€/mois**

### Total mensuel estimé
**~10€** pour 100 rapports

---

## 🎯 ALTERNATIVES (si besoin)

### Si vous dépassez les limites gratuites

#### Streamlit Cloud Teams
- 99$/mois
- Apps privées
- Plus de ressources
- Support prioritaire

#### Hébergement propre
- VPS OVH : ~5€/mois
- Docker + Nginx
- Contrôle total

---

## ✅ CHECKLIST DE DÉPLOIEMENT

- [ ] Compte GitHub créé
- [ ] Dépôt créé avec tous les fichiers
- [ ] Compte Streamlit Cloud créé
- [ ] Application déployée
- [ ] Clé API Claude configurée
- [ ] Test complet effectué
- [ ] URL partagée avec collègues
- [ ] Instructions envoyées

---

## 📞 CONTACT

Pour toute question sur le déploiement :
- Documentation Streamlit : https://docs.streamlit.io
- Support Anthropic : https://support.anthropic.com
- GitHub : https://github.com

---

✅ **Déploiement terminé avec succès !**

Votre équipe peut maintenant générer des rapports EN-VS en quelques clics ! 🚀
