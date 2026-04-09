#!/usr/bin/env python3
"""Generate human-readable architecture diagrams using mingrammer/diagrams.

Produces 4 PNG diagrams in diagrams/human/:
  1. system-overview.png    — Full system: orchestrator, agents, pipelines, data stores
  2. pipeline-flows.png     — All 8 pipeline step-by-step flows with gates
  3. 14-layer-stack.png     — The 14-layer knowledge-work abstraction
  4. agent-topology.png     — 25 agents grouped by model tier and domain

Requires: pip install diagrams (+ graphviz system package)
"""

from __future__ import annotations

import os
import sys

# diagrams library uses graphviz under the hood
from diagrams import Cluster, Diagram, Edge
from diagrams.custom import Custom
from diagrams.onprem.analytics import Spark
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import Kafka
from diagrams.programming.flowchart import (
    Action,
    Collate,
    Database,
    Decision,
    Document,
    MultipleDocuments,
    PredefinedProcess,
    StartEnd,
)
from diagrams.programming.framework import React
from diagrams.programming.language import Python, TypeScript

OUT_DIR = os.path.join(os.path.dirname(__file__), "human")


def diagram_1_system_overview():
    """Full system overview: orchestrator at center, agents, data stores, CLI."""
    with Diagram(
        "AgentStreams System Overview",
        filename=os.path.join(OUT_DIR, "system-overview"),
        outformat="png",
        show=False,
        direction="TB",
        graph_attr={
            "fontsize": "20",
            "bgcolor": "#0a0a0a",
            "fontcolor": "#c8ff00",
            "pad": "0.8",
            "dpi": "150",
        },
        node_attr={"fontcolor": "#e0e0e0", "color": "#333333"},
        edge_attr={"color": "#555555"},
    ):
        user = User("Developer\nCLI / Web")

        with Cluster(
            "Claude Code Harness",
            graph_attr={"bgcolor": "#111111", "fontcolor": "#c8ff00"},
        ):
            cli = Python("agentstreams CLI\n8 subcommands")
            webapp = React("Next.js Webapp\nagentcrawls.com")

        with Cluster(
            "Opus 4.6 Orchestrator",
            graph_attr={"bgcolor": "#0d1117", "fontcolor": "#c8ff00"},
        ):
            orch = Server("Orchestrator\n8 pipelines")
            gate = Decision("Safety Gates\nVERDICT / ALIGNMENT")

        with Cluster(
            "Safety Agents (Opus)",
            graph_attr={"bgcolor": "#1a0000", "fontcolor": "#ff6666"},
        ):
            sec = Server("security-auditor")
            align = Server("alignment-auditor")
            arch = Server("architecture-reviewer")

        with Cluster(
            "Codegen Agents (Sonnet)",
            graph_attr={"bgcolor": "#001a00", "fontcolor": "#66ff66"},
        ):
            codegen = Server("code-generator")
            testrun = Server("test-runner")
            hardener = Server("prompt-hardener")
            evalb = Server("eval-builder")

        with Cluster(
            "Screen (Haiku)",
            graph_attr={"bgcolor": "#00001a", "fontcolor": "#6666ff"},
        ):
            screen = Server("harmlessness-screen")

        with Cluster(
            "Knowledge Agents (17 Opus)",
            graph_attr={"bgcolor": "#0a0a1a", "fontcolor": "#aa88ff"},
        ):
            sales = Server("sales-agent")
            data = Server("data-analyst")
            compliance = Server("compliance-reviewer")
            eng = Server("engineering-agent")
            dots = Server("... 13 more")

        with Cluster(
            "Data Layer",
            graph_attr={"bgcolor": "#1a1a00", "fontcolor": "#ffff66"},
        ):
            neon = PostgreSQL("Neon Postgres\ncalm-paper-82059121")
            otel = Grafana("OTel Traces")

        with Cluster(
            "Vendors",
            graph_attr={"bgcolor": "#0a0a0a", "fontcolor": "#888888"},
        ):
            kwp = Document("knowledge-work-plugins\n17 plugins, 164 skills")
            ct = Document("circuit-tracer\nv0.4.1")
            sr = Document("safety-research\n18 repos")

        # Connections
        user >> Edge(color="#c8ff00") >> cli
        user >> Edge(color="#c8ff00") >> webapp
        cli >> Edge(color="#c8ff00", label="pipeline") >> orch
        webapp >> Edge(color="#c8ff00") >> neon

        orch >> Edge(color="#ff6666", label="audit") >> sec
        orch >> Edge(color="#ff6666") >> align
        orch >> Edge(color="#ff6666") >> arch

        orch >> Edge(color="#66ff66", label="generate") >> codegen
        orch >> Edge(color="#66ff66") >> testrun
        orch >> Edge(color="#66ff66") >> hardener
        orch >> Edge(color="#66ff66") >> evalb

        orch >> Edge(color="#6666ff", label="pre-screen") >> screen

        orch >> Edge(color="#aa88ff", label="domain") >> sales
        orch >> Edge(color="#aa88ff") >> data
        orch >> Edge(color="#aa88ff") >> compliance
        orch >> Edge(color="#aa88ff") >> eng
        orch >> Edge(color="#aa88ff") >> dots

        sec >> Edge(color="#ff6666", style="dashed") >> gate
        align >> Edge(color="#ff6666", style="dashed") >> gate
        gate >> Edge(color="#ffff66", label="persist") >> neon
        gate >> Edge(color="#ffff66") >> otel

        # Vendor references
        sales >> Edge(color="#555555", style="dotted") >> kwp
        sec >> Edge(color="#555555", style="dotted") >> sr
        codegen >> Edge(color="#555555", style="dotted") >> ct


