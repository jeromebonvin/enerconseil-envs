"""
Export des données JSON extraites vers un document Word formaté (Document de Conformité)
Version CORRIGÉE avec remplissage des tableaux et corrections orthographiques
Usage : python export_word.py fichier_extraction.json
"""

import json
import argparse
import os
from datetime import datetime
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

from utils import (
    set_font,
    remove_table_borders,
    set_table_header_gray,
    info,
    success,
    warning,
    error,
)


# -----------------------------------------------------
# CORRECTION ORTHOGRAPHIQUE
# -----------------------------------------------------
def corriger_orthographe_champ(nom_champ):
    """Corrige l'orthographe et la casse des noms de champs"""
    corrections = {
        # Générales
        'sre': 'SRE',
        'snf': 'SNF',
        'sre neuf': 'SRE neuf',
        'sre existant': 'SRE existant',
        'egid': 'EGID',
        'ecs': 'ECS',
        'pac': 'PAC',
        'pc': 'PC',
        'sia': 'SIA',
        'minergie': 'Minergie',
        'ehwlk': 'EHWLK',
        'qh': 'Qh',
        
        # EN-VS
        'type de batiment': 'Type de bâtiment',
        'type batiment': 'Type de bâtiment',
        'type de construction': None,  # À supprimer
        'affectation principale': 'Affectation principale',
        'nombre d etages': "Nombre d'étages",
        'nombre etages': "Nombre d'étages",
        'annee construction': 'Année construction',
        'annee de construction': 'Année de construction',
        'numero parcelle': 'Numéro parcelle',
        'maitre ouvrage': "Maître d'ouvrage",
        'maitre d ouvrage': "Maître d'ouvrage",
        'nature des travaux': 'Nature des travaux',
        'projet interet cantonal': "Projet d'intérêt cantonal",
        'categorie sia': 'Catégorie SIA',
        'type de chauffage': 'Type de chauffage',
        'couverture des besoins de chaleur': 'Couverture des besoins de chaleur',
        'formulaires necessaires ou annexes': 'Formulaires annexés',
        
        # EN-VS-101a
        'rafraichissement humidification ou deshumidification': 'Rafraîchissement et/ou (dés)humidification',
        'pac reversible projetee': 'PAC réversible projetée',
        'solution standard choisie': 'Solution standard choisie',
        
        # EN-VS-102a
        'hygiene air interieur concept ventilation': 'Concept de ventilation',
        'protection thermique ete valeur g': 'Respect de la valeur g',
        'protection thermique ete rafraichissement': 'Rafraîchissement',
        'valeurs u respectees par tous elements': 'Valeurs U respectées par tous les éléments',
        'justificatif ponts thermiques respecte': 'Justificatif des ponts thermiques respecté',
        'enveloppe thermique completement fermee': 'Enveloppe thermique complètement fermée',
        'tous locaux chauffes interieur enveloppe': "Tous les locaux chauffés à l'intérieur de l'enveloppe thermique",
        
        # EN-VS-103
        'type de generateur de chaleur': 'Type de générateur de chaleur',
        'puissance thermique kw': 'Puissance thermique',
        'dispositif comptage energie': "Dispositif de comptage d'énergie",
        'emission chaleur locaux isoles': 'Émission de chaleur que dans locaux isolés',
        'emission de chaleur': 'Émission de chaleur',
        'temperature emission chaleur': "Température de départ de l'émetteur de chaleur",
        'regulation temperature par local': 'Régulation de température par local',
        'temperature ecs inferieure 60': 'Température ECS < 60°C',
        'systeme mesure installe chauffage': 'Système de mesure installé pour chauffage',
        'systeme mesure installe ecs': 'Système de mesure installé pour ECS',
        
        # EN-VS-104
        'puissance production propre electricite annuelle': 'Puissance projetée',
        'puissance production propre electricite requise': 'Puissance requise',
        'nbre de panneaux': 'Nombre de panneaux',
        'punitaire des panneaux wc': 'Puissance unitaire des panneaux',
        
        # EN-VS-110
        'surface nette plancher rafraichi deshumidifie': 'Surface nette de plancher rafraîchie',
        'total puissances thermiques frigorifiques': 'Total des puissances frigorifiques',
        'puissances electriques total kw': 'Puissance électrique totale',
        'puissances electriques puissance specifique w m2': 'Puissance spécifique',
        
        # Autres
        'responsable': 'Responsable',
        'architecte': 'Architecte',
        'telephone': 'Téléphone',
        'thermique': 'Thermique',
        'energie': 'Énergie',
        'batiment': 'Bâtiment',
        'electrique': 'Électrique',
        'electricite': 'Électricité',
        'categorie': 'Catégorie',
        'renouvellement': 'Renouvellement',
        'renovation': 'Rénovation',
        'chauffage': 'Chauffage',
        'ventilation': 'Ventilation',
        'refroidissement': 'Refroidissement',
        'climatisation': 'Climatisation',
        'eau chaude sanitaire': 'Eau chaude sanitaire',
        'enveloppe': 'Enveloppe',
        'isolation': 'Isolation',
        'coefficient': 'Coefficient',
        'puissance': 'Puissance',
        'rendement': 'Rendement',
        'surface': 'Surface',
        'volume': 'Volume',
        'deperdition': 'Déperdition',
        'apport': 'Apport',
        'besoin': 'Besoin',
        'production': 'Production',
        'consommation': 'Consommation',
    }
    
    nom_lower = nom_champ.lower()
    
    # Chercher une correspondance exacte
    if nom_lower in corrections:
        result = corrections[nom_lower]
        if result is None:  # Champ à supprimer
            return None
        return result
    
    # Chercher une correspondance partielle
    for pattern, replacement in corrections.items():
        if replacement is not None and pattern in nom_lower:
            nom_champ = nom_champ.lower().replace(pattern, replacement)
    
    # Capitaliser la première lettre si ce n'est pas déjà fait
    if nom_champ and not nom_champ[0].isupper():
        nom_champ = nom_champ[0].upper() + nom_champ[1:]
    
    return nom_champ


