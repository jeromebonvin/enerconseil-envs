# 🔴 FONCTIONNALITÉ : ALERTE ROUGE AUTOMATIQUE

## Description
Le script vérifie automatiquement si les valeurs U des éléments d'enveloppe respectent les limites réglementaires.

## Comportement

### ✅ Cas conforme (U projet ≤ U limite)
La ligne reste **blanche** avec texte noir.

**Exemple :**
```
Élément: Mur extérieur
U projet: 0.15 W/m²K
U limite: 0.20 W/m²K
→ LIGNE BLANCHE ✓
```

### 🔴 Cas NON conforme (U projet > U limite)
La ligne devient **ROUGE** (#FF0000) avec texte blanc pour une visibilité maximale.

**Exemple :**
```
Élément: Fenêtre séjour
U projet: 1.5 W/m²K
U limite: 1.0 W/m²K
→ LIGNE ROUGE ⚠️
```

## Éléments vérifiés

### 1. Éléments OPAQUES
- Murs extérieurs
- Toits
- Plafonds
- Sols
- Dalles
- Caissons de store

**Comparaison :** `valeur_u` vs `valeur_u_limite`

### 2. Éléments VITRÉS
- Fenêtres
- Portes-fenêtres
- Velux
- Portes
- Baies vitrées

**Comparaison :** `valeur_u_fenetre` vs `valeur_u_limite`

## Code de vérification

```python
# Pour éléments opaques
if float(valeur_u) > float(valeur_u_limite):
    # Mettre ligne en rouge + texte blanc
    
# Pour éléments vitrés
if float(valeur_u_fenetre) > float(valeur_u_limite):
    # Mettre ligne en rouge + texte blanc
```

## Avantages

✅ **Détection automatique** des non-conformités
✅ **Visibilité immédiate** dans le document Word
✅ **Pas d'intervention manuelle** requise
✅ **Alerte visuelle forte** (rouge + blanc)
✅ **Conformité réglementaire** facilitée

## Exemple de tableau généré

```
┌─────────────────┬──────────────────┬─────────────┬──────────────┐
│ Élément         │ Construction     │ U projet    │ U limite     │
├─────────────────┼──────────────────┼─────────────┼──────────────┤
│ Mur extérieur   │ 20 cm laine...   │ 0.15        │ 0.20         │ ← Blanc
├─────────────────┼──────────────────┼─────────────┼──────────────┤
│ Fenêtre séjour  │ Double vitrage...│ 1.5         │ 1.0          │ ← ROUGE ⚠️
├─────────────────┼──────────────────┼─────────────┼──────────────┤
│ Toit            │ 30 cm laine...   │ 0.12        │ 0.15         │ ← Blanc
└─────────────────┴──────────────────┴─────────────┴──────────────┘
```

## Gestion des erreurs

- Si valeur_u ou valeur_u_limite est `null` → Pas de vérification
- Si conversion en float impossible → Pas de vérification
- Le script continue sans erreur même en cas de données manquantes

## Notes techniques

- Couleur rouge : #FF0000
- Texte blanc : RGB(255, 255, 255)
- Format Word : Shading XML avec `w:fill`
- Police maintenue : Arial 10pt

---

✅ **Fonctionnalité testée et opérationnelle**
