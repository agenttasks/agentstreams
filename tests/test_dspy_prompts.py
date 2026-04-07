"""Tests for src/dspy_prompts.py — DSPy structured extraction."""

from __future__ import annotations

import pytest

from src.dspy_prompts import (
    ALIGN_TO_ONTOLOGY,
    CLASSIFY_CONTENT,
    EXTRACT_API_PATTERNS,
    EXTRACT_ENTITIES,
    ChainOfThought,
    Field,
    Module,
    Pipeline,
    Prediction,
    Signature,
)


class TestField:
    def test_default_type_is_str(self):
        f = Field("name", "description")
        assert f.field_type == "str"
        assert f.required is True

    def test_custom_type(self):
        f = Field("items", "list of items", field_type="list", required=False)
        assert f.field_type == "list"
        assert f.required is False


class TestSignature:
    def test_to_xml_schema(self):
        sig = Signature(
            name="TestTask",
            doc="A test task",
            inputs=[Field("text", "Input text")],
            outputs=[Field("result", "Output result")],
        )
        xml = sig.to_xml_schema()
        assert '<task name="TestTask">' in xml
        assert '<field name="text"' in xml
        assert '<field name="result"' in xml
        assert "<inputs>" in xml
        assert "<outputs>" in xml

    def test_to_prompt_instructions(self):
        sig = Signature(
            name="ExtractData",
            doc="Extract data from text",
            inputs=[Field("content", "Source content")],
            outputs=[Field("entities", "Extracted entities", "list")],
        )
        instructions = sig.to_prompt_instructions()
        assert "## Task: ExtractData" in instructions
        assert "Extract data from text" in instructions
        assert "content (str)" in instructions
        assert "entities (list)" in instructions
        assert "respond as JSON" in instructions.lower() or "Required Outputs" in instructions


class TestPreBuiltSignatures:
    def test_extract_entities_signature(self):
        assert EXTRACT_ENTITIES.name == "ExtractEntities"
        assert len(EXTRACT_ENTITIES.inputs) == 3
        assert len(EXTRACT_ENTITIES.outputs) == 3
        input_names = {f.name for f in EXTRACT_ENTITIES.inputs}
        assert input_names == {"url", "content", "domain"}

    def test_classify_content_signature(self):
        assert CLASSIFY_CONTENT.name == "ClassifyContent"
        output_names = {f.name for f in CLASSIFY_CONTENT.outputs}
        assert "primary_category" in output_names
        assert "confidence" in output_names

    def test_extract_api_patterns_signature(self):
        assert EXTRACT_API_PATTERNS.name == "ExtractAPIPatterns"
        output_names = {f.name for f in EXTRACT_API_PATTERNS.outputs}
        assert "sdk_constructor" in output_names
        assert "auth_method" in output_names

    def test_align_to_ontology_signature(self):
        assert ALIGN_TO_ONTOLOGY.name == "AlignToOntology"
        input_names = {f.name for f in ALIGN_TO_ONTOLOGY.inputs}
        assert "ontology_classes" in input_names


class TestPrediction:
    def test_attribute_access(self):
        p = Prediction(outputs={"name": "test", "value": 42})
        assert p.name == "test"
        assert p.value == 42

    def test_missing_attribute_raises(self):
        p = Prediction(outputs={"name": "test"})
        with pytest.raises(AttributeError, match="No output field"):
            _ = p.missing


class TestModule:
    def test_build_messages(self):
        sig = Signature(
            name="Test",
            doc="Test task",
            inputs=[Field("text", "Input")],
            outputs=[Field("result", "Output")],
        )
        module = Module(sig)
        messages = module._build_messages({"text": "hello"})
        assert len(messages) == 1
        assert messages[0]["role"] == "user"
        assert "hello" in messages[0]["content"]

    def test_parse_json_output_clean(self):
        result = Module._parse_json_output('{"name": "test", "value": 42}')
        assert result == {"name": "test", "value": 42}

    def test_parse_json_output_with_fences(self):
        result = Module._parse_json_output('```json\n{"name": "test"}\n```')
        assert result == {"name": "test"}

    def test_parse_json_output_invalid(self):
        result = Module._parse_json_output("not json at all")
        assert "raw" in result


class TestChainOfThought:
    def test_adds_reasoning_instruction(self):
        sig = Signature(
            name="Test",
            doc="Test",
            inputs=[Field("text", "Input")],
            outputs=[Field("result", "Output")],
        )
        cot = ChainOfThought(sig)
        messages = cot._build_messages({"text": "hello"})
        assert "reasoning" in messages[0]["content"].lower()


class TestPipelineStructure:
    def test_pipeline_stores_modules(self):
        sig1 = Signature(name="A", doc="First", inputs=[], outputs=[])
        sig2 = Signature(name="B", doc="Second", inputs=[], outputs=[])
        p = Pipeline([Module(sig1), Module(sig2)])
        assert len(p.modules) == 2
