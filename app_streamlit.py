"""
Application Streamlit pour l'extraction et génération de rapports de conformité EN-VS
Version avec sélection de commune et utilisateur
"""

import streamlit as st
import tempfile
import os
import json
from datetime import datetime
from pathlib import Path

# Import des modules existants
from extract import lire_pdf, extraire_donnees_ia, analyser_completude
from export_word import exporter_vers_word

# Configuration de la page
st.set_page_config(
    page_title="Enerconseil - Conformité énergétique",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CONFIGURATION : Communes et Utilisateurs
# ============================================

COMMUNES = {
    "Crans-Montana": {
        "nom": "Commune de Crans-Montana",
        "adresse": "Avenue de la Gare 20\nCase postale 308\n3963 Crans-Montana"
    },
    "Lens": {
        "nom": "Commune de Lens",
        "adresse": "Service Technique\nPlace du Village 1\n1978 Lens"
    },
    "Sion": {
        "nom": "Commune de Sion",
        "adresse": "p.a. OIKEN\nRue de l'Industrie 43\n1951 Sion"
    },
    "Martigny": {
        "nom": "Commune de Nendaz",
        "adresse": "Service de l'édilité\nRoute de Nendaz 352\n1996 Basse-Nendaz"
    },
    "Fully": {
        "nom": "Commune de Fully",
        "adresse": "Service technique\nRue de l'Eglise 46\n1926 Fully"
    },
    "Noble-Contrée": {
        "nom": "Commune de Noble-Contrée",
        "adresse": "Service technique\nAvenue St-François 6\n3968 Veyras"
    },
    "Grimisuat": {
        "nom": "Commune de Grimisuat",
        "adresse": "Service technique\nPlace Mgr Gabriel Balet 1\n1971 Grimisuat"
    }
}

UTILISATEURS = {
    "Jérôme Bonvin": {
        "prenom": "Jérôme",
        "nom": "Bonvin",
        "titre": "Ingénieur énergéticien"
    },
    "Fabien Roduit": {
        "prenom": "Fabien",
        "nom": "Roduit",
        "titre": "Ingénieur thermicien"
    },
    "Quentin Remondeulaz": {
        "prenom": "Quentin",
        "nom": "Remondeulaz",
        "titre": "Ingénieur thermicien"
    },
    "Steven Deperiers": {
        "prenom": "Steven",
        "nom": "Deperiers",
        "titre": "Ingénieur thermicien"
    },
}

# ============================================
# STYLE CSS PERSONNALISÉ
# ============================================

st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #2c3e50;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #7f8c8d;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin: 1rem 0;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #3498db;
        color: white;
        border-radius: 0.5rem;
        padding: 0.75rem;
        font-weight: bold;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #2980b9;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    </style>
""", unsafe_allow_html=True)

# ============================================
# EN-TÊTE DE L'APPLICATION
# ============================================

st.markdown('<div class="main-header">🏢 Enerconseil - Contrôle de dossiers énergétiques</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Génération automatique de rapports de conformité énergétique</div>', unsafe_allow_html=True)

# ============================================
# BARRE LATÉRALE - CONFIGURATION
# ============================================

with st.sidebar:
    st.image("https://via.placeholder.com/150x50/3498db/ffffff?text=Enerconseil", width=150)
    
    st.markdown("### ⚙️ Configuration")
    
    # Sélection de la commune
    commune_selectionnee = st.selectbox(
        "🏛️ Commune destinataire",
        options=list(COMMUNES.keys()),
        index=0,
        help="Sélectionnez la commune à qui le rapport sera adressé"
    )
    
    # Sélection de l'utilisateur
    utilisateur_selectionne = st.selectbox(
        "👤 Signataire du rapport",
        options=list(UTILISATEURS.keys()),
        index=0,
        help="Sélectionnez la personne qui signera le rapport"
    )
    
    st.markdown("---")
    
    # Affichage des informations sélectionnées
    st.markdown("### 📋 Récapitulatif")
    st.markdown(f"**Destinataire :**  \n{COMMUNES[commune_selectionnee]['nom']}")
    st.markdown(f"**Signataire :**  \n{utilisateur_selectionne}")
    
    st.markdown("---")
    
    # Informations sur l'application
    st.markdown("### ℹ️ À propos")
    st.markdown("""
    Cette application permet de :
    - 📄 Extraire les données d'un PDF EN-VS
    - 🤖 Analyser avec Claude AI
    - 📊 Générer un rapport Word formaté
    - 🔴 Détecter les non-conformités
    """)
    
    st.markdown("---")
    st.markdown("**Version :** 1.0.0  \n**Date :** Octobre 2025")

# ============================================
# CONTENU PRINCIPAL
# ============================================

# Zone d'upload
st.markdown("### 📤 1. Télécharger le fichier PDF")

uploaded_file = st.file_uploader(
    "Sélectionnez un fichier PDF contenant les formulaires EN-VS",
    type=['pdf'],
    help="Formats acceptés : PDF uniquement"
)

if uploaded_file is not None:
    # Afficher les informations du fichier
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📄 Nom du fichier", uploaded_file.name)
    with col2:
        file_size = uploaded_file.size / 1024  # Ko
        st.metric("📊 Taille", f"{file_size:.1f} Ko")
    with col3:
        st.metric("📅 Date", datetime.now().strftime("%d/%m/%Y"))
    
    st.markdown("---")
    
    # Bouton de traitement
    st.markdown("### 🚀 2. Générer le rapport")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        traiter_button = st.button("🔄 Traiter et générer le rapport", use_container_width=True)
    
    if traiter_button:
        # Créer un dossier temporaire
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            
            # Sauvegarder le PDF temporairement
            pdf_path = temp_dir_path / uploaded_file.name
            with open(pdf_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Étape 1 : Lecture du PDF
                status_text.markdown("📖 **Étape 1/4 :** Lecture du fichier PDF...")
                progress_bar.progress(25)
                
                texte_pdf = lire_pdf(str(pdf_path))
                
                if not texte_pdf.strip():
                    st.markdown('<div class="error-box">❌ <b>Erreur :</b> Le PDF semble vide ou illisible.</div>', unsafe_allow_html=True)
                    st.stop()
                
                st.markdown(f'<div class="success-box">✅ PDF lu avec succès ({len(texte_pdf)} caractères extraits)</div>', unsafe_allow_html=True)
                
                # Étape 2 : Extraction avec IA
                status_text.markdown("🤖 **Étape 2/4 :** Extraction des données avec Claude AI...")
                progress_bar.progress(50)
                
                # Vérifier la clé API
                if not os.getenv("CLAUDE_API_KEY"):
                    st.markdown('<div class="error-box">❌ <b>Erreur :</b> Clé API Claude manquante. Configurez CLAUDE_API_KEY dans les secrets.</div>', unsafe_allow_html=True)
                    st.stop()
                
                json_resultat = extraire_donnees_ia(texte_pdf, uploaded_file.name)
                data = json.loads(json_resultat)
                
                if "erreur" in data:
                    st.markdown(f'<div class="error-box">❌ <b>Erreur lors de l\'extraction :</b> {data["erreur"]}</div>', unsafe_allow_html=True)
                    st.stop()
                
                # Sauvegarder le JSON
                json_path = temp_dir_path / f"{Path(uploaded_file.name).stem}_extraction.json"
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                st.markdown('<div class="success-box">✅ Données extraites avec succès</div>', unsafe_allow_html=True)
                
                # Afficher un aperçu des données
                with st.expander("🔍 Aperçu des données extraites"):
                    st.json(data)
                
                # Analyse de complétude
                with st.expander("📊 Analyse de complétude"):
                    # Simple comptage
                    def compter_champs(obj):
                        count = 0
                        total = 0
                        if isinstance(obj, dict):
                            for v in obj.values():
                                c, t = compter_champs(v)
                                count += c
                                total += t
                        elif isinstance(obj, list):
                            if len(obj) > 0:
                                count = 1
                            total = 1
                        else:
                            total = 1
                            if obj is not None:
                                count = 1
                        return count, total
                    
                    remplis, total = compter_champs(data)
                    pourcentage = 100 * remplis / total if total > 0 else 0
                    
                    st.metric("Complétude des données", f"{pourcentage:.1f}%", f"{remplis}/{total} champs")
                    st.progress(pourcentage / 100)
                
                # Étape 3 : Modification des données pour commune/utilisateur
                status_text.markdown("⚙️ **Étape 3/4 :** Configuration du rapport...")
                progress_bar.progress(75)
                
                # Sauvegarder la configuration dans le JSON pour export_word
                data['_config'] = {
                    'commune': COMMUNES[commune_selectionnee],
                    'utilisateur': UTILISATEURS[utilisateur_selectionne]
                }
                
                # Re-sauvegarder avec config
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                # Étape 4 : Génération du Word
                status_text.markdown("📄 **Étape 4/4 :** Génération du document Word...")
                progress_bar.progress(90)
                
                output_word_path = exporter_vers_word(
                    str(json_path),
                    str(temp_dir_path / f"{Path(uploaded_file.name).stem}_rapport_conformite.docx")
                )
                
                progress_bar.progress(100)
                status_text.markdown("✅ **Traitement terminé avec succès !**")
                
                st.markdown('<div class="success-box">🎉 <b>Rapport généré avec succès !</b></div>', unsafe_allow_html=True)
                
                # Bouton de téléchargement
                st.markdown("### 📥 3. Télécharger le rapport")
                
                with open(output_word_path, "rb") as file:
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        st.download_button(
                            label="⬇️ Télécharger le rapport Word",
                            data=file,
                            file_name=f"{Path(uploaded_file.name).stem}_rapport_conformite.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            use_container_width=True
                        )
                
                # Informations complémentaires
                st.markdown("---")
                st.markdown("### 📋 Informations du rapport")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"""
                    **Destinataire :**  
                    {COMMUNES[commune_selectionnee]['nom']}
                    
                    **Dossier :**  
                    {data.get('numero_dossier', 'Non spécifié')}
                    """)
                
                with col2:
                    st.markdown(f"""
                    **Signataire :**  
                    {utilisateur_selectionne}  
                    {UTILISATEURS[utilisateur_selectionne]['titre']}
                    
                    **Date :**  
                    {datetime.now().strftime('%d %B %Y')}
                    """)
                
                # Alertes sur les non-conformités
                st.markdown("---")
                st.markdown("### ⚠️ Alertes")
                
                # Vérifier s'il y a des éléments non conformes
                alertes = []
                for form_key in ['EN-VS-102a', 'EN-VS-102b']:
                    if form_key in data:
                        form_data = data[form_key]
                        
                        # Vérifier éléments opaques
                        if 'elements_enveloppe_opaques' in form_data:
                            for elem in form_data['elements_enveloppe_opaques']:
                                u = elem.get('valeur_u')
                                u_lim = elem.get('valeur_u_limite')
                                if u is not None and u_lim is not None:
                                    try:
                                        if float(u) > float(u_lim):
                                            alertes.append(f"🔴 {elem.get('element', 'Élément')} : U={u} > {u_lim}")
                                    except:
                                        pass
                        
                        # Vérifier éléments vitrés
                        if 'elements_enveloppe_vitres' in form_data:
                            for elem in form_data['elements_enveloppe_vitres']:
                                u = elem.get('valeur_u_fenetre')
                                u_lim = elem.get('valeur_u_limite')
                                if u is not None and u_lim is not None:
                                    try:
                                        if float(u) > float(u_lim):
                                            alertes.append(f"🔴 {elem.get('element', 'Élément')} : U={u} > {u_lim}")
                                    except:
                                        pass
                
                if alertes:
                    st.markdown('<div class="warning-box"><b>⚠️ Non-conformités détectées :</b></div>', unsafe_allow_html=True)
                    for alerte in alertes:
                        st.markdown(f"- {alerte}")
                    st.markdown("*Ces éléments sont surlignés en ROUGE dans le rapport Word.*")
                else:
                    st.markdown('<div class="success-box">✅ <b>Aucune non-conformité détectée</b></div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.markdown(f'<div class="error-box">❌ <b>Erreur :</b> {str(e)}</div>', unsafe_allow_html=True)
                st.exception(e)

else:
    # Message d'attente
    st.markdown('<div class="info-box">👆 <b>Commencez par télécharger un fichier PDF pour démarrer l\'analyse.</b></div>', unsafe_allow_html=True)
    
    # Guide d'utilisation
    st.markdown("---")
    st.markdown("### 📖 Guide d'utilisation")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        #### 1️⃣ Configuration
        - Sélectionnez la commune
        - Choisissez le signataire
        """)
    
    with col2:
        st.markdown("""
        #### 2️⃣ Upload
        - Glissez-déposez votre PDF
        - Ou cliquez pour sélectionner
        """)
    
    with col3:
        st.markdown("""
        #### 3️⃣ Génération
        - Cliquez sur "Traiter"
        - Téléchargez le rapport
        """)
    
    st.markdown("---")
    
    # Fonctionnalités
    st.markdown("### ✨ Fonctionnalités")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Extraction automatique :**
        - ✅ Tous les formulaires EN-VS
        - ✅ Données d'enveloppe (opaques + vitrés)
        - ✅ Systèmes techniques
        - ✅ Numéro de dossier
        """)
    
    with col2:
        st.markdown("""
        **Rapport Word professionnel :**
        - ✅ Mise en forme automatique
        - ✅ Tableaux formatés
        - ✅ Alertes visuelles (🟡 🔴 🟢)
        - ✅ Signatures personnalisées
        """)

# ============================================
# PIED DE PAGE
# ============================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d; font-size: 0.9rem;'>
    🏢 <b>Enerconseil SA</b> | Passage de la Matze 13, CH-1950 Sion<br>
    📞 027 558 83 47 | 🌐 www.enerconseil.ch | ✉️ sion@enerconseil.ch
</div>
""", unsafe_allow_html=True)
