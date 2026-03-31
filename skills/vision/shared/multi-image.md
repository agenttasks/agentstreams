# Multi-Image Analysis Reference

## Overview

Claude can process up to 20 images in a single request. Images are referenced by position in the message content array.

## Use Cases

### Before/After Comparison

Send two images and ask Claude to identify differences:
- UI changes between versions
- Photo editing results
- Document revisions

### Visual A/B Testing

Compare design variants:
- Layout differences
- Color scheme impact
- Typography changes

### Sequential Analysis

Process a series of related images:
- Multi-page document scanning
- Step-by-step instructions with screenshots
- Progress photos over time

## Best Practices

1. **Order matters** — place images in logical sequence
2. **Reference by position** — "the first image", "image 3"
3. **Be specific** — tell Claude exactly what to compare
4. **Limit count** — more images = more tokens and slower processing
5. **Consistent format** — same resolution and format for comparison images
