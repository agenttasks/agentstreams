# Programmatic Prompts

## What Are Programmatic Prompts?

Programmatic prompts are prompts that are compiled, optimized, and executed by a framework rather than hand-written. Instead of crafting prompt strings manually, you define **typed input/output signatures** and let an optimizer find the best prompt formulation automatically.

## DSPy (Python — Primary)

DSPy 3.1.3 is the canonical framework. It works with Claude via:

```python
import dspy

# Configure Claude as the LM
lm = dspy.LM("anthropic/claude-sonnet-4-6")
dspy.configure(lm=lm)

# Define a signature (typed I/O)
class ExtractProduct(dspy.Signature):
    """Extract product information from a web page."""
    page_html: str = dspy.InputField(desc="Raw HTML of a product page")
    product_name: str = dspy.OutputField(desc="Product name")
    price: float = dspy.OutputField(desc="Price in USD")
    description: str = dspy.OutputField(desc="Short product description")

# Use a module
extractor = dspy.ChainOfThought(ExtractProduct)
result = extractor(page_html=html_content)
print(result.product_name, result.price)
```

### Key DSPy Concepts

| Concept | What it does |
|---------|-------------|
| **Signature** | Typed I/O spec — defines what goes in and what comes out |
| **Module** | Execution strategy — `Predict`, `ChainOfThought`, `ReAct`, `ProgramOfThought` |
| **Optimizer** | Auto-tunes prompts from examples — `BootstrapFewShot`, `MIPROv2`, `COPRO` |
| **Metric** | Evaluation function — returns True/False or 0-1 score |
| **Example** | Training data — input/output pairs for optimization |

### Optimization Workflow

```python
# 1. Define your metric
def extraction_accuracy(example, prediction, trace=None):
    return example.product_name.lower() == prediction.product_name.lower()

# 2. Prepare training examples
trainset = [
    dspy.Example(page_html="<html>...", product_name="Widget A", price=29.99),
    # ... more examples
]

# 3. Optimize
optimizer = dspy.MIPROv2(metric=extraction_accuracy, num_threads=4)
optimized_extractor = optimizer.compile(extractor, trainset=trainset)

# 4. Use the optimized module (prompt is now auto-tuned)
result = optimized_extractor(page_html=new_html)
```

## @ts-dspy/core (TypeScript)

TypeScript port with type-safe signatures:

```typescript
import { Predict, Signature, InputField, OutputField } from '@ts-dspy/core';

// Define signature with Zod-like types
const ExtractProduct = new Signature({
  pageHtml: InputField({ type: 'string', desc: 'Raw HTML' }),
  productName: OutputField({ type: 'string', desc: 'Product name' }),
  price: OutputField({ type: 'number', desc: 'Price in USD' }),
});

const extractor = new Predict(ExtractProduct);
const result = await extractor.forward({ pageHtml: html });
```

Note: `@ts-dspy/core` 0.4.2 has fewer optimizers than Python DSPy. For full optimization support, consider calling Python DSPy via subprocess or using `dspy.ts` 2.1.1 (claims MIPROv2 support).

## Java — No Direct Equivalent

Java has no DSPy equivalent. Closest approaches:

1. **LangChain4j** — prompt templates + RAG, but no automatic optimization
2. **Manual optimization** — implement BootstrapFewShot pattern manually:
   - Run extraction on labeled examples
   - Select best-performing examples as few-shot demonstrations
   - Embed into prompt template
3. **Python subprocess** — call DSPy from Java for the optimization step, export the optimized prompt, use it in Java

## When to Use Programmatic Prompts

| Scenario | Use Programmatic? |
|----------|------------------|
| Simple extraction with known schema | No — use structured outputs directly |
| Complex extraction with quality variance | Yes — optimize with BootstrapFewShot |
| Multi-step classification pipeline | Yes — use ChainOfThought + optimizer |
| One-off crawl, low volume | No — hand-write the prompt |
| Production crawl, high volume | Yes — optimized prompts save tokens and improve accuracy |

## Integration with Crawl Pipeline

```
Crawl → Extract HTML → DSPy Module → Structured Data → Store
                            ↑
                    Optimized prompt
                    (from training set)
```

Use the Anthropic Batch API (50% discount) for bulk extraction after optimization.