# -----------------------------------------------------
# 1️⃣ EN-TÊTE DU DOCUMENT
# -----------------------------------------------------
def ajouter_entete(doc, numero_dossier=None, config=None):
    """Ajoute l'en-tête (logo, adresse, date, introduction)."""
    header_table = doc.add_table(rows=3, cols=2)
    remove_table_borders(header_table)

    # Logo + adresse
    cell_logo = header_table.rows[0].cells[0]
    cell_logo.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
    logo_path = "logo.png"
    if os.path.exists(logo_path):
        try:
            run = cell_logo.paragraphs[0].add_run()
            run.add_picture(logo_path, width=Inches(2.25))
        except Exception as e:
            warning(f"Logo non inséré : {e}")
    p = cell_logo.add_paragraph(
        "Passage de la Matze 13\nCH-1950 Sion\n027 558 83 47\nwww.enerconseil.ch\nsion@enerconseil.ch"
    )
    p.paragraph_format.space_before = Pt(0)
    set_font(p)

    # Destinataire (depuis config si disponible)
    cell_dest = header_table.rows[1].cells[1]
    p = cell_dest.paragraphs[0]
    
    if config and 'commune' in config:
        commune_info = config['commune']
        p.text = f"{commune_info['nom']}\n{commune_info['adresse']}"
    else:
        # Valeur par défaut
        p.text = "Commune de Crans-Montana\nAvenue de la Gare 20\nCase postale 308\n3963 Crans-Montana 1"
    
    p.paragraph_format.space_after = Pt(24)  # ✅ Espace après l'adresse (modifié selon vos préférences)
    set_font(p)

    # Date
    mois_fr = {
        "January": "janvier", "February": "février", "March": "mars",
        "April": "avril", "May": "mai", "June": "juin",
        "July": "juillet", "August": "août", "September": "septembre",
        "October": "octobre", "November": "novembre", "December": "décembre"
    }
    date_aujourd_hui = datetime.now().strftime("Sion, le %d %B %Y")
    for en, fr in mois_fr.items():
        date_aujourd_hui = date_aujourd_hui.replace(en, fr)
    cell_date = header_table.rows[2].cells[1]
    p = cell_date.paragraphs[0]
    p.text = date_aujourd_hui
    set_font(p)

    header_table.columns[0].width = Cm(10)
    header_table.columns[1].width = Cm(7)

    # Titre dossier
    if numero_dossier:
        p1 = doc.add_paragraph(f"Dossier {numero_dossier}")
        set_font(p1, bold=True)
        p1.paragraph_format.space_after = Pt(0)
        p1.paragraph_format.space_before = Pt(0)

    p2 = doc.add_paragraph("Contrôle de dossier thermique pour autorisation de construire")
    set_font(p2, bold=True)
    p2.paragraph_format.space_before = Pt(0)

    p = doc.add_paragraph("Mesdames, Messieurs,")
    p.paragraph_format.space_before = Pt(0)
    set_font(p)

    p = doc.add_paragraph(
        "Nous vous retournons en annexe le dossier énergétique pour le projet en référence. "
        "Le calcul est réalisé de manière correcte, en performance globale. "
        "Le projet respecte les exigences légales (normes SIA 380/1 : 2016 et SIA 180)."
    )
    set_font(p)

    p = doc.add_paragraph(
        "Les caractéristiques principales concernant ce bâtiment sont les suivantes :"
    )
    set_font(p)


