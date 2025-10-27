# utils.py
import os
from docx.shared import Pt, RGBColor
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

# Tentative d’import de rich (facultatif)
try:
    from rich import print
except ImportError:
    # Fallback si Rich non installé
    def print(*args, **kwargs):
        __builtins__['print'](*args, **kwargs)

# ------------------------------
# 📄 Mise en forme Word
# ------------------------------
def set_font(paragraph, bold=False, size=10, color=(0, 0, 0)):
    """Applique le style Arial 10 (ou autre) à un paragraphe."""
    for run in paragraph.runs:
        run.font.name = 'Arial'
        run.font.size = Pt(size)
        run.bold = bold
        if color:
            r, g, b = color
            run.font.color.rgb = RGBColor(r, g, b)


def remove_table_borders(table):
    """Supprime toutes les bordures d'un tableau Word (compatible python-docx)."""
    tbl = table._element

    # Récupérer ou créer le nœud <w:tblPr>
    tblPr = tbl.find(qn('w:tblPr'))
    if tblPr is None:
        tblPr = OxmlElement('w:tblPr')
        tbl.insert(0, tblPr)

    # Supprimer ou créer la section <w:tblBorders>
    tblBorders = tblPr.find(qn('w:tblBorders'))
    if tblBorders is not None:
        tblPr.remove(tblBorders)

    tblBorders = OxmlElement('w:tblBorders')
    for border_name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        border = OxmlElement(f'w:{border_name}')
        border.set(qn('w:val'), 'none')
        border.set(qn('w:sz'), '0')
        border.set(qn('w:space'), '0')
        border.set(qn('w:color'), 'auto')
        tblBorders.append(border)

    tblPr.append(tblBorders)


def set_table_header_gray(cell):
    """Applique un fond gris clair à une cellule d’en-tête."""
    shading_elm = parse_xml(r'<w:shd {} w:fill="D3D3D3"/>'.format(nsdecls('w')))
    cell._element.get_or_add_tcPr().append(shading_elm)


# ------------------------------
# 🧠 Logs colorés (Rich ou fallback)
# ------------------------------
def info(msg): print(f"[cyan]ℹ️  {msg}[/cyan]")
def success(msg): print(f"[green]✅ {msg}[/green]")
def warning(msg): print(f"[yellow]⚠️ {msg}[/yellow]")
def error(msg): print(f"[red]❌ {msg}[/red]")


# ------------------------------
# 🔐 Vérification environnement
# ------------------------------
def check_env_var(name):
    """Vérifie la présence d’une variable d’environnement et avertit si absente."""
    val = os.getenv(name)
    if not val:
        warning(f"Variable d'environnement manquante : {name}")
    return val