def diagram_2_pipeline_flows():
    """All 8 pipeline flows showing step ordering and gates."""
    with Diagram(
        "Pipeline Flows (8 Pipelines)",
        filename=os.path.join(OUT_DIR, "pipeline-flows"),
        outformat="png",
        show=False,
        direction="LR",
        graph_attr={
            "fontsize": "18",
            "bgcolor": "#0a0a0a",
            "fontcolor": "#c8ff00",
            "pad": "0.6",
            "dpi": "150",
            "ranksep": "0.8",
        },
        node_attr={"fontcolor": "#e0e0e0", "color": "#333333"},
        edge_attr={"color": "#555555"},
    ):
        # Pipeline 1: standard-codegen
        with Cluster(
            "1. standard-codegen",
            graph_attr={"bgcolor": "#111111", "fontcolor": "#c8ff00"},
        ):
            sc0 = Action("harmlessness\nscreen")
            sc1 = Action("code\ngenerator")
            sc2a = Action("security\nauditor")
            sc2b = Action("test\nrunner")
            sc3 = Action("alignment\nauditor")
            scg = Decision("GATE")
            sc0 >> sc1 >> sc2a
            sc1 >> sc2b
            sc2a >> scg
            sc2b >> scg
            scg >> Edge(style="dashed", label="if agent code") >> sc3

        # Pipeline 2: security-deep-scan
        with Cluster(
            "2. security-deep-scan",
            graph_attr={"bgcolor": "#111111", "fontcolor": "#ff6666"},
        ):
            sd1 = Action("security\nauditor")
            sd2 = Action("prompt\nhardener")
            sd3 = Action("architecture\nreviewer")
            sdg = Decision("GATE")
            sd1 >> sdg
            sdg >> Edge(style="dashed", label="if prompt") >> sd2
            sdg >> Edge(style="dashed", label="if critical") >> sd3

        # Pipeline 3: prompt-hardening (iterative)
        with Cluster(
            "3. prompt-hardening (iterative x3)",
            graph_attr={"bgcolor": "#111111", "fontcolor": "#66ff66"},
        ):
            ph1 = Action("prompt\nhardener")
            ph2 = Action("security\nauditor")
            phg = Decision("PASS?")
            ph1 >> ph2 >> phg
            phg >> Edge(style="dashed", label="retry") >> ph1

        # Pipeline 4: architecture-review
        with Cluster(
            "4. architecture-review",
            graph_attr={"bgcolor": "#111111", "fontcolor": "#6688ff"},
        ):
            ar1 = Action("architecture\nreviewer")
            ar2a = Action("security\nauditor")
            ar2b = Action("prompt\nhardener")
            ar3 = Action("eval\nbuilder")
            ar1 >> ar2a >> ar3
            ar1 >> ar2b >> ar3

        # Pipeline 5: eval-suite-creation
        with Cluster(
            "5. eval-suite-creation",
            graph_attr={"bgcolor": "#111111", "fontcolor": "#ffaa00"},
        ):
            es1 = Action("eval\nbuilder")
            es2 = Action("test\nrunner")
            es1 >> es2

        # Pipeline 6: research-to-report
        with Cluster(
            "6. research-to-report",
            graph_attr={"bgcolor": "#0a0a1a", "fontcolor": "#aa88ff"},
        ):
            rr0 = Action("harmlessness\nscreen")
            rr1 = Action("enterprise\nsearch")
            rr2a = Action("marketing\nagent")
            rr2b = Action("compliance\nreviewer")
            rr3 = Action("security\nauditor")
            rr0 >> rr1 >> rr2a >> rr3
            rr1 >> rr2b >> rr3

        # Pipeline 7: data-to-insight
        with Cluster(
            "7. data-to-insight",
            graph_attr={"bgcolor": "#0a0a1a", "fontcolor": "#88aaff"},
        ):
            di0 = Action("harmlessness\nscreen")
            di1 = Action("data\nanalyst")
            di2a = Action("finance\nagent")
            di2b = Action("compliance\nreviewer")
            di3 = Action("marketing\nagent")
            di0 >> di1 >> di2a >> di3
            di1 >> di2b >> di3

        # Pipeline 8: compliance-review
        with Cluster(
            "8. compliance-review",
            graph_attr={"bgcolor": "#0a0a1a", "fontcolor": "#ff88aa"},
        ):
            cr0 = Action("harmlessness\nscreen")
            cr1 = Action("compliance\nreviewer")
            cr2a = Action("security\nauditor")
            cr2b = Action("enterprise\nsearch")
            cr3 = Action("marketing\nagent")
            cr0 >> cr1 >> cr2a >> cr3
            cr1 >> cr2b >> cr3


