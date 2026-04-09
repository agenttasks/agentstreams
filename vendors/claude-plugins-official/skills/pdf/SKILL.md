---
name: pdf
description: "Use this skill any time a PDF file is involved -- as input, output, or both. This includes: creating PDFs, reading or extracting text/tables from PDFs, editing existing PDFs, OCR for scanned documents, watermarking, merging/splitting, and form field operations. Trigger whenever the user mentions a .pdf filename or asks about PDF documents."
license: Proprietary. LICENSE.txt has complete terms
---

# PDF Skill

## Capabilities

- Create new PDFs (reportlab)
- Read and extract text with layout (pdfplumber)
- Merge and split PDFs (pypdf)
- OCR for scanned documents
- Watermarking and encryption
- Image extraction
- Form field operations

## Additional References

- `forms.md` - PDF form field operations
- `reference.md` - Detailed library reference
- `scripts/` - Helper scripts

## Key Libraries

- pypdf - Merging, splitting
- pdfplumber - Text extraction with layout, tables
- reportlab - PDF creation
- pdftotext, qpdf, pdftk - Command-line tools

## Important Notes

Never use Unicode subscript/superscript characters in ReportLab -- use XML markup tags instead.
