---
name: xlsx
description: "Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .csv, or .tsv file; create a new spreadsheet from scratch or from other data sources; or convert between tabular file formats. Trigger when the user references a spreadsheet file by name or path."
license: Proprietary. LICENSE.txt has complete terms
---

# XLSX Skill

## Important Requirements

- Use a consistent, professional font (e.g., Arial, Times New Roman)
- Every Excel model MUST be delivered with ZERO formula errors
- Always use Excel formulas instead of calculating values in Python and hardcoding them
- Preserve existing templates when updating them

## Financial Model Color Coding

- **Blue text** (0,0,255): Hardcoded inputs
- **Black text** (0,0,0): ALL formulas and calculations
- **Green text** (0,128,0): Links from other worksheets
- **Red text** (255,0,0): External links to other files
- **Yellow background** (255,255,0): Key assumptions

## Library Selection

- **pandas**: Data analysis, bulk operations, simple data export
- **openpyxl**: Complex formatting, formulas, Excel-specific features

## Workflow

1. Choose tool (pandas or openpyxl)
2. Create/Load workbook
3. Modify (data, formulas, formatting)
4. Save to file
5. Recalculate formulas: `python scripts/recalc.py output.xlsx`
6. Verify and fix any errors

## Scripts

- `scripts/recalc.py` - Recalculate formulas via LibreOffice
