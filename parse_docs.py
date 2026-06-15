import os
import docx
import pypdf
import traceback
import sys

# Ensure stdout uses utf-8 encoding if possible, or ignore encoding errors
sys.stdout.reconfigure(encoding='utf-8')

def extract_docx_text(docx_path):
    print(f"=== Extracting text from {docx_path} ===")
    if not os.path.exists(docx_path):
        print("File not found")
        return
    try:
        doc = docx.Document(docx_path)
        texts = []
        for p in doc.paragraphs:
            texts.append(p.text)
        for t in doc.tables:
            for r in t.rows:
                for c in r.cells:
                    texts.append(c.text)
        full_text = "\n".join(texts)
        print(f"Read {len(texts)} elements.")
        
        # Write to txt file
        out_path = docx_path + ".txt"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(full_text)
        print(f"Saved to {out_path}")
    except Exception as e:
        print(f"Error docx: {e}")
        traceback.print_exc()

def extract_pdf_text(pdf_path):
    print(f"=== Extracting text from {pdf_path} ===")
    if not os.path.exists(pdf_path):
        print("File not found")
        return
    try:
        reader = pypdf.PdfReader(pdf_path)
        text = ""
        for i, page in enumerate(reader.pages):
            text += f"\n--- Page {i+1} ---\n"
            text += page.extract_text()
        
        print(f"Read {len(reader.pages)} pages. Total length: {len(text)} characters.")
        out_path = pdf_path + ".txt"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Saved to {out_path}")
    except Exception as e:
        print(f"Error pdf: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    extract_docx_text(r"e:\Bao Cao Ha Dung\Tuan6-Test Huong di ha dung\Project\conference-template-a4.docx")
    extract_docx_text(r"e:\Bao Cao Ha Dung\Tuan6-Test Huong di ha dung\Project\Latex.docx")
    extract_pdf_text(r"e:\Bao Cao Ha Dung\Tuan6-Test Huong di ha dung\Project\FAIR_2025_-_9435.pdf")