# -----------------------------------------------------
# 2️⃣ TABLEAUX D'ÉLÉMENTS D'ENVELOPPE
# -----------------------------------------------------
def creer_tableau_elements_enveloppe_opaque(doc, elements):
    if not elements:
        return

    p = doc.add_paragraph("Composition des éléments d'enveloppe :")
    set_font(p)

    table = doc.add_table(rows=len(elements) + 1, cols=4)
    table.style = "Table Grid"

    headers = ["Élément", "Couches d'isolation", "Valeur U projet (W/m²K)", "Valeur U limite (W/m²K)"]
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = h
        set_font(cell.paragraphs[0], bold=True)
        set_table_header_gray(cell)

    for idx, elem in enumerate(elements, 1):
        c = table.rows[idx].cells
        c[0].text = str(elem.get("element", "—"))
        
        # Couches d'isolation : nouveau format OU ancien format (rétrocompatible)
        couches = elem.get('couches_isolation', '')
        
        # Si le nouveau champ n'existe pas ou est vide, reconstruire depuis les anciens champs
        if not couches:
            construction_parts = []
            epaisseur = elem.get('epaisseur_isolation_cm')
            type_iso = elem.get('type_isolation')
            lambda_val = elem.get('lambda_isolation')
            
            if epaisseur is not None:
                construction_parts.append(f"{epaisseur} cm")
            if type_iso:
                construction_parts.append(f"de {type_iso}")
            if lambda_val is not None:
                construction_parts.append(f"(λ={lambda_val} W/mK)")
            
            couches = " ".join(construction_parts) if construction_parts else "—"
        
        c[1].text = couches
        
        c[2].text = str(elem.get("valeur_u")) if elem.get("valeur_u") is not None else "—"
        c[3].text = str(elem.get("valeur_u_limite")) if elem.get("valeur_u_limite") is not None else "—"
        
        for cell in c:
            set_font(cell.paragraphs[0])
        
        # ✅ Mettre la ligne en rouge si U projet > U limite
        valeur_u = elem.get("valeur_u")
        valeur_u_limite = elem.get("valeur_u_limite")
        
        if valeur_u is not None and valeur_u_limite is not None:
            try:
                if float(valeur_u) > float(valeur_u_limite):
                    # Mettre toute la ligne en rouge
                    from docx.oxml import parse_xml
                    from docx.oxml.ns import nsdecls
                    for cell in c:
                        shading_elm = parse_xml(r'<w:shd {} w:fill="FF0000"/>'.format(nsdecls('w')))  # Rouge
                        cell._element.get_or_add_tcPr().append(shading_elm)
                        # Mettre le texte en blanc pour la lisibilité
                        for run in cell.paragraphs[0].runs:
                            run.font.color.rgb = RGBColor(255, 255, 255)
            except (ValueError, TypeError):
                pass  # Si conversion impossible, ignorer

    table.columns[0].width = Cm(3.5)   # Élément
    table.columns[1].width = Cm(10.0)  # Couches d'isolation (agrandi)
    table.columns[2].width = Cm(1.75)  # U projet
    table.columns[3].width = Cm(1.75)  # U limite


