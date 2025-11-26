import os
from pathlib import Path

from PIL import Image
from pix2tex.cli import LatexOCR
from latex2mathml.converter import convert as latex_to_mathml
from latex2mathml.exceptions import ExtraLeftOrMissingRightError

try:
    from pdf2image import convert_from_path
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

# For creating PDF containing MathML text
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Preformatted
from reportlab.lib.styles import getSampleStyleSheet

# OPTIONAL: hide annoying warnings
import warnings
warnings.filterwarnings("ignore")

# Initialize the OCR model once
ocr_model = LatexOCR()


def sanitize_latex(latex: str) -> str:
    """
    Clean up LaTeX so latex2mathml doesn't choke on it.
    - Remove \left and \right (they're just for bracket sizing)
    - Strip spaces
    """
    if not latex:
        return ""
    latex = latex.replace(r"\left", "")
    latex = latex.replace(r"\right", "")
    return latex.strip()


def _image_file_to_latex(image_path: str) -> str:
    """Convert a single image file to LaTeX using pix2tex."""
    img = Image.open(image_path).convert("RGB")
    latex = ocr_model(img)
    return latex


def _pdf_to_latex_list(pdf_path: str) -> list:
    """
    Convert each page of a PDF to LaTeX.
    Returns a list of LaTeX strings, one per page.
    """
    if not PDF_SUPPORT:
        raise RuntimeError(
            "pdf2image is not installed or Poppler is missing. "
            "Install with: pip install pdf2image and install Poppler."
        )

    pages = convert_from_path(pdf_path)
    latex_list = []
    for i, page_img in enumerate(pages, start=1):
        print(f"[INFO] Running OCR on page {i}...")
        latex = ocr_model(page_img)
        latex_list.append(latex)
    return latex_list


def file_to_mathml(path: str) -> str:
    """
    Main function:
    Input: path to image or PDF
    Output: MathML (string). For multi-page PDF, concatenates MathML blocks.
    """
    path_obj = Path(path)
    if not path_obj.exists():
        raise FileNotFoundError(f"File not found: {path}")

    ext = path_obj.suffix.lower()

    # ---------- Single image case ----------
    if ext in [".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".webp"]:
        latex = _image_file_to_latex(str(path_obj))
        clean_latex = sanitize_latex(latex)

        print("[DEBUG] LaTeX from image:")
        print(clean_latex)
        print("------------")

        mathml = latex_to_mathml(clean_latex)
        return mathml

    # ---------- PDF case ----------
    elif ext == ".pdf":
        latex_list = _pdf_to_latex_list(str(path_obj))
        mathml_blocks = []

        for idx, lx in enumerate(latex_list, start=1):
            clean_latex = sanitize_latex(lx)
            if not clean_latex:
                print(f"[WARN] Page {idx}: empty LaTeX, skipping.")
                continue

            try:
                mathml_page = latex_to_mathml(clean_latex)
                mathml_blocks.append(f"<!-- Page {idx} -->\n{mathml_page}")
            except ExtraLeftOrMissingRightError:
                print(f"[ERROR] Page {idx}: ExtraLeftOrMissingRightError – skipping this page.")
                print("[DEBUG] Problematic LaTeX:")
                print(clean_latex)
                print("------------")
            except Exception as e:
                print(f"[ERROR] Page {idx}: Unexpected error while converting to MathML: {e}")
                print("[DEBUG] LaTeX that caused error:")
                print(clean_latex)
                print("------------")

        if not mathml_blocks:
            raise RuntimeError("No pages could be converted to MathML.")

        combined = "<root>\n" + "\n\n".join(mathml_blocks) + "\n</root>"
        return combined

    else:
        raise ValueError(f"Unsupported file extension: {ext}")


def save_mathml_to_pdf(mathml_str: str, pdf_path: str) -> None:
    """
    Save the MathML string as plain text inside a PDF file.
    (The PDF will show the MathML code so you can view/copy it.)
    """
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    styles = getSampleStyleSheet()
    # 'Code' style is monospaced; good for markup
    pre = Preformatted(mathml_str, styles["Code"])
    doc.build([pre])


if __name__ == "__main__":
    # 🔹 CHANGE THIS TO YOUR FILE PATH (raw string with r"")
    input_path = r"C:\Users\USER\OneDrive\Desktop\pythonforml\11th JEE Main Part Test-01_Print 4.pdf"

    # Convert image/PDF -> MathML string
    mathml_output = file_to_mathml(input_path)

    # Print ONLY MathML to console
    print("\n===== MATHML OUTPUT =====\n")
    print(mathml_output)

    # Save MathML as .xml
    xml_path = "output_mathml.xml"
    with open(xml_path, "w", encoding="utf-8") as f:
        f.write(mathml_output)
    print(f"\n[INFO] MathML XML saved to: {xml_path}")

    # Save MathML as a PDF (code printed in PDF)
    pdf_path = "output_mathml.pdf"
    save_mathml_to_pdf(mathml_output, pdf_path)
    print(f"[INFO] MathML PDF saved to: {pdf_path}")
