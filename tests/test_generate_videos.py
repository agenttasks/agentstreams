"""Tests for video generation pipeline with agentic prompt patterns."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from xml.etree import ElementTree

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "skills" / "video-generation" / "scripts"))

from generate_videos import (
    VideoTask,
    PromptVerdict,
    validate_prompt,
    render_task_notification,
)


class TestVideoTask:
    """Test XML task rendering."""

    def test_basic_xml(self):
        task = VideoTask(
            task_id="01",
            prompt="Drone shot of mountains",
            aspect_ratio="16:9",
            output_file="test.mp4",
        )
        xml = task.to_xml()
        assert '<video-task id="01"' in xml
        assert 'status="pending"' in xml
        assert "<prompt>" in xml
        assert 'aspect_ratio="16:9"' in xml

    def test_xml_parses(self):
        task = VideoTask(
            task_id="02",
            prompt="Tracking shot of surfer",
            aspect_ratio="9:16",
            output_file="tiktok.mp4",
            platform="tiktok",
            status="ready",
        )
        root = ElementTree.fromstring(task.to_xml())
        assert root.tag == "video-task"
        assert root.attrib["id"] == "02"
        assert root.attrib["status"] == "ready"

    def test_xml_with_error(self):
        task = VideoTask(
            task_id="03",
            prompt="Bad prompt",
            status="failed",
            error="Validation failed",
        )
        xml = task.to_xml()
        assert "<error>" in xml
        assert "Validation failed" in xml

    def test_xml_escaping(self):
        task = VideoTask(
            task_id="04",
            prompt='Test with "quotes" & <angle> brackets',
        )
        xml = task.to_xml()
        assert "&amp;" in xml
        assert "&lt;" in xml
        assert "&quot;" in xml

    def test_from_dict_youtube(self):
        task = VideoTask.from_dict({
            "prompt": "Drone shot of city",
            "aspect_ratio": "16:9",
            "output_file": "city.mp4",
        }, task_id="05")
        assert task.platform == "youtube"
        assert task.aspect_ratio == "16:9"

    def test_from_dict_tiktok(self):
        task = VideoTask.from_dict({
            "prompt": "Vertical tracking shot",
            "aspect_ratio": "9:16",
        }, task_id="06")
        assert task.platform == "tiktok"

    def test_from_dict_defaults(self):
        task = VideoTask.from_dict({"prompt": "Test"})
        assert task.model == "veo-3.1-lite"
        assert task.aspect_ratio == "16:9"


class TestPromptValidation:
    """Test adversarial prompt verification."""

    def test_good_prompt_passes(self):
        task = VideoTask(
            task_id="01",
            prompt="A cinematic sweeping drone shot of a futuristic city at sunset, highly detailed, 4K.",
            aspect_ratio="16:9",
        )
        verdict = validate_prompt(task)
        assert verdict.verdict == "PASS"
        assert all(c["result"] == "PASS" for c in verdict.checks)

    def test_too_short_fails(self):
        task = VideoTask(task_id="02", prompt="A city video.")
        verdict = validate_prompt(task)
        failed_checks = [c for c in verdict.checks if c["result"] == "FAIL"]
        assert any(c["name"] == "prompt-length" for c in failed_checks)

    def test_missing_camera_movement(self):
        task = VideoTask(
            task_id="03",
            prompt="A beautiful sunset over the ocean with warm golden light, cinematic, highly detailed.",
        )
        verdict = validate_prompt(task)
        failed_checks = [c for c in verdict.checks if c["result"] == "FAIL"]
        assert any(c["name"] == "camera-movement" for c in failed_checks)

    def test_missing_style_modifier(self):
        task = VideoTask(
            task_id="04",
            prompt="A drone shot of a mountain range at sunrise with natural lighting.",
        )
        verdict = validate_prompt(task)
        failed_checks = [c for c in verdict.checks if c["result"] == "FAIL"]
        assert any(c["name"] == "style-modifier" for c in failed_checks)

    def test_multi_scene_fails(self):
        task = VideoTask(
            task_id="05",
            prompt="A cinematic drone shot of a city then tracking shot of a car, 4K.",
        )
        verdict = validate_prompt(task)
        failed_checks = [c for c in verdict.checks if c["result"] == "FAIL"]
        assert any(c["name"] == "single-scene" for c in failed_checks)

    def test_invalid_aspect_ratio(self):
        task = VideoTask(
            task_id="06",
            prompt="A cinematic drone shot of mountains, 4K.",
            aspect_ratio="4:3",
        )
        verdict = validate_prompt(task)
        failed_checks = [c for c in verdict.checks if c["result"] == "FAIL"]
        assert any(c["name"] == "aspect-ratio" for c in failed_checks)

    def test_verdict_xml_renders(self):
        task = VideoTask(
            task_id="07",
            prompt="A cinematic drone shot of a city at sunset, highly detailed.",
            aspect_ratio="16:9",
        )
        verdict = validate_prompt(task)
        xml = verdict.to_xml()
        assert '<verification task_id="07">' in xml
        assert "<verdict>" in xml

    def test_partial_verdict_one_fail(self):
        task = VideoTask(
            task_id="08",
            prompt="A drone shot of mountains at sunrise with golden hour lighting.",
            aspect_ratio="16:9",
        )
        verdict = validate_prompt(task)
        # Has camera movement but may be missing style modifier
        assert verdict.verdict in ("PASS", "PARTIAL")


class TestTaskNotification:
    """Test coordinator-style task notifications."""

    def test_completed_notification(self):
        xml = render_task_notification("video-01", "completed", "Generated test.mp4")
        assert "<task-notification>" in xml
        assert "<task-id>video-01</task-id>" in xml
        assert "<status>completed</status>" in xml

    def test_failed_notification(self):
        xml = render_task_notification("video-02", "failed", "Quota exceeded", "Retry in 60s")
        assert "<status>failed</status>" in xml
        assert "<result>" in xml

    def test_notification_parses(self):
        xml = render_task_notification("video-03", "completed", "Done")
        root = ElementTree.fromstring(xml)
        assert root.tag == "task-notification"
        assert root.find("task-id").text == "video-03"


class TestCLI:
    """Test the generate_videos.py CLI."""

    SCRIPT = str(Path(__file__).parent.parent / "skills" / "video-generation" / "scripts" / "generate_videos.py")

    def _run(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, self.SCRIPT, *args],
            capture_output=True,
            text=True,
        )

    def test_validate_good_prompts(self, tmp_path):
        batch = [
            {"prompt": "A cinematic drone shot of mountains at sunrise, golden hour, 4K.", "aspect_ratio": "16:9"},
        ]
        batch_file = tmp_path / "good.json"
        batch_file.write_text(json.dumps(batch))
        result = self._run("--validate-prompts", str(batch_file))
        assert result.returncode == 0
        assert "<verdict>PASS</verdict>" in result.stdout

    def test_validate_bad_prompts(self, tmp_path):
        batch = [
            {"prompt": "video", "aspect_ratio": "4:3"},
        ]
        batch_file = tmp_path / "bad.json"
        batch_file.write_text(json.dumps(batch))
        result = self._run("--validate-prompts", str(batch_file))
        assert result.returncode == 1
        assert "FAIL" in result.stdout

    def test_generate_plan(self):
        result = self._run(
            "--prompt",
            "A cinematic drone shot of mountains, 4K, highly detailed.",
            "--aspect-ratio", "16:9",
        )
        assert result.returncode == 0
        assert "<video-generation-plan>" in result.stdout
        assert '<video-task id="01"' in result.stdout

    def test_no_args_shows_help(self):
        result = self._run()
        assert result.returncode == 1


class TestAgentManifest:
    """Test video-generator agent manifest."""

    def test_manifest_exists(self):
        path = Path(__file__).parent.parent / ".claude" / "agents" / "video-generator.md"
        assert path.exists()

    def test_manifest_has_frontmatter(self):
        path = Path(__file__).parent.parent / ".claude" / "agents" / "video-generator.md"
        content = path.read_text()
        assert content.startswith("---")
        assert "name: video-generator" in content
        assert "description:" in content
        assert "tools:" in content

    def test_shared_agentic_patterns_exists(self):
        path = Path(__file__).parent.parent / "skills" / "video-generation" / "shared" / "agentic-patterns.md"
        assert path.exists()
        assert path.stat().st_size > 100