def ajouter_elements_vitres_au_tableau(table, elements_vitres):
    """Ajoute les éléments vitrés à la suite du tableau existant"""
    if not elements_vitres:
        return
    
    for elem in elements_vitres:
        # Ajouter une nouvelle ligne
        row = table.add_row()
        c = row.cells
        
        # Nom de l'élément
        element_nom = str(elem.get("element", "—"))
        c[0].text = element_nom
        
        # Construction détaillée pour fenêtres/portes
        element_lower = element_nom.lower()
        
        if 'porte' in element_lower and 'garage' in element_lower:
            # Porte de garage
            c[1].text = "Porte isolante à définir"
        elif 'porte' in element_lower:
            # Porte simple
            c[1].text = "Porte isolante à définir"
        else:
            # Fenêtre, porte-fenêtre, velux - Nouveau format avec Ug, Uf, g OU ancien format
            ug = elem.get("valeur_ug") or elem.get("valeur_u_vitrage")  # Nouveau OU ancien
            uf = elem.get("valeur_uf")  # Cadre
            uw = elem.get("valeur_uw") or elem.get("valeur_u_fenetre")  # Nouveau OU ancien
            facteur_g = elem.get("facteur_g")  # Facteur solaire
            
            # Détecter si double ou triple vitrage basé sur Ug
            if ug is not None:
                if ug <= 0.7:
                    type_vitrage = "Triple vitrage"
                else:
                    type_vitrage = "Double vitrage"
            else:
                type_vitrage = "Double/Triple vitrage"
            
            # Construction de la description
            parts = [type_vitrage]
            
            if ug is not None:
                parts.append(f"Ug = {ug} W/m²K")
            else:
                parts.append("Ug = xx W/m²K")
            
            if facteur_g is not None:
                parts.append(f"g = {facteur_g}")
            else:
                parts.append("g = xx")
            
            if uf is not None:
                parts.append(f"cadre performant Uf = {uf} W/mK")
            else:
                parts.append("cadre performant Uf = xx W/mK")
            
            parts.append("intercalaire à rupture thermique")
            
            construction = ", ".join(parts)
            c[1].text = construction
        
        # U fenêtre (projet) - Utiliser valeur_uw OU valeur_u_fenetre (rétrocompatible)
        u_fenetre = elem.get("valeur_uw") or elem.get("valeur_u_fenetre")
        c[2].text = str(u_fenetre) if u_fenetre is not None else "—"
        
        # U limite
        c[3].text = str(elem.get("valeur_u_limite")) if elem.get("valeur_u_limite") is not None else "—"
        
        for cell in c:
            set_font(cell.paragraphs[0])
        
        # ✅ Mettre la ligne en rouge si Uw > U limite (rétrocompatible)
        valeur_uw = elem.get("valeur_uw") or elem.get("valeur_u_fenetre")
        valeur_u_limite = elem.get("valeur_u_limite")
        
        if valeur_uw is not None and valeur_u_limite is not None:
            try:
                if float(valeur_uw) > float(valeur_u_limite):
                    # Mettre toute la ligne en rouge
                    from docx.oxml import parse_xml
                    from docx.oxml.ns import nsdecls
                    for cell in c:
                        shading_elm = parse_xml(r'<w:shd {} w:fill="FF0000"/>'.format(nsdecls('w')))  # Rouge
                        cell._element.get_or_add_tcPr().append(shading_elm)
                        # Mettre le texte en blanc pour la lisibilité
                        for run in cell.paragraphs[0].runs:
                            run.font.color.rgb = RGBColor(255, 255, 255)
            except (ValueError, TypeError):
                pass  # Si conversion impossible, ignorer


