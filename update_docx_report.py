import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
import shutil
from pathlib import Path

BASE_DIR = Path("d:/LAB/chuyen-de-tot-nghiep")
DOCX_PATH = BASE_DIR / "Báo Cáo Chuyên Đề.docx"
BACKUP_PATH = BASE_DIR / "Báo Cáo Chuyên Đề_backup.docx"

# 1. Make a backup
shutil.copyfile(DOCX_PATH, BACKUP_PATH)
print("Backup created at:", BACKUP_PATH)

doc = docx.Document(DOCX_PATH)

# Helper to format paragraph
def add_styled_p(doc, text, bold_prefix=None, italic=False, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.2
    p.paragraph_format.space_after = Pt(space_after)
    if bold_prefix:
        r_bold = p.add_run(bold_prefix)
        r_bold.bold = True
        r_bold.font.name = "Times New Roman"
        r_bold.font.size = Pt(13)
    r = p.add_run(text)
    r.italic = italic
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    return p

print("Loaded docx with paragraphs:", len(doc.paragraphs))
