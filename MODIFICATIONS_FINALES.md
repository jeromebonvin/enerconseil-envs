# MODIFICATIONS FINALES APPLIQUÉES ✅

## Version finale : export_word.py + utils.py

---

## 1. EN-TÊTE
✅ **Espace ajouté entre l'adresse de la commune et la date**
   - `space_after = Pt(12)` après l'adresse du destinataire

---

## 2. TABLEAUX D'ENVELOPPE

### Tableau fusionné (éléments opaques + vitrés)
✅ **En-têtes modifiés :**
   - "Valeur U projet (W/m²K)" au lieu de "Coeff. U projet"
   - "Valeur U limite (W/m²K)" au lieu de "Coeff. U SIA"

✅ **Largeurs des colonnes ajustées :**
   - Colonne 1 (Élément) : 3.5 cm
   - Colonne 2 (Construction) : 10 cm (largement augmenté)
   - Colonne 3 (U projet) : 1.75 cm
   - Colonne 4 (U limite) : 1.75 cm

✅ **Éléments vitrés intégrés dans le même tableau :**
   - Fenêtres/portes-fenêtres/velux :
     * Construction : "Double/Triple vitrage Ug = X.X W/m²K, g = xx, cadre performant Uf = xx W/mK, intercalaire à rupture thermique"
     * Détection automatique double/triple selon Ug (≤0.7 = triple)
   
   - Portes/portes de garage :
     * Construction : "Porte isolante à définir"
   
   - Colonnes U projet et U limite : utilisent U fenêtre et U limite

✅ **⚠️ ALERTE ROUGE AUTOMATIQUE :**
   - **Si U projet > U limite** → Toute la ligne passe en ROUGE avec texte blanc
   - Fonctionne pour les éléments opaques (murs, toits, sols) ET vitrés (fenêtres, portes)
   - Vérification automatique pour chaque élément

---

## 3. FORMULAIRE EN-VS
✅ **Ligne supprimée :** Type de construction
✅ **Texte modifié :** "Formulaires annexés" (au lieu de "Formulaires nécessaires ou annexes")

---

## 4. FORMULAIRE EN-VS-101a
✅ **Textes modifiés :**
   - "Rafraîchissement et/ou (dés)humidification"
   - "PAC réversible projetée"

✅ **Surlignage jaune** sur toute la ligne "Solution standard choisie"

---

## 5. FORMULAIRE EN-VS-102a
✅ **Textes simplifiés :**
   - "Concept de ventilation" (sans "Hygiène de l'air intérieur")
   - "Respect de la valeur g" (sans "Protection thermique été")
   - "Rafraîchissement" (sans "Protection thermique été")
   - "Valeurs U respectées par tous les éléments"
   - "Justificatif des ponts thermiques respecté"
   - "Enveloppe thermique complètement fermée"
   - "Tous les locaux chauffés à l'intérieur de l'enveloppe thermique"

---

## 6. FORMULAIRE EN-VS-103
✅ **Textes clarifiés :**
   - "Type de générateur de chaleur"
   - "Puissance thermique"
   - "Dispositif de comptage d'énergie"
   - "Émission de chaleur que dans locaux isolés"
   - "Température de départ de l'émetteur de chaleur"
   - "Régulation de température par local"
   - "Température ECS < 60°C"
   - "Système de mesure installé pour chauffage"
   - "Système de mesure installé pour ECS"

✅ **Unité ajoutée :** kW pour puissance thermique

---

## 7. FORMULAIRE EN-VS-104
✅ **Textes modifiés :**
   - "Puissance projetée"
   - "Puissance requise"
   - "Nombre de panneaux"
   - "Puissance unitaire des panneaux"

✅ **Unités ajoutées :**
   - **Wc** pour puissance unitaire des panneaux
   - **kW** pour puissances projetée/requise

---

## 8. FORMULAIRE EN-VS-110
✅ **Textes modifiés :**
   - "Surface nette de plancher rafraîchie"
   - "Total des puissances frigorifiques"
   - "Puissance électrique totale"
   - "Puissance spécifique"

✅ **Unités ajoutées :**
   - **m²** pour surface
   - **kW** pour puissances frigorifiques et électrique totale
   - **W/m²** (et non kW) pour puissance spécifique

---

## 9. SECTION PRÉAVIS
✅ **Encadrement vert** autour du tableau préavis
   - Couleur : #00B050 (vert)
   - Épaisseur : 12

✅ **Ligne vide ajoutée après le préavis**

---

## FICHIERS MODIFIÉS
1. `export_word.py` - Script principal
2. `utils.py` - Fonctions utilitaires (copié depuis uploads)

## UTILISATION
```bash
python export_word.py chemin/vers/fichier_extraction.json
```

Ou via main_with_word.py :
```bash
python main_with_word.py chemin/vers/fichier.pdf --word
```

---

✅ **TOUTES LES MODIFICATIONS SONT APPLIQUÉES ET TESTÉES**
