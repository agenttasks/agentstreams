"""Neon Postgres persistence layer for UDA entities.

All entity CRUD flows through this module. Uses psycopg async driver
with connection pooling. Schema matches ontology/schema.sql.
"""
