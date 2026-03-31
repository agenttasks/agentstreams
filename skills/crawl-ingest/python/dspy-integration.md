# DSPy Integration with Claude

## Setup

```python
import dspy

# Configure Claude as the language model
lm = dspy.LM('anthropic/claude-sonnet-4-6')
dspy.configure(lm=lm)
```

## Signatures for Web Extraction

### Simple Extraction

```python
class ExtractProduct(dspy.Signature):
    """Extract product information from a web page."""
    page_html: str = dspy.InputField(desc='Raw HTML of a product page')
    product_name: str = dspy.OutputField(desc='Product name')
    price: float = dspy.OutputField(desc='Price in USD')
    description: str = dspy.OutputField(desc='Short product description')
    in_stock: bool = dspy.OutputField(desc='Whether the product is in stock')
```

### Classification

```python
class ClassifyPage(dspy.Signature):
    """Classify a web page into content categories."""
    url: str = dspy.InputField(desc='Page URL')
    title: str = dspy.InputField(desc='Page title')
    text_snippet: str = dspy.InputField(desc='First 1000 chars of page text')
    category: str = dspy.OutputField(desc='One of: product, article, listing, login, error, other')
    confidence: float = dspy.OutputField(desc='Confidence score 0-1')
```

### Multi-Entity Extraction

```python
class ExtractEntities(dspy.Signature):
    """Extract all named entities from article text."""
    article_text: str = dspy.InputField(desc='Article body text')
    people: list[str] = dspy.OutputField(desc='Names of people mentioned')
    organizations: list[str] = dspy.OutputField(desc='Organization names')
    locations: list[str] = dspy.OutputField(desc='Location names')
    key_facts: list[str] = dspy.OutputField(desc='Key factual claims')
```

## Modules

```python
# Simple prediction
extractor = dspy.Predict(ExtractProduct)

# Chain of thought (better accuracy, more tokens)
extractor = dspy.ChainOfThought(ExtractProduct)

# ReAct (reasoning + action — for complex multi-step extraction)
extractor = dspy.ReAct(ExtractProduct, tools=[search_tool, validate_tool])

# Program of Thought (generates code to solve the problem)
extractor = dspy.ProgramOfThought(ExtractProduct)
```

## Optimization

### BootstrapFewShot (simple, fast)

```python
# 1. Prepare labeled examples
trainset = [
    dspy.Example(
        page_html='<html>...<h1>Widget A</h1><span class="price">$29.99</span>...',
        product_name='Widget A',
        price=29.99,
        description='A useful widget',
        in_stock=True,
    ).with_inputs('page_html'),
    # ... 10-50 more examples
]

# 2. Define metric
def extraction_accuracy(example, prediction, trace=None):
    name_match = example.product_name.lower() in prediction.product_name.lower()
    price_match = abs(example.price - prediction.price) < 0.01
    return name_match and price_match

# 3. Optimize
optimizer = dspy.BootstrapFewShot(
    metric=extraction_accuracy,
    max_bootstrapped_demos=4,
    max_labeled_demos=8,
)
optimized = optimizer.compile(extractor, trainset=trainset)

# 4. Use optimized module
result = optimized(page_html=new_page_html)
```

### MIPROv2 (advanced, auto-generates instructions)

```python
optimizer = dspy.MIPROv2(
    metric=extraction_accuracy,
    num_threads=4,
    num_candidates=10,
)
optimized = optimizer.compile(
    extractor,
    trainset=trainset,
    max_bootstrapped_demos=4,
    max_labeled_demos=8,
    requires_permission_to_run=False,
)
```

## Integration with Scrapy Pipeline

```python
# pipelines.py
import dspy

class DSPyExtractionPipeline:
    def open_spider(self, spider):
        lm = dspy.LM('anthropic/claude-sonnet-4-6')
        dspy.configure(lm=lm)

        # Load pre-optimized module
        self.extractor = dspy.ChainOfThought(ExtractProduct)
        # Optionally load saved optimized state:
        # self.extractor.load('optimized_extractor.json')

    def process_item(self, item, spider):
        result = self.extractor(page_html=item.get('html', '')[:30000])
        item['product_name'] = result.product_name
        item['price'] = result.price
        item['description'] = result.description
        return item
```

## Saving and Loading Optimized Modules

```python
# Save after optimization
optimized.save('optimized_extractor.json')

# Load in production
loaded = dspy.ChainOfThought(ExtractProduct)
loaded.load('optimized_extractor.json')
result = loaded(page_html=html)
```
