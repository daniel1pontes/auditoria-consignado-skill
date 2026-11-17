"""Extração literal com localização; não interpreta campos automaticamente."""
import csv
from pathlib import Path
import fitz
from openpyxl import load_workbook


def extract(path):
    p = Path(path)
    result = {"arquivo": p.name, "trechos": [], "avisos": []}
    suffix = p.suffix.lower()
    if suffix == ".pdf":
        with fitz.open(p) as doc:
            if doc.needs_pass:
                raise ValueError("PDF protegido por senha: desbloqueie-o localmente antes da análise")
            for page in doc:
                text = page.get_text().strip()
                if not text:
                    result["avisos"].append(f"Página {page.number + 1} sem texto extraível; pode necessitar OCR e revisão visual")
                else:
                    result["trechos"].append({"local": f"página {page.number + 1}", "texto": text})
    elif suffix == ".csv":
        with p.open(encoding="utf-8-sig", newline="") as f:
            for n, row in enumerate(csv.reader(f), 1):
                result["trechos"].append({"local": f"linha {n}", "texto": " | ".join(row)})
    elif suffix == ".xlsx":
        wb = load_workbook(p, read_only=True, data_only=False)
        try:
            for sheet in wb:
                for row in sheet.iter_rows():
                    for cell in row:
                        if cell.value is not None:
                            result["trechos"].append({"local": f"aba {sheet.title}, célula {cell.coordinate}", "texto": str(cell.value)})
        finally:
            wb.close()
    else:
        raise ValueError("Formato não suportado: use PDF, CSV ou XLSX")
    return result
