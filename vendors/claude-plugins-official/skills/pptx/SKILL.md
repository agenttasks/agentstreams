---
name: pptx
description: "Use this skill any time a .pptx file is involved in any way -- as input, output, or both. This includes: creating slide decks, pitch decks, or presentations; reading, parsing, or extracting text from any .pptx file; editing, modifying, or updating existing presentations; combining or splitting slide files; working with templates, layouts, speaker notes, or comments. Trigger whenever the user mentions deck, slides, presentation, or references a .pptx filename."
license: Proprietary. LICENSE.txt has complete terms
---

# PPTX Skill

## Quick Reference

| Task | Guide |
|------|-------|
| Read/analyze content | `python -m markitdown presentation.pptx` |
| Edit or create from template | Read editing.md |
| Create from scratch | Read pptxgenjs.md |

## Reading Content

```bash
python -m markitdown presentation.pptx    # Text extraction
python scripts/thumbnail.py presentation.pptx  # Visual overview
python scripts/office/unpack.py presentation.pptx unpacked/  # Raw XML
```

## Additional References

- `editing.md` - Editing workflow documentation
- `pptxgenjs.md` - Creating from scratch with PptxGenJS
- `scripts/` - Helper scripts (thumbnail.py, office/unpack.py, office/soffice.py)

## Design Guidance

Pick a bold, content-informed color palette. Dark backgrounds for title + conclusion slides, light for content. Commit to a visual motif. Every slide needs a visual element.

## Dependencies

- `pip install "markitdown[pptx]"` - Text extraction
- `pip install Pillow` - Thumbnail grids
- `npm install -g pptxgenjs` - Creating from scratch
- LibreOffice (`soffice`) - PDF conversion
- Poppler (`pdftoppm`) - PDF to images