# -----------------------------------------------------
# 3️⃣ FORMULAIRES INDIVIDUELS
# -----------------------------------------------------
def creer_tableau_formulaire(doc, titre_formulaire, donnees, form_id=None):
    elements_opaques = donnees.get("elements_enveloppe_opaques", [])
    elements_vitres = donnees.get("elements_enveloppe_vitres", [])

    donnees_filtrees = {
        k: v for k, v in donnees.items()
        if k not in ["elements_enveloppe_opaques", "elements_enveloppe_vitres"]
    }
    
    # ✅ Filtrer les champs à supprimer AVANT de créer le tableau
    donnees_a_afficher = {}
    for cle, valeur in donnees_filtrees.items():
        if form_id == 'EN-VS':
            if cle == 'type_de_construction':
                continue  # Supprimer ce champ
            elif cle == 'sre_neuf':
                nom_champ = 'SRE neuf'
            elif cle == 'sre_existant':
                nom_champ = 'SRE existant'
            else:
                nom_champ = cle.replace('_', ' ')
                nom_champ = corriger_orthographe_champ(nom_champ)
        else:
            nom_champ = cle.replace('_', ' ')
            nom_champ = corriger_orthographe_champ(nom_champ)
        
        if nom_champ is not None:  # Ne pas inclure les champs None
            donnees_a_afficher[cle] = (nom_champ, valeur)

    titre = doc.add_heading(titre_formulaire, level=2)
    for run in titre.runs:
        run.font.name = "Arial"
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(0, 0, 0)

    # ✅ REMPLIR LE TABLEAU AVEC LES DONNÉES
    if donnees_a_afficher:
        table = doc.add_table(rows=len(donnees_a_afficher), cols=2)
        table.style = "Table Grid"

        # Bordures horizontales grises uniquement
        tbl = table._element
        tblPr = tbl.find(qn('w:tblPr'))
        if tblPr is None:
            tblPr = OxmlElement('w:tblPr')
            tbl.insert(0, tblPr)
        tblBorders = OxmlElement('w:tblBorders')
        for border_name, color in [
            ('top', 'BFBFBF'), ('bottom', 'BFBFBF'), ('insideH', 'BFBFBF'),
            ('left', 'none'), ('right', 'none'), ('insideV', 'none')
        ]:
            border = OxmlElement(f'w:{border_name}')
            border.set(qn('w:val'), 'single' if color != 'none' else 'none')
            border.set(qn('w:sz'), '4')
            border.set(qn('w:space'), '0')
            border.set(qn('w:color'), color if color != 'none' else 'auto')
            tblBorders.append(border)
        tblPr.append(tblBorders)

        # ✅ REMPLIR LES DONNÉES
        for idx, (cle, (nom_champ, valeur)) in enumerate(donnees_a_afficher.items()):
            row_cells = table.rows[idx].cells
            
            row_cells[0].text = nom_champ
            set_font(row_cells[0].paragraphs[0])
            
            # Formater la valeur
            if valeur is None:
                valeur_str = "—"
            elif isinstance(valeur, bool):
                valeur_str = "✓ Oui" if valeur else "✗ Non"
            elif isinstance(valeur, (int, float)):
                valeur_str = str(valeur)
                
                # Ajouter les unités pour les cas spéciaux
                if form_id == 'EN-VS' and cle in ['sre_neuf', 'sre_existant']:
                    valeur_str += " m²"
                elif form_id == 'EN-VS-103':
                    if 'puissance' in cle.lower():
                        valeur_str += " kW"
                elif form_id == 'EN-VS-104':
                    if 'punitaire' in cle.lower():
                        valeur_str += " Wc"
                    elif 'puissance' in cle.lower():
                        valeur_str += " kW"
                elif form_id == 'EN-VS-110':
                    if 'surface' in cle.lower():
                        valeur_str += " m²"
                    elif 'specifique' in cle.lower():
                        valeur_str += " W/m²"
                    elif 'puissance' in cle.lower() and 'specifique' not in cle.lower():
                        valeur_str += " kW"
            elif isinstance(valeur, list):
                valeur_str = ", ".join(str(v) for v in valeur) if valeur else "—"
            elif isinstance(valeur, dict):
                valeur_str = json.dumps(valeur, ensure_ascii=False, indent=2)
            else:
                valeur_str = str(valeur)
            
            row_cells[1].text = valeur_str
            set_font(row_cells[1].paragraphs[0])
            
            # ✅ Surligner en jaune la ligne "Solution standard choisie"
            if form_id == 'EN-VS-101a' and 'solution' in cle.lower() and 'standard' in cle.lower():
                from docx.oxml import parse_xml
                from docx.oxml.ns import nsdecls
                for cell in row_cells:
                    shading_elm = parse_xml(r'<w:shd {} w:fill="FFFF00"/>'.format(nsdecls('w')))  # Jaune
                    cell._element.get_or_add_tcPr().append(shading_elm)

        table.columns[0].width = Inches(3.0)
        table.columns[1].width = Inches(4.0)
        doc.add_paragraph()

    # Tableaux d'enveloppe
    if elements_opaques or elements_vitres:
        creer_tableau_elements_enveloppe_opaque(doc, elements_opaques)
        
        # Ajouter les éléments vitrés dans le même tableau
        if elements_vitres:
            # Retrouver le dernier tableau créé
            tables = doc.tables
            if tables:
                dernier_tableau = tables[-1]
                ajouter_elements_vitres_au_tableau(dernier_tableau, elements_vitres)
        
        doc.add_paragraph()


