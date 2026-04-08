"""Tests for scripts/extract-patterns.py — taxonomy pattern extraction."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from importlib import import_module

mod = import_module("extract-patterns")
classify_page_type = mod.classify_page_type
extract_topics = mod.extract_topics
extract_api_surface = mod.extract_api_surface
detect_code_languages = mod.detect_code_languages
extract_sdk_patterns = mod.extract_sdk_patterns
extract_links = mod.extract_links
parse_taxonomy_pages = mod.parse_taxonomy_pages
extract_domain = mod.extract_domain
analyze_page = mod.analyze_page


class TestClassifyPageType:
    def test_blog_post(self):
        assert (
            classify_page_type(
                "https://anthropic.com/engineering/foo",
                "Published Nov 24, 2025\nSome blog content",
            )
            == "blog"
        )

    def test_reference_page(self):
        assert (
            classify_page_type(
                "https://platform.claude.com/docs/en/api-reference/messages",
                "Parameters\nReturns a type Message",
            )
            == "reference"
        )

    def test_tutorial_page(self):
        assert (
            classify_page_type(
                "https://code.claude.com/docs/en/quickstart",
                "quickstart guide step 1 step 2",
            )
            == "tutorial"
        )

    def test_guide_default(self):
        assert (
            classify_page_type(
                "https://example.com/something",
                "Just some generic content here",
            )
            == "guide"
        )

    def test_changelog(self):
        assert (
            classify_page_type(
                "https://example.com/changelog",
                "What's new in this release",
            )
            == "changelog"
        )


class TestExtractTopics:
    def test_tool_use(self):
        topics = extract_topics("This page covers tool use and function calling with Claude")
        assert "tool-use" in topics

    def test_mcp_and_agents(self):
        topics = extract_topics("MCP server for agents with sub-agent orchestration")
        assert "mcp" in topics
        assert "agents" in topics

    def test_max_topics(self):
        content = "tool use streaming models agents MCP evals prompting vision embeddings"
        topics = extract_topics(content, max_topics=3)
        assert len(topics) <= 3

    def test_empty_content(self):
        assert extract_topics("") == []

    def test_claude_code(self):
        topics = extract_topics("Claude Code CLI configuration")
        assert "claude-code" in topics


class TestExtractApiSurface:
    def test_model_ids(self):
        apis = extract_api_surface("Use claude-opus-4-6 or claude-sonnet-4-6")
        assert any("claude-opus-4-6" in a for a in apis)
        assert any("claude-sonnet-4-6" in a for a in apis)

    def test_mythos_model_id(self):
        apis = extract_api_surface("Use claude-mythos-preview for vulnerability detection")
        assert any("claude-mythos-preview" in a for a in apis)

    def test_rest_endpoints(self):
        apis = extract_api_surface("POST /v1/messages to create a message")
        assert any("/v1/messages" in a for a in apis)

    def test_client_methods(self):
        apis = extract_api_surface("Call client.messages.create with your parameters")
        assert any("client.messages.create" in a for a in apis)

    def test_empty(self):
        assert extract_api_surface("No API stuff here") == []


class TestDetectCodeLanguages:
    def test_python(self):
        langs = detect_code_languages("import anthropic\nclient = anthropic.Anthropic()")
        assert "python" in langs

    def test_typescript(self):
        langs = detect_code_languages('import Anthropic from "@anthropic-ai/sdk"')
        assert "typescript" in langs

    def test_curl(self):
        langs = detect_code_languages("curl -X POST https://api.anthropic.com/v1/messages")
        assert "curl" in langs

    def test_multiple(self):
        langs = detect_code_languages("python typescript javascript examples")
        assert len(langs) >= 3

    def test_empty(self):
        assert detect_code_languages("no code here") == []


class TestExtractSdkPatterns:
    def test_python_constructor(self):
        patterns = extract_sdk_patterns("client = anthropic.Anthropic()")
        assert "anthropic.Anthropic()" in patterns

    def test_typescript_constructor(self):
        patterns = extract_sdk_patterns("const client = new Anthropic()")
        assert "new Anthropic()" in patterns

    def test_messages_create(self):
        patterns = extract_sdk_patterns("response = client.messages.create")
        assert "client.messages.create" in patterns


class TestExtractLinks:
    def test_same_domain(self):
        links = extract_links(
            "See https://code.claude.com/docs/en/tools for more",
            "code.claude.com",
        )
        assert any("code.claude.com" in link for link in links)

    def test_cross_domain_docs(self):
        links = extract_links(
            "See https://platform.claude.com/docs/en/messages",
            "code.claude.com",
        )
        assert any("platform.claude.com" in link for link in links)

    def test_ignores_external(self):
        links = extract_links(
            "Visit https://github.com/anthropics/sdk",
            "code.claude.com",
        )
        assert len(links) == 0


class TestParseTaxonomyPages:
    def test_parses_pages(self):
        text = """---
source: https://example.com/sitemap.xml
domain: example.com
---

# Taxonomy

## Pages

### page-one

URL: https://example.com/page-one
Hash: abc123

```
Hello world content here
```

### page-two

URL: https://example.com/page-two
Hash: def456

```
Second page content
```
"""
        pages = parse_taxonomy_pages(text)
        assert len(pages) == 2
        assert pages[0]["slug"] == "page-one"
        assert pages[0]["url"] == "https://example.com/page-one"
        assert "Hello world" in pages[0]["content"]

    def test_empty_taxonomy(self):
        assert parse_taxonomy_pages("# Empty\n\nNo pages here") == []


class TestExtractDomain:
    def test_extracts_domain(self):
        text = "---\nsource: x\ndomain: code.claude.com\n---"
        assert extract_domain(text) == "code.claude.com"

    def test_missing_domain(self):
        assert extract_domain("no frontmatter") == ""


class TestAnalyzePage:
    def test_full_analysis(self):
        page = {
            "slug": "tool-use",
            "url": "https://platform.claude.com/docs/en/tool-use",
            "content": "Tool use guide for Claude. import anthropic\nclient.messages.create with claude-sonnet-4-6",
        }
        result = analyze_page(page, "platform.claude.com")
        assert result["url"] == page["url"]
        assert result["slug"] == "tool-use"
        assert result["page_type"] in ("guide", "reference", "tutorial")
        assert "tool-use" in result["topics"]
        assert isinstance(result["api_surface"], list)
        assert isinstance(result["code_langs"], list)
