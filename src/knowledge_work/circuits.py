"""Layer 1: knowledge-work-circuits — Feature circuits and topology.

A circuit is a set of features across model layers that work together to
complete a knowledge-work task. This module provides the data structures
for representing circuits as attributed graphs, mapping them to plugin
skills, and reasoning about which model capabilities contribute to which
knowledge-work outcomes.

Bridges:
    vendors/circuit-tracer  → CircuitTopology, FeatureNode, attribution graphs
    vendors/knowledge-work-plugins → SkillCircuit maps circuits to plugin skills

Glossary:
    feature  — Interpretable unit from SAE/transcoder decomposition
    circuit  — Subgraph of features causally linked to a task output
    topology — The shape/structure of a circuit (depth, width, branching)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class FeatureType(Enum):
    """Classification of features by their role in knowledge-work circuits."""

    INPUT = "input"  # Token-level input features (text, code, data)
    DOMAIN = "domain"  # Domain knowledge features (finance, legal, medical)
    REASONING = "reasoning"  # Multi-step reasoning features
    STYLE = "style"  # Output style/format features (tone, structure)
    TOOL_USE = "tool_use"  # Tool selection and invocation features
    SAFETY = "safety"  # Safety/alignment features (refusal, guardrails)
    OUTPUT = "output"  # Final output generation features


@dataclass
class FeatureNode:
    """A single interpretable feature in a circuit.

    Maps to a transcoder feature from circuit-tracer's Graph.active_features.
    """

    layer: int
    position: int
    feature_idx: int
    activation: float = 0.0
    feature_type: FeatureType = FeatureType.REASONING
    label: str = ""
    description: str = ""

    @property
    def key(self) -> str:
        return f"L{self.layer}:P{self.position}:F{self.feature_idx}"


@dataclass
class CircuitEdge:
    """A causal link between two features in a circuit.

    The weight represents the direct effect of source on target,
    computed via attribution in the circuit-tracer.
    """

    source: FeatureNode
    target: FeatureNode
    weight: float = 0.0


@dataclass
class Circuit:
    """A subgraph of features causally linked to a knowledge-work task.

    A circuit captures the "how" of a model completing a task: which
    features fire, how they influence each other, and which ultimately
    drive the output logits.
    """

    name: str
    nodes: list[FeatureNode] = field(default_factory=list)
    edges: list[CircuitEdge] = field(default_factory=list)
    replacement_score: float = 0.0  # Fraction of influence through features
    completeness_score: float = 0.0  # Weighted non-error input fraction
    plugin_category: str = ""  # Maps to PluginCategory.value
    skill_name: str = ""  # Maps to a SKILL.md

    @property
    def depth(self) -> int:
        """Number of distinct layers spanned by this circuit."""
        if not self.nodes:
            return 0
        layers = {n.layer for n in self.nodes}
        return max(layers) - min(layers) + 1

    @property
    def width(self) -> int:
        """Maximum number of features active at any single layer."""
        if not self.nodes:
            return 0
        from collections import Counter

        layer_counts = Counter(n.layer for n in self.nodes)
        return max(layer_counts.values())

    @property
    def feature_types(self) -> dict[FeatureType, int]:
        """Count of features by type."""
        from collections import Counter

        return dict(Counter(n.feature_type for n in self.nodes))

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "depth": self.depth,
            "width": self.width,
            "node_count": len(self.nodes),
            "edge_count": len(self.edges),
            "replacement_score": self.replacement_score,
            "completeness_score": self.completeness_score,
            "plugin_category": self.plugin_category,
            "skill_name": self.skill_name,
            "feature_types": {k.value: v for k, v in self.feature_types.items()},
        }


@dataclass
class CircuitTopology:
    """Structural analysis of how circuits relate across knowledge-work domains.

    Captures which features are shared across tasks (common reasoning
    pathways) and which are task-specific (domain specialization).
    """

    circuits: list[Circuit] = field(default_factory=list)

    @property
    def shared_features(self) -> set[str]:
        """Features that appear in more than one circuit."""
        from collections import Counter

        all_keys = Counter()
        for circuit in self.circuits:
            for node in circuit.nodes:
                all_keys[node.key] += 1
        return {k for k, count in all_keys.items() if count > 1}

    @property
    def domain_specific_features(self) -> dict[str, set[str]]:
        """Features unique to each circuit (not shared with any other)."""
        shared = self.shared_features
        result = {}
        for circuit in self.circuits:
            unique = {n.key for n in circuit.nodes} - shared
            result[circuit.name] = unique
        return result

    def similarity(self, circuit_a: str, circuit_b: str) -> float:
        """Jaccard similarity between two circuits' feature sets."""
        a_nodes = set()
        b_nodes = set()
        for c in self.circuits:
            if c.name == circuit_a:
                a_nodes = {n.key for n in c.nodes}
            if c.name == circuit_b:
                b_nodes = {n.key for n in c.nodes}
        if not a_nodes or not b_nodes:
            return 0.0
        intersection = a_nodes & b_nodes
        union = a_nodes | b_nodes
        return len(intersection) / len(union) if union else 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "circuit_count": len(self.circuits),
            "total_features": sum(len(c.nodes) for c in self.circuits),
            "shared_feature_count": len(self.shared_features),
            "circuits": [c.to_dict() for c in self.circuits],
        }
