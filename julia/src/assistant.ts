/**
 * assistant.ts — Multi-turn legal AI sessions with builder pattern.
 *
 * Provides JuliaSessionBuilder (Cherny Ch.5 p.129) and JuliaSession for
 * stateful, multi-turn conversations grounded in a specific LegalSkill.
 * Conversation history is maintained in-memory as a messages array and
 * replayed on every send() call so the model has full context.
 *
 * Auth: CLAUDE_CODE_OAUTH_TOKEN (never ANTHROPIC_API_KEY).
 */

import Anthropic from "@anthropic-ai/sdk";
import { buildLegalSystemPrompt } from "./completion.js";
import {
  Ok,
  Err,
  FileId,
  type Result,
  type LegalSkill,
  type ProjectId,
  type MatterId,
} from "./types.js";

// ── Session config ────────────────────────────────────────────

/**
 * Resolved configuration for a JuliaSession.
 * Constructed by JuliaSessionBuilder.build().
 */
type JuliaSessionConfig<S extends LegalSkill> = {
  skill: S;
  model: string;
  projectIds: ProjectId[];
  matterId: MatterId | undefined;
};

// ── Message shape mirroring the SDK ──────────────────────────

type MessageParam = {
  role: "user" | "assistant";
  content: string;
};

// ── JuliaSessionBuilder ───────────────────────────────────────

/**
 * Builder for JuliaSession (Cherny Ch.5 p.129).
 *
 * All mutating methods return `this` for fluent chaining.
 * build() validates that skill has been set before constructing the session.
 *
 * @example
 *   const session = JuliaSession.builder()
 *     .skill("review-contract")
 *     .vault(ProjectId("proj_1"))
 *     .matter(MatterId("matter_abc"))
 *     .build();
 */
export class JuliaSessionBuilder<S extends LegalSkill> {
  private _skill: S | undefined = undefined;
  private _model: string = "claude-opus-4-6";
  private _projectIds: ProjectId[] = [];
  private _matterId: MatterId | undefined = undefined;

  /**
   * Set the legal skill that specializes this session's system prompt.
   * Must be called before build().
   */
  skill(s: S): this {
    this._skill = s;
    return this;
  }

  /**
   * Add one or more vault project IDs to ground responses in documents.
   * Can be called multiple times; IDs accumulate.
   */
  vault(...projectIds: ProjectId[]): this {
    this._projectIds.push(...projectIds);
    return this;
  }

  /**
   * Associate this session with a client matter for billing and audit.
   */
  matter(id: MatterId): this {
    this._matterId = id;
    return this;
  }

  /**
   * Override the default model (claude-opus-4-6).
   */
  model(m: string): this {
    this._model = m;
    return this;
  }

  /**
   * Validate configuration and construct the JuliaSession.
   *
   * @throws Error when skill has not been set.
   */
  build(): JuliaSession<S> {
    if (this._skill === undefined) {
      throw new Error(
        "JuliaSessionBuilder: skill() must be called before build()",
      );
    }
    const config: JuliaSessionConfig<S> = {
      skill: this._skill,
      model: this._model,
      projectIds: this._projectIds,
      matterId: this._matterId,
    };
    return new JuliaSession(config);
  }
}

// ── JuliaSession ──────────────────────────────────────────────

/**
 * Stateful multi-turn legal AI session for a specific LegalSkill.
 *
 * Maintains conversation history in-memory. Each send() appends the user
 * message, calls the Anthropic Messages API with the full history, and
 * appends the assistant reply on success. On failure the user message is
 * rolled back so the history remains consistent.
 *
 * Use JuliaSession.builder() as the entry point.
 */
export class JuliaSession<S extends LegalSkill> {
  private readonly config: JuliaSessionConfig<S>;
  private readonly history: MessageParam[] = [];
  private sessionId: string | undefined = undefined;

  /** @internal — use JuliaSession.builder() instead. */
  constructor(config: JuliaSessionConfig<S>) {
    this.config = config;
  }

  /**
   * Static factory entry point for the builder pattern.
   *
   * @returns A fresh JuliaSessionBuilder<never> ready to be configured.
   */
  static builder(): JuliaSessionBuilder<never> {
    return new JuliaSessionBuilder<never>();
  }

  /**
   * Send a user message and receive the assistant's reply.
   *
   * Appends the user message to history, calls the API, and on success
   * appends the assistant reply and initialises the session ID.
   * On failure the user message is rolled back and an Err is returned.
   *
   * @param prompt - The user's message text.
   * @returns Ok(string) with the assistant reply, or Err on API failure.
   */
  async send(prompt: string): Promise<Result<string>> {
    // Initialise session ID on first send
    if (this.sessionId === undefined) {
      this.sessionId = crypto.randomUUID();
    }

    const systemPrompt = buildLegalSystemPrompt(this.config.skill);

    // Tentatively append the user turn — will be rolled back on error
    this.history.push({ role: "user", content: prompt });

    try {
      const client = new Anthropic();
      const apiResponse = await client.messages.create({
        model: this.config.model,
        max_tokens: 4096,
        system: systemPrompt,
        messages: this.history,
      });

      // Extract text from content blocks
      const text = apiResponse.content
        .filter(
          (block): block is Anthropic.TextBlock => block.type === "text",
        )
        .map((block) => block.text)
        .join("\n");

      // Commit the assistant turn to history
      this.history.push({ role: "assistant", content: text });

      return Ok(text);
    } catch (err) {
      // Roll back the user message so history stays consistent
      this.history.pop();

      const reason = err instanceof Error ? err.message : String(err);
      return Err({
        type: "processing_failed",
        fileId: FileId(""),
        reason: `Session send failed: ${reason}`,
      });
    }
  }

  /**
   * Returns the session ID assigned on the first send(), or undefined
   * if no messages have been sent yet.
   */
  getSessionId(): string | undefined {
    return this.sessionId;
  }
}