# -----------------------------------------------------
# 4️⃣ PIED DE PAGE
# -----------------------------------------------------
def ajouter_pied_de_page(doc, config=None):
    doc.add_paragraph()

    # Remarques
    remarques_table = doc.add_table(rows=1, cols=1)
    remarques_table.style = "Table Grid"
    cell = remarques_table.rows[0].cells[0]
    p = cell.paragraphs[0]
    p.text = "Remarques :"
    set_font(p, bold=True)

    remarques = [
        "Le bâtiment doit être équipé d'un système de mesure par unité d'occupation "
        "pour le chauffage et l'eau chaude sanitaire (décompte individuel des frais "
        "de chauffage et d'ECS).",

        "Étant donné les hauteurs de fenêtres, nous vous recommandons fortement d'installer "
        "du triple vitrage, selon les indications de la norme SIA 180:2014 (point 4.1.3), "
        "sans quoi les exigences de confort hivernal dans la cuisine et séjour ne sont pas respectées.",

        "Nous recommandons l'appui d'un physicien du bâtiment pour éviter tout risque de "
        "condensation et de moisissures au niveau des ponts thermiques et autres raccords."
    ]
    for r in remarques:
        p = cell.add_paragraph(r, style="List Bullet")
        set_font(p)

    # Préavis
    doc.add_paragraph()
    preavis_table = doc.add_table(rows=1, cols=1)
    preavis_table.style = "Table Grid"
    
    # ✅ Encadrer en vert
    tbl = preavis_table._element
    tblPr = tbl.find(qn('w:tblPr'))
    if tblPr is None:
        tblPr = OxmlElement('w:tblPr')
        tbl.insert(0, tblPr)
    
    tblBorders = OxmlElement('w:tblBorders')
    for border_name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        border = OxmlElement(f'w:{border_name}')
        border.set(qn('w:val'), 'single')
        border.set(qn('w:sz'), '12')  # Épaisseur
        border.set(qn('w:space'), '0')
        border.set(qn('w:color'), '00B050')  # Vert
        tblBorders.append(border)
    tblPr.append(tblBorders)
    
    cell = preavis_table.rows[0].cells[0]
    p = cell.paragraphs[0]
    p.text = "Préavis"
    set_font(p, bold=True)

    preavis = [
        "Le projet de construction présenté respecte les exigences légales "
        "(LcEne, SIA 380/1 et SIA 180), conformément au document de conformité "
        "joint au préavis.",

        "Le projet respecte les exigences légales (normes SIA 380/1 : 2016 et SIA 180), "
        "sous réserve de la validation du justificatif EN-VS-105 qui sera envoyé plus tard. "
        "Ce dernier doit nous parvenir pour contrôle au plus tard 8 semaines avant le début "
        "des travaux, comme mentionné sur le formulaire EN-VS."
    ]
    for r in preavis:
        p = cell.add_paragraph(r, style="List Bullet")
        set_font(p)
    
    doc.add_paragraph()  # ✅ Ligne après le préavis

    # Texte final
    p = doc.add_paragraph(
        "Les indications figurant dans ce rapport doivent être respectées. "
        "Des contrôles sur chantier peuvent être effectués."
    )
    set_font(p)

    p = doc.add_paragraph(
        "En vous souhaitant bonne réception, nous vous prions d'agréer, "
        "Mesdames, Messieurs, nos meilleures salutations."
    )
    set_font(p)

    doc.add_paragraph()

    # Signature (depuis config si disponible)
    sig_table = doc.add_table(rows=1, cols=2)
    remove_table_borders(sig_table)
    sig_table.columns[0].width = Cm(10)
    sig_table.columns[1].width = Cm(7)
    
    cell = sig_table.rows[0].cells[1]
    p = cell.paragraphs[0]
    
    if config and 'utilisateur' in config:
        utilisateur_info = config['utilisateur']
        p.text = f"Enerconseil SA\n{utilisateur_info['prenom']} {utilisateur_info['nom']}"
    else:
        # Valeur par défaut
        p.text = "Enerconseil SA\nJérôme Bonvin"
    
    set_font(p)


