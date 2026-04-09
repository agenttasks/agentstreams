"""Layer 2: knowledge-work-tracers — Circuit tracing and attribution.

Bridges vendors/circuit-tracer to knowledge-work tasks. Given a prompt
and model, traces which features activate and how they causally influence
the output — producing a Circuit that can be analyzed, compared, and
used to understand model behavior on knowledge-work tasks.

Bridges:
    vendors/circuit-tracer → ReplacementModel, attribute(), Graph, prune_graph()
    Layer 1 (circuits)     → Circuit, FeatureNode, CircuitEdge
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

from src.knowledge_work.circuits import (
    Circuit,
    CircuitEdge,
    FeatureNode,
    FeatureType,
)

PROJECT_ROOT = Path(__file__).parent.parent.parent
CIRCUIT_TRACER_ROOT = PROJECT_ROOT / "vendors" / "circuit-tracer"


class TracerBackend(Enum):
    """Which circuit-tracer backend to use."""

    TRANSFORMERLENS = "transformerlens"
    NNSIGHT = "nnsight"


@dataclass
class TracerConfig:
    """Configuration for a circuit tracing run.

    Controls model loading, transcoder selection, attribution parameters,
    and pruning thresholds.
    """

    # Model
    model_name: str = "google/gemma-2-2b"
    backend: TracerBackend = TracerBackend.TRANSFORMERLENS
    device: str = "cpu"
    dtype: str = "float32"

    # Transcoder
    transcoder_name: str = ""  # HuggingFace transcoder path
    use_clt: bool = False  # Use cross-layer transcoders if available

    # Attribution
    max_n_logits: int = 10
    batch_size: int = 1

    # Pruning
    node_threshold: float = 0.8
    edge_threshold: float = 0.98

    # Knowledge-work context
    plugin_category: str = ""
    skill_name: str = ""


@dataclass
class TracerResult:
    """Result of a circuit tracing run.

    Contains the traced circuit, raw graph data, quality metrics,
    and the prompt that was traced.
    """

    circuit: Circuit
    prompt: str = ""
    target_token: str = ""
    replacement_score: float = 0.0
    completeness_score: float = 0.0
    total_features: int = 0
    pruned_features: int = 0
    config: TracerConfig = field(default_factory=TracerConfig)

    def to_dict(self) -> dict[str, Any]:
        return {
            "prompt": self.prompt,
            "target_token": self.target_token,
            "replacement_score": self.replacement_score,
            "completeness_score": self.completeness_score,
            "total_features": self.total_features,
            "pruned_features": self.pruned_features,
            "circuit": self.circuit.to_dict(),
        }


def _classify_feature(layer: int, total_layers: int) -> FeatureType:
    """Heuristic classification of a feature by its layer position.

    Early layers → input processing, middle → reasoning, late → output.
    """
    fraction = layer / max(total_layers - 1, 1)
    if fraction < 0.15:
        return FeatureType.INPUT
    elif fraction < 0.4:
        return FeatureType.DOMAIN
    elif fraction < 0.7:
        return FeatureType.REASONING
    elif fraction < 0.85:
        return FeatureType.STYLE
    else:
        return FeatureType.OUTPUT


def trace_circuit(prompt: str, config: TracerConfig | None = None) -> TracerResult:
    """Trace the circuit activated by a prompt.

    This is the main entry point for Layer 2. It:
    1. Loads the model and transcoders via circuit-tracer
    2. Runs attribution to build the full feature graph
    3. Prunes to significant features
    4. Wraps the result as a Circuit (Layer 1)

    Requires circuit-tracer dependencies (torch, transformer-lens).
    Falls back to a stub result if dependencies aren't available.
    """
    if config is None:
        config = TracerConfig()

    try:
        import sys

        sys.path.insert(0, str(CIRCUIT_TRACER_ROOT))
        from circuit_tracer import ReplacementModel, attribute
        from circuit_tracer.graph import compute_graph_scores, prune_graph
    except ImportError:
        # Dependencies not available — return stub for type-checking/testing
        circuit = Circuit(
            name=f"stub-{config.skill_name or 'unknown'}",
            plugin_category=config.plugin_category,
            skill_name=config.skill_name,
        )
        return TracerResult(
            circuit=circuit,
            prompt=prompt,
            config=config,
        )

    # Load model + transcoders
    model = ReplacementModel.from_pretrained(
        config.model_name,
        config.transcoder_name or None,
        backend=config.backend.value,
        device=config.device,
        dtype=config.dtype,
    )

    # Run attribution
    graph = attribute(
        prompt,
        model,
        max_n_logits=config.max_n_logits,
        batch_size=config.batch_size,
    )

    # Compute quality metrics
    replacement_score, completeness_score = compute_graph_scores(graph)

    # Prune
    prune_result = prune_graph(
        graph,
        node_threshold=config.node_threshold,
        edge_threshold=config.edge_threshold,
    )
    pruned_graph = prune_result.graph

    # Total layers in the model (for feature classification heuristic)
    total_layers = getattr(model, "cfg", None)
    total_layers = total_layers.n_layers if total_layers else 26  # Gemma-2 default

    # Convert to Layer 1 Circuit
    nodes = []
    node_map: dict[str, FeatureNode] = {}

    for feat in pruned_graph.active_features:
        node = FeatureNode(
            layer=feat.layer,
            position=feat.position,
            feature_idx=feat.feature_idx,
            activation=feat.activation,
            feature_type=_classify_feature(feat.layer, total_layers),
        )
        nodes.append(node)
        node_map[f"{feat.layer}:{feat.position}:{feat.feature_idx}"] = node

    edges = []
    adj = pruned_graph.adjacency_matrix
    if adj is not None:
        for i, src_feat in enumerate(pruned_graph.active_features):
            src_key = f"{src_feat.layer}:{src_feat.position}:{src_feat.feature_idx}"
            if src_key not in node_map:
                continue
            for j, tgt_feat in enumerate(pruned_graph.active_features):
                tgt_key = f"{tgt_feat.layer}:{tgt_feat.position}:{tgt_feat.feature_idx}"
                if tgt_key not in node_map:
                    continue
                weight = float(adj[i, j])
                if abs(weight) > 1e-6:
                    edges.append(
                        CircuitEdge(
                            source=node_map[src_key],
                            target=node_map[tgt_key],
                            weight=weight,
                        )
                    )

    circuit = Circuit(
        name=f"{config.plugin_category}-{config.skill_name}" if config.skill_name else prompt[:40],
        nodes=nodes,
        edges=edges,
        replacement_score=replacement_score,
        completeness_score=completeness_score,
        plugin_category=config.plugin_category,
        skill_name=config.skill_name,
    )

    return TracerResult(
        circuit=circuit,
        prompt=prompt,
        replacement_score=replacement_score,
        completeness_score=completeness_score,
        total_features=len(graph.active_features),
        pruned_features=len(nodes),
        config=config,
    )