def diagram_3_layer_stack():
    """14-layer knowledge-work stack from L0 to L10."""
    with Diagram(
        "14-Layer Knowledge-Work Stack",
        filename=os.path.join(OUT_DIR, "14-layer-stack"),
        outformat="png",
        show=False,
        direction="BT",
        graph_attr={
            "fontsize": "18",
            "bgcolor": "#0a0a0a",
            "fontcolor": "#c8ff00",
            "pad": "0.6",
            "dpi": "150",
            "ranksep": "0.6",
            "nodesep": "0.4",
        },
        node_attr={"fontcolor": "#e0e0e0", "color": "#333333", "width": "3.5"},
        edge_attr={"color": "#444444"},
    ):
        # Build layers bottom-to-top
        with Cluster(
            "Governance & Welfare (L9-L10)",
            graph_attr={"bgcolor": "#1a0a00", "fontcolor": "#ff8800"},
        ):
            l10 = PredefinedProcess("L10 governance.py\nRSP, ASL, release decisions")
            l9 = PredefinedProcess("L9 welfare.py\nModel affect, distress detection")

        with Cluster(
            "Evaluation (L8)",
            graph_attr={"bgcolor": "#1a1a00", "fontcolor": "#ffff66"},
        ):
            l8 = PredefinedProcess("L8 evals.py\nA/B comparison, 3pt significance")

        with Cluster(
            "Agent Runtime (L5-L7.5)",
            graph_attr={"bgcolor": "#001a00", "fontcolor": "#66ff66"},
        ):
            l75 = PredefinedProcess("L7.5 behavioral_safety.py\n6-dim audit (Mythos)")
            l7 = PredefinedProcess("L7 harness.py\nManaged Agent brain/hands loop")
            l6 = PredefinedProcess("L6 subagents.py\nSubagentPool, cattle-not-pets")
            l5 = PredefinedProcess("L5 subtasks.py\nDAG decomposition, topo-exec")

        with Cluster(
            "Task & Prompt Layer (L3-L4)",
            graph_attr={"bgcolor": "#00001a", "fontcolor": "#6688ff"},
        ):
            l4 = PredefinedProcess("L4 tasks.py\nTaskRouter: NL → plugin skills")
            l3 = PredefinedProcess("L3 prompts.py\nPromptRegistry: 119 SKILL.md")

        with Cluster(
            "Interpretability (L1-L2.5)",
            graph_attr={"bgcolor": "#1a001a", "fontcolor": "#ff66ff"},
        ):
            l25 = PredefinedProcess("L2.5 reasoning.py\nScratchpad faithfulness")
            l2 = PredefinedProcess("L2 tracers.py\nCircuit tracing (circuit-tracer)")
            l15 = PredefinedProcess("L1.5 steering.py\nActivation steering, persona vectors")
            l1 = PredefinedProcess("L1 circuits.py\nFeature nodes, topology")

        with Cluster(
            "Foundation (L0)",
            graph_attr={"bgcolor": "#0a0a0a", "fontcolor": "#888888"},
        ):
            l0 = PredefinedProcess("L0 training.py\nRLHF, Constitutional AI, character")

        # Stack connections (bottom to top)
        l0 >> l1 >> l15 >> l2 >> l25 >> l3 >> l4 >> l5 >> l6 >> l7 >> l75 >> l8 >> l9 >> l10

        # Vendor connections
        with Cluster(
            "Vendors",
            graph_attr={"bgcolor": "#0a0a0a", "fontcolor": "#555555"},
        ):
            v_ct = Document("circuit-tracer v0.4.1")
            v_kwp = Document("knowledge-work-plugins\n17 plugins")
            v_sr = Document("safety-research\n18 repos")

        v_ct >> Edge(style="dotted", color="#555555") >> l2
        v_kwp >> Edge(style="dotted", color="#555555") >> l3
        v_sr >> Edge(style="dotted", color="#555555") >> l75