# -----------------------------------------------------
# 5️⃣ EXPORT PRINCIPAL
# -----------------------------------------------------
def exporter_vers_word(json_path, output_path=None):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Extraire la configuration si présente
    config = data.pop('_config', None)

    doc = Document()
    ajouter_entete(doc, data.get("numero_dossier"), config)

    ordre = [
        ("EN-VS", "EN-VS – Informations générales"),
        ("EN-VS-101a", "EN-VS-101a – Solution standard"),
        ("EN-VS-101b", "EN-VS-101b – Valeur limite EHWLK"),
        ("EN-VS-102a", "EN-VS-102a – Enveloppe thermique et ventilation (simplifié)"),
        ("EN-VS-102b", "EN-VS-102b – Besoins de chaleur et enveloppe (détaillé)"),
        ("EN-VS-103", "EN-VS-103 – Chauffage et eau chaude sanitaire"),
        ("EN-VS-104", "EN-VS-104 – Production propre d'électricité"),
        ("EN-VS-105", "EN-VS-105 – Ventilation"),
        ("EN-VS-110", "EN-VS-110 – Rafraîchissement et climatisation"),
    ]

    for form_id, titre in ordre:
        if form_id in data:
            info(f"Ajout du formulaire {form_id}")
            creer_tableau_formulaire(doc, titre, data[form_id], form_id)

    ajouter_pied_de_page(doc, config)

    if output_path is None:
        output_path = json_path.replace(".json", "_rapport_conformite.docx")

    try:
        doc.save(output_path)
        success(f"Document Word créé : {output_path}")
    except PermissionError:
        import time
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_path = f"{output_path.replace('.docx', '')}_{timestamp}.docx"
        doc.save(output_path)
        warning(f"Fichier Word ouvert, enregistré sous {output_path}")

    return output_path


# -----------------------------------------------------
# 6️⃣ MODE CLI
# -----------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Exporter un fichier JSON d'extraction vers Word (format conformité)")
    parser.add_argument("json_path", help="Chemin vers le JSON d'extraction")
    parser.add_argument("--output", "-o", help="Nom du fichier Word de sortie")
    args = parser.parse_args()

    if not os.path.exists(args.json_path):
        error(f"Fichier JSON non trouvé : {args.json_path}")
        return

    exporter_vers_word(args.json_path, args.output)


if __name__ == "__main__":
    main()
