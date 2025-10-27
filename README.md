# 🏢 Enerconseil - Générateur de Rapports EN-VS

Application web pour la génération automatique de rapports de conformité énergétique (formulaires EN-VS du canton du Valais).

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![Streamlit](https://img.shields.io/badge/streamlit-1.29-red)

## ✨ Fonctionnalités

- 📤 **Upload PDF** - Importez vos formulaires EN-VS
- 🤖 **Extraction IA** - Analyse automatique avec Claude AI
- 🏛️ **Multi-communes** - 7 communes valaisannes configurées
- 👤 **Multi-utilisateurs** - 5 signataires prédéfinis
- 📄 **Export Word** - Rapports professionnels formatés
- 🔴 **Alertes visuelles** - Détection automatique des non-conformités
- ✅ **100% automatique** - Aucune saisie manuelle requise

## 🚀 Démarrage rapide

### Prérequis

- Python 3.9+
- Clé API Claude (Anthropic)

### Installation

```bash
# Cloner le dépôt
git clone https://github.com/votre-username/enerconseil-envs.git
cd enerconseil-envs

# Installer les dépendances
pip install -r requirements.txt

# Configurer la clé API
echo "CLAUDE_API_KEY=votre-clé-api" > .env

# Lancer l'application
streamlit run app_streamlit.py
```

L'application s'ouvre sur http://localhost:8501

## 📋 Formulaires supportés

- ✅ EN-VS - Informations générales
- ✅ EN-VS-101a - Solution standard
- ✅ EN-VS-101b - Valeur limite EHWLK
- ✅ EN-VS-102a - Enveloppe thermique (simplifié)
- ✅ EN-VS-102b - Besoins de chaleur (détaillé)
- ✅ EN-VS-103 - Chauffage et ECS
- ✅ EN-VS-104 - Production électricité
- ✅ EN-VS-105 - Ventilation
- ✅ EN-VS-110 - Rafraîchissement

## 🏛️ Communes configurées

1. Crans-Montana
2. Sion
3. Sierre
4. Martigny
5. Monthey
6. Brig-Glis
7. Visp

## 👥 Utilisateurs configurés

1. Jérôme Bonvin - Ingénieur énergéticien
2. Marie Dupont - Ingénieure énergéticienne
3. Pierre Martin - Ingénieur thermicien
4. Sophie Laurent - Experte en performance énergétique
5. Thomas Moreau - Consultant énergétique

## ⚙️ Configuration personnalisée

### Ajouter une commune

Éditez `app_streamlit.py` :

```python
COMMUNES = {
    "Votre-Commune": {
        "nom": "Commune de Votre-Commune",
        "adresse": "Rue Exemple 1\n1234 Ville"
    }
}
```

### Ajouter un utilisateur

```python
UTILISATEURS = {
    "Prénom Nom": {
        "prenom": "Prénom",
        "nom": "Nom",
        "titre": "Votre titre"
    }
}
```

## 📊 Fonctionnalités du rapport

### Extraction automatique
- Numéro de dossier
- Données techniques complètes
- Éléments d'enveloppe (opaques + vitrés)
- Systèmes énergétiques

### Mise en forme professionnelle
- En-tête personnalisé (commune + signataire)
- Tableaux formatés
- Corrections orthographiques automatiques
- Unités correctes (m², kW, Wc, W/m²)

### Alertes visuelles
- 🟡 **Jaune** - Solution standard choisie
- 🔴 **Rouge** - Non-conformités (U > U limite)
- 🟢 **Vert** - Préavis encadré

## 🔐 Sécurité

- Clé API stockée en sécurité (secrets Streamlit)
- Pas de sauvegarde des données utilisateur
- Traitement en mémoire temporaire
- Suppression automatique après génération

## 📈 Performance

- Extraction : ~10-15 secondes
- Génération Word : ~2-3 secondes
- **Total : ~15-20 secondes par rapport**

## 💰 Coûts

- **Streamlit Community Cloud** : Gratuit
- **API Claude** : ~0.10€ par rapport
- **Total** : ~10€/mois pour 100 rapports

## 🛠️ Technologies utilisées

- **Frontend** : Streamlit
- **IA** : Anthropic Claude Sonnet 4.5
- **PDF** : pdfplumber
- **Word** : python-docx
- **Hébergement** : Streamlit Community Cloud

## 📖 Documentation

- [Guide de déploiement complet](GUIDE_DEPLOIEMENT_STREAMLIT.md)
- [Documentation des modifications](MODIFICATIONS_FINALES.md)
- [Info alerte rouge](ALERTE_ROUGE_INFO.md)

## 🤝 Support

Pour toute question ou problème :
- Consultez la [documentation Streamlit](https://docs.streamlit.io)
- Vérifiez les [logs de l'application](https://share.streamlit.io)
- Contactez le support Anthropic

## 📄 Licence

Copyright © 2025 Enerconseil SA  
Tous droits réservés

## 🎯 Roadmap

- [ ] Mode batch (plusieurs PDF à la fois)
- [ ] Export PDF en plus du Word
- [ ] Historique des rapports générés
- [ ] Statistiques d'utilisation
- [ ] API REST pour intégration

## ✅ Statut

**Version stable 1.0.0** - Prêt pour la production

---

Développé avec ❤️ par Enerconseil SA
