# ⚡ DÉMARRAGE RAPIDE - 5 MINUTES

## 🎯 Objectif
Déployer votre application de génération de rapports EN-VS sur le web.

---

## ✅ CE QUE VOUS AVEZ

Une application Streamlit complète avec :
- 📱 Interface web intuitive
- 🏛️ 7 communes configurées
- 👤 5 utilisateurs configurés
- 🤖 Extraction automatique IA
- 📄 Génération Word professionnelle
- 🔴 Détection des non-conformités

**Coût : 0€** (hébergement gratuit) + ~10€/mois (API Claude)

---

## 🚀 DÉPLOIEMENT EN 7 ÉTAPES

### 1️⃣ Créer un compte GitHub (2 min)
👉 https://github.com → "Sign up"

### 2️⃣ Créer un dépôt (1 min)
- Cliquez "New repository"
- Nom : `enerconseil-envs`
- Type : Public
- Cliquez "Create"

### 3️⃣ Uploader les fichiers (2 min)
Uploadez ces 6 fichiers minimum :
```
✅ app_streamlit.py
✅ export_word.py
✅ extract.py
✅ utils.py
✅ requirements.txt
✅ .streamlit/config.toml
```

### 4️⃣ Créer un compte Streamlit (1 min)
👉 https://share.streamlit.io  
→ Se connecter avec GitHub

### 5️⃣ Déployer l'app (30 sec)
- Cliquez "New app"
- Sélectionnez votre dépôt
- Fichier : `app_streamlit.py`
- Cliquez "Deploy!"

### 6️⃣ Configurer la clé API (1 min)
- Settings → Secrets
- Ajoutez :
```toml
CLAUDE_API_KEY = "votre-clé-api-claude"
```

### 7️⃣ Testez ! (30 sec)
- Attendez le déploiement (~2 min)
- Ouvrez l'URL générée
- Testez avec un PDF

---

## 🎉 C'EST PRÊT !

Votre application est en ligne :
```
https://[votre-app].streamlit.app
```

---

## 📧 PARTAGER AVEC VOS COLLÈGUES

Envoyez-leur ce message :

```
Bonjour,

Notre nouvel outil de génération de rapports EN-VS est disponible !

🔗 Lien : https://[votre-app].streamlit.app

📖 Mode d'emploi :
1. Sélectionnez commune et signataire (menu gauche)
2. Uploadez votre PDF EN-VS
3. Cliquez "Traiter et générer"
4. Téléchargez le Word

Durée : 20 secondes ⏱️

Pour toute question : [votre-email]
```

---

## 🆘 EN CAS DE PROBLÈME

### L'app ne démarre pas
→ Vérifiez que tous les fichiers sont uploadés
→ Vérifiez les logs dans Streamlit Cloud

### Erreur "API Key missing"
→ Ajoutez `CLAUDE_API_KEY` dans les Secrets

### Autres problèmes
→ Consultez `GUIDE_DEPLOIEMENT_STREAMLIT.md` (détails complets)

---

## 📚 DOCUMENTATION COMPLÈTE

Pour aller plus loin :
- **GUIDE_DEPLOIEMENT_STREAMLIT.md** - Guide détaillé
- **GUIDE_UTILISATEUR.md** - Pour vos collègues  
- **STREAMLIT_RECAPITULATIF.md** - Vue d'ensemble
- **README.md** - Documentation technique

---

## ✨ ET APRÈS ?

1. ✅ Personnaliser les communes/utilisateurs
2. ✅ Ajouter votre logo
3. ✅ Former vos collègues
4. ✅ Collecter les feedbacks
5. ✅ Améliorer l'app

---

**⏱️ Temps total : 5-10 minutes**  
**💰 Coût : 0€ hébergement + ~10€/mois API**  
**👥 Utilisateurs : Illimité**

🚀 **Lancez-vous maintenant !**

---

*Guide de démarrage rapide - Enerconseil SA*  
*Version 1.0 - Octobre 2025*
