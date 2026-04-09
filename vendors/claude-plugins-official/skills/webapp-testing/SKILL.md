---
name: webapp-testing
description: Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs.
license: Complete terms in LICENSE.txt
---

# Web Application Testing

Test local web applications using native Python Playwright scripts.

## Helper Scripts

- `scripts/with_server.py` - Manages server lifecycle (supports multiple servers)

## Decision Tree

1. Static HTML? -> Read HTML file directly, write Playwright script
2. Dynamic webapp, server not running? -> Use `scripts/with_server.py`
3. Dynamic webapp, server running? -> Reconnaissance-then-action pattern

## Reconnaissance-Then-Action Pattern

1. Navigate and wait for networkidle
2. Take screenshot or inspect DOM
3. Identify selectors from rendered state
4. Execute actions with discovered selectors

## Examples

- `examples/element_discovery.py` - Discovering buttons, links, and inputs
- `examples/static_html_automation.py` - Using file:// URLs for local HTML
- `examples/console_logging.py` - Capturing console logs

## Best Practices

- Always wait for `page.wait_for_load_state('networkidle')` before inspection
- Use `sync_playwright()` for synchronous scripts
- Always close the browser when done
- Use descriptive selectors: `text=`, `role=`, CSS selectors, or IDs
