"""BL-011: Output style presets for non-engineering domains.

Pre-built output styles that adapt Claude Code for knowledge-work domains
beyond software engineering (code.claude.com/docs/en/output-styles.md).

Uses CLAUDE_CODE_OAUTH_TOKEN for auth (never ANTHROPIC_API_KEY).
"""

from __future__ import annotations

from dataclasses import dataclass

STYLES: dict[str, str] = {
    "legal": (
        "Write in precise legal language. Use defined terms consistently. "
        "Cite specific clauses and sections. Flag ambiguities explicitly. "
        "Structure output as: Summary > Analysis > Risks > Recommendations."
    ),
    "finance": (
        "Use standard financial terminology. Present numbers with proper formatting "
        "(thousands separators, 2 decimal places for currency). "
        "Structure output as: Executive Summary > Key Metrics > Analysis > Action Items."
    ),
    "sales": (
        "Write concisely and action-oriented. Lead with the ask or insight. "
        "Use bullet points for key facts. Include specific next steps with owners and dates. "
        "Tone: confident but not aggressive."
    ),
    "marketing": (
        "Match the brand voice specified in the brief. Lead with the audience benefit. "
        "Use active voice and concrete language. Avoid jargon unless the audience expects it. "
        "Include a clear call-to-action."
    ),
    "research": (
        "Structure as: Question > Methods > Findings > Limitations > Conclusion. "
        "Cite sources with author-date format. Distinguish correlation from causation. "
        "Flag confidence levels for each finding."
    ),
    "executive": (
        "Lead with the recommendation. Maximum 3 paragraphs for the summary. "
        "Use bullet points for supporting evidence. Include a decision matrix if "
        "there are multiple options. End with clear next steps."
    ),
    "technical": (
        "Use precise terminology. Include code examples where relevant. "
        "Structure as: Problem > Context > Solution > Trade-offs > Implementation. "
        "Link to relevant documentation."
    ),
    "hr": (
        "Write with empathy and precision. Use inclusive language. "
        "Structure feedback as: Observation > Impact > Suggestion. "
        "Distinguish policy requirements from recommendations."
    ),
    "support": (
        "Acknowledge the user's issue first. Use simple, jargon-free language. "
        "Provide step-by-step instructions with numbered lists. "
        "End with verification steps and escalation path if needed."
    ),
}


@dataclass
class OutputStyle:
    name: str
    instruction: str

    def as_system_prompt(self) -> str:
        return f"Output Style: {self.name}\n\n{self.instruction}"


def get_style(name: str) -> OutputStyle | None:
    instruction = STYLES.get(name)
    return OutputStyle(name=name, instruction=instruction) if instruction else None


def list_styles() -> list[str]:
    return list(STYLES.keys())
