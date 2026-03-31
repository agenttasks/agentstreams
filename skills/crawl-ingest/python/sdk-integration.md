# Python SDK Integration

## Core SDK Patterns

### Streaming

```python
import anthropic

client = anthropic.Anthropic()

with client.messages.stream(
    model='claude-opus-4-6',
    max_tokens=4096,
    thinking={'type': 'adaptive'},
    messages=[{'role': 'user', 'content': f'Extract data:\n{content}'}],
) as stream:
    for text in stream.text_stream:
        print(text, end='', flush=True)

response = stream.get_final_message()
```

### Structured Outputs (Pydantic)

```python
from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: float
    currency: str
    description: str
    in_stock: bool

response = client.messages.parse(
    model='claude-opus-4-6',
    max_tokens=1024,
    output_format=Product,
    messages=[{'role': 'user', 'content': f'Extract product:\n{html}'}],
)

product: Product = response.output
print(product.name, product.price)
```

### Batch API (50% discount)

```python
batch = client.messages.batches.create(
    requests=[
        {
            'custom_id': f'page-{i}',
            'params': {
                'model': 'claude-sonnet-4-6',
                'max_tokens': 1024,
                'messages': [{'role': 'user', 'content': f'Extract:\n{page}'}],
            },
        }
        for i, page in enumerate(pages)
    ]
)

# Poll for completion
import time
while True:
    result = client.messages.batches.retrieve(batch.id)
    if result.processing_status != 'in_progress':
        break
    time.sleep(10)
```

### Tool Use with @beta_tool

```python
from anthropic.beta import beta_tool

@beta_tool
def save_product(name: str, price: float, url: str) -> str:
    """Save an extracted product to the database."""
    db.insert('products', {'name': name, 'price': price, 'url': url})
    return f'Saved: {name}'

@beta_tool
def flag_for_review(url: str, reason: str) -> str:
    """Flag a page for manual review."""
    db.insert('review_queue', {'url': url, 'reason': reason})
    return f'Flagged: {url}'

# Tool runner handles the loop
result = client.beta.messages.run_tools(
    model='claude-opus-4-6',
    max_tokens=4096,
    tools=[save_product, flag_for_review],
    messages=[{'role': 'user', 'content': f'Process page:\n{html}'}],
)
```

## Agent SDK

```python
from claude_agent_sdk import query, ClaudeSDKClient

# One-shot query
async for message in query(
    prompt='Crawl example.com and extract all product data to ./data/',
    options={
        'model': 'claude-opus-4-6',
        'permission_mode': 'acceptEdits',
        'max_turns': 50,
    },
):
    if message.type == 'assistant':
        print(message.content)

# Full control with ClaudeSDKClient
async with ClaudeSDKClient() as sdk:
    result = await sdk.query(
        prompt='Analyze the crawl results in ./data/ and generate a summary report',
        tools=[custom_tool],
    )
```

## MCP Integration

```python
from mcp import Server, Tool

# Create MCP server for crawl tools
server = Server('crawl-tools')

@server.tool('crawl_url')
async def crawl_url(url: str) -> str:
    """Crawl a URL and return extracted content."""
    # ... crawl logic
    return extracted_content

@server.tool('check_bloom')
async def check_bloom(url: str) -> str:
    """Check if URL has been seen before."""
    return 'new' if url not in bloom else 'seen'
```

## Memory Tool Integration

```python
# Use SDK's BetaAbstractMemoryTool for crawl state persistence
from anthropic.beta import BetaAbstractMemoryTool

class CrawlMemory(BetaAbstractMemoryTool):
    def __init__(self, base_path='./data/memories'):
        super().__init__(base_path)

# Attach to messages for cross-session crawl state
```