def diagram_4_agent_topology():
    """25 agents grouped by model tier, showing tool grants and connections."""
    with Diagram(
        "Agent Topology (25 Agents, 4 Model Tiers)",
        filename=os.path.join(OUT_DIR, "agent-topology"),
        outformat="png",
        show=False,
        direction="TB",
        graph_attr={
            "fontsize": "18",
            "bgcolor": "#0a0a0a",
            "fontcolor": "#c8ff00",
            "pad": "0.6",
            "dpi": "150",
        },
        node_attr={"fontcolor": "#e0e0e0", "color": "#333333"},
        edge_attr={"color": "#444444"},
    ):
        orch = Server("Opus 4.6\nOrchestrator")

        # Opus safety agents
        with Cluster(
            "Opus Safety (3)",
            graph_attr={"bgcolor": "#1a0000", "fontcolor": "#ff6666"},
        ):
            sa = Server("security-auditor\nRead,Glob,Grep,Bash")
            aa = Server("alignment-auditor\nRead,Glob,Grep")
            ar = Server("architecture-reviewer\nRead,Glob,Grep")

        # Sonnet codegen agents
        with Cluster(
            "Sonnet Codegen (4)",
            graph_attr={"bgcolor": "#001a00", "fontcolor": "#66ff66"},
        ):
            cg = Server("code-generator\nRead,Glob,Grep,Write,Edit")
            tr = Server("test-runner\nRead,Glob,Grep,Bash")
            ph = Server("prompt-hardener\nRead,Glob,Grep,Edit")
            eb = Server("eval-builder\nRead,Glob,Grep,Write,Bash")

        # Haiku screen
        with Cluster(
            "Haiku (1)",
            graph_attr={"bgcolor": "#00001a", "fontcolor": "#6666ff"},
        ):
            hs = Server("harmlessness-screen\nJSON-only, 256 tokens")

        # Knowledge-work agents (Opus)
        with Cluster(
            "Opus Knowledge-Work (17)",
            graph_attr={"bgcolor": "#0a0a1a", "fontcolor": "#aa88ff"},
        ):
            with Cluster("Business", graph_attr={"bgcolor": "#111122"}):
                s1 = Server("sales-agent")
                s2 = Server("marketing-agent")
                s3 = Server("finance-agent")
                s4 = Server("hr-agent")

            with Cluster("Technical", graph_attr={"bgcolor": "#111122"}):
                t1 = Server("engineering-agent")
                t2 = Server("data-analyst")
                t3 = Server("product-mgmt-agent")
                t4 = Server("operations-agent")

            with Cluster("Specialist", graph_attr={"bgcolor": "#111122"}):
                sp1 = Server("compliance-reviewer")
                sp2 = Server("enterprise-search")
                sp3 = Server("design-agent")
                sp4 = Server("bio-research-agent")

            with Cluster("Support & Partners", graph_attr={"bgcolor": "#111122"}):
                su1 = Server("customer-support")
                su2 = Server("productivity-agent")
                su3 = Server("partner-built-agent")
                su4 = Server("pdf-viewer-agent")
                su5 = Server("cowork-plugin-agent")

        # Orchestrator connections
        orch >> Edge(color="#ff6666", label="audit") >> sa
        orch >> Edge(color="#ff6666") >> aa
        orch >> Edge(color="#ff6666") >> ar

        orch >> Edge(color="#66ff66", label="codegen") >> cg
        orch >> Edge(color="#66ff66") >> tr
        orch >> Edge(color="#66ff66") >> ph
        orch >> Edge(color="#66ff66") >> eb

        orch >> Edge(color="#6666ff", label="pre-screen") >> hs

        orch >> Edge(color="#aa88ff", label="domain") >> s1
        orch >> Edge(color="#aa88ff") >> t1
        orch >> Edge(color="#aa88ff") >> sp1
        orch >> Edge(color="#aa88ff") >> su1


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    print("Generating human-readable architecture diagrams...")
    print("  [1/4] System overview...")
    diagram_1_system_overview()
    print("  [2/4] Pipeline flows...")
    diagram_2_pipeline_flows()
    print("  [3/4] 14-layer stack...")
    diagram_3_layer_stack()
    print("  [4/4] Agent topology...")
    diagram_4_agent_topology()
    print(f"Done. 4 diagrams written to {OUT_DIR}/")
