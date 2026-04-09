"""Layer 3: knowledge-work-prompts — Prompt engineering layer.

Maps knowledge-work plugin skills to prompt templates, enabling
systematic prompt construction, A/B variant testing, and prompt-to-
circuit correlation analysis.

Bridges:
    vendors/knowledge-work-plugins → SKILL.md files as prompt templates
    Layer 2 (tracers)              → Prompts traced to understand circuits
    Layer 4 (tasks)                → Tasks select prompts from the registry
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).parent.parent.parent
PLUGINS_ROOT = PROJECT_ROOT / "vendors" / "knowledge-work-plugins"


@dataclass
class PromptTemplate:
    """A prompt template derived from a knowledge-work plugin skill.

    Each template corresponds to a SKILL.md and supports variable
    interpolation, variant generation for A/B testing, and metadata
    for circuit tracing correlation.
    """

    name: str
    plugin_category: str
    skill_name: str
    system_prompt: str = ""
    user_template: str = ""
    variables: list[str] = field(default_factory=list)
    variant: str = "default"  # A/B variant identifier
    model: str = "claude-opus-4-6"

    def render(self, **kwargs: str) -> str:
        """Interpolate variables into the user template."""
        result = self.user_template
        for key, value in kwargs.items():
            result = result.replace(f"{{{{{key}}}}}", value)
        return result

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "plugin_category": self.plugin_category,
            "skill_name": self.skill_name,
            "variant": self.variant,
            "model": self.model,
            "variables": self.variables,
        }


class PromptRegistry:
    """Registry of prompt templates indexed by plugin category and skill.

    Loads templates from vendored SKILL.md files and supports
    variant management for A/B testing.
    """

    def __init__(self) -> None:
        self._templates: dict[str, dict[str, list[PromptTemplate]]] = {}

    def register(self, template: PromptTemplate) -> None:
        """Add a template to the registry."""
        cat = template.plugin_category
        skill = template.skill_name
        self._templates.setdefault(cat, {}).setdefault(skill, []).append(template)

    def get(
        self, plugin_category: str, skill_name: str, variant: str = "default"
    ) -> PromptTemplate | None:
        """Look up a specific template by category, skill, and variant."""
        templates = self._templates.get(plugin_category, {}).get(skill_name, [])
        for t in templates:
            if t.variant == variant:
                return t
        return templates[0] if templates else None

    def variants(self, plugin_category: str, skill_name: str) -> list[str]:
        """List available variants for a skill."""
        templates = self._templates.get(plugin_category, {}).get(skill_name, [])
        return [t.variant for t in templates]

    def categories(self) -> list[str]:
        """List all registered plugin categories."""
        return list(self._templates.keys())

    def skills(self, plugin_category: str) -> list[str]:
        """List all skills in a category."""
        return list(self._templates.get(plugin_category, {}).keys())

    @classmethod
    def from_plugins(cls, plugins_root: Path | None = None) -> PromptRegistry:
        """Build registry from vendored knowledge-work-plugins.

        Scans each plugin directory for SKILL.md files and creates
        default templates from their content.
        """
        root = plugins_root or PLUGINS_ROOT
        registry = cls()

        if not root.exists():
            return registry

        for plugin_dir in sorted(root.iterdir()):
            if not plugin_dir.is_dir() or plugin_dir.name.startswith("."):
                continue

            skills_dir = plugin_dir / "skills"
            if not skills_dir.exists():
                continue

            for skill_dir in sorted(skills_dir.iterdir()):
                if not skill_dir.is_dir():
                    continue

                skill_md = skill_dir / "SKILL.md"
                if not skill_md.exists():
                    continue

                content = skill_md.read_text(errors="replace")

                # Extract description from YAML frontmatter
                description = ""
                if content.startswith("---"):
                    end = content.find("---", 3)
                    if end != -1:
                        frontmatter = content[3:end]
                        for line in frontmatter.split("\n"):
                            if line.strip().startswith("description:"):
                                description = line.split(":", 1)[1].strip().strip("\"'")
                                break

                template = PromptTemplate(
                    name=f"{plugin_dir.name}/{skill_dir.name}",
                    plugin_category=plugin_dir.name,
                    skill_name=skill_dir.name,
                    system_prompt=description,
                    user_template=content,
                )
                registry.register(template)

        return registry
