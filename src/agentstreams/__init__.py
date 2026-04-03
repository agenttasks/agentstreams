"""AgentStreams — Unified Data Architecture for multi-language skill pipelines.

Implements the Netflix UDA pattern: model once (ontology), represent everywhere
(Avro, GraphQL, TTL, SQL). All data flows through a single semantic model with
bloom-filter deduplication, Scrapy crawlers, DSPy programmatic prompts, and
Neon Postgres persistence.
"""

__version__ = "0.1.0"
