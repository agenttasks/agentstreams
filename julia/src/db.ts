/**
 * Shared Neon database connection — single lazy-initialized SQL function.
 *
 * All Julia modules import getSql() from here instead of maintaining
 * their own _sql singletons. Eliminates the duplicated connection
 * pattern found in matters.ts and audit.ts.
 *
 * Auth: CLAUDE_CODE_OAUTH_TOKEN (never ANTHROPIC_API_KEY).
 */

import { neon, type NeonQueryFunction } from "@neondatabase/serverless";
import { Err, type Result } from "./types.js";

let _sql: NeonQueryFunction<false, false> | null = null;

/**
 * Get the shared Neon SQL tagged template function.
 *
 * Returns Result instead of throwing when NEON_DATABASE_URL is not set.
 */
export function getSql(): Result<NeonQueryFunction<false, false>> {
  if (_sql) {
    return { ok: true, value: _sql };
  }
  const url = process.env.NEON_DATABASE_URL;
  if (!url) {
    return Err({
      type: "database_error",
      message: "NEON_DATABASE_URL environment variable is not set",
    });
  }
  _sql = neon(url);
  return { ok: true, value: _sql };
}

/**
 * Reset the connection (for testing).
 * @internal
 */
export function _resetSql(): void {
  _sql = null;
}
