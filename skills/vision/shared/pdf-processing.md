# PDF Processing Reference

## Overview

Claude can process PDFs through the files API (beta) or by converting pages to images. The files API preserves text fidelity; image conversion works for scanned documents.

## Files API (Beta)

### Upload

```
POST /v1/files
Content-Type: multipart/form-data

file: <pdf-binary>
```

Returns a `file_id` that can be referenced in messages.

### Reference in Message

```json
{
  "type": "file",
  "source": {
    "type": "file",
    "file_id": "file_abc123"
  }
}
```

## Image-Based PDF Processing

For scanned PDFs or when the files API is unavailable:

1. Convert PDF pages to images (e.g., using `pymupdf` or `pdf2image`)
2. Send images to Claude with analysis prompt
3. Process results

## Best Practices

1. **Use files API for text PDFs** — preserves formatting, lower token cost
2. **Use image conversion for scanned docs** — better OCR handling
3. **Process large PDFs in chunks** — split into sections of 10-20 pages
4. **Include page numbers** — helps Claude reference specific locations
5. **Be specific about what to extract** — "extract the table on page 3"
