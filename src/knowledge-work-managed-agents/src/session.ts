/**
 * Session store — durable event log backed by Neon Postgres.
 *
 * The session log lives OUTSIDE Claude's context window (per Anthropic's
 * Managed Agents design). It survives harness crashes, enables
 * getEvents() interrogation, and persists across restarts.
 *
 * Uses @neondatabase/serverless for SQL-over-HTTP (no TCP needed).
 * Falls back to in-memory storage when NEON_DATABASE_URL is not set.
 *
 * Auth: CLAUDE_CODE_OAUTH_TOKEN (never ANTHROPIC_API_KEY).
 */

import { neon, type NeonQueryFunction } from "@neondatabase/serverless";

export interface SessionEvent {
  id: number;
  session_id: string;
  type: string;
  data: Record<string, unknown>;
  layer: number;
  timestamp: string;
}

export class SessionStore {
  private sql: NeonQueryFunction<false, false> | null = null;
  private memory: SessionEvent[] = [];
  private counter = 0;

  constructor(private sessionId: string) {
    const dbUrl = process.env.NEON_DATABASE_URL;
    if (dbUrl) {
      this.sql = neon(dbUrl);
    }
  }

  /** Emit an event to the session log */
  async emit(
    type: string,
    data: Record<string, unknown>,
    layer: number = 0
  ): Promise<SessionEvent> {
    const event: SessionEvent = {
      id: ++this.counter,
      session_id: this.sessionId,
      type,
      data,
      layer,
      timestamp: new Date().toISOString(),
    };

    if (this.sql) {
      await this.sql`
        INSERT INTO session_events (session_id, type, data, layer, timestamp)
        VALUES (${this.sessionId}, ${type}, ${JSON.stringify(data)}, ${layer}, ${event.timestamp})
      `;
    }

    this.memory.push(event);
    return event;
  }

  /** Query events — the harness uses this to rebuild context after crash */
  async getEvents(opts?: {
    start?: number;
    end?: number;
    type?: string;
    layer?: number;
  }): Promise<SessionEvent[]> {
    let events = [...this.memory];

    if (opts?.type) {
      events = events.filter((e) => e.type === opts.type);
    }
    if (opts?.layer !== undefined) {
      events = events.filter((e) => e.layer === opts.layer);
    }
    if (opts?.start !== undefined) {
      events = events.slice(opts.start, opts?.end);
    }

    return events;
  }

  /** Get the last N events (for context window management) */
  async tail(n: number): Promise<SessionEvent[]> {
    return this.memory.slice(-n);
  }

  /** Total event count */
  get length(): number {
    return this.memory.length;
  }
}
