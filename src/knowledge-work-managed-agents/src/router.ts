/**
 * Task router — maps natural language requests to knowledge-work tasks.
 *
 * Bridges Layer 4 (tasks) with the managed agent runtime. Uses keyword
 * matching locally and can escalate to Claude for intent classification.
 *
 * Auth: CLAUDE_CODE_OAUTH_TOKEN (never ANTHROPIC_API_KEY).
 */

export interface TaskDefinition {
  name: string;
  description: string;
  domain: string;
  pluginCategory: string;
  skillName: string;
  agentName: string;
  model: string;
  complexity: "atomic" | "composite" | "orchestrated";
}

/** Task catalog — mirrors src/knowledge_work/tasks.py TASK_CATALOG */
const CATALOG: TaskDefinition[] = [
  { name: "sales/account-research", description: "Research a prospect account", domain: "sales", pluginCategory: "sales", skillName: "account-research", agentName: "sales-agent", model: "claude-opus-4-6", complexity: "atomic" },
  { name: "sales/call-prep", description: "Prepare for a sales call", domain: "sales", pluginCategory: "sales", skillName: "call-prep", agentName: "sales-agent", model: "claude-opus-4-6", complexity: "composite" },
  { name: "sales/draft-outreach", description: "Draft outreach email or message", domain: "sales", pluginCategory: "sales", skillName: "draft-outreach", agentName: "sales-agent", model: "claude-opus-4-6", complexity: "orchestrated" },
  { name: "finance/journal-entry", description: "Create accounting journal entry", domain: "finance", pluginCategory: "finance", skillName: "journal-entry", agentName: "finance-agent", model: "claude-opus-4-6", complexity: "atomic" },
  { name: "finance/variance-analysis", description: "Analyze financial variances", domain: "finance", pluginCategory: "finance", skillName: "variance-analysis", agentName: "finance-agent", model: "claude-opus-4-6", complexity: "composite" },
  { name: "legal/contract-review", description: "Review contract for risks", domain: "legal", pluginCategory: "legal", skillName: "contract-review", agentName: "compliance-reviewer", model: "claude-opus-4-6", complexity: "orchestrated" },
  { name: "engineering/code-improvement", description: "Improve code quality", domain: "engineering", pluginCategory: "engineering", skillName: "code-improvement", agentName: "engineering-agent", model: "claude-opus-4-6", complexity: "composite" },
  { name: "data/sql-query", description: "Write and execute SQL queries", domain: "data", pluginCategory: "data", skillName: "sql-queries", agentName: "data-analyst", model: "claude-opus-4-6", complexity: "atomic" },
  { name: "design/accessibility-review", description: "Review accessibility compliance", domain: "design", pluginCategory: "design", skillName: "accessibility-review", agentName: "design-agent", model: "claude-opus-4-6", complexity: "composite" },
  { name: "customer-support/ticket-triage", description: "Triage support ticket", domain: "customer-support", pluginCategory: "customer-support", skillName: "ticket-triage", agentName: "customer-support-agent", model: "claude-opus-4-6", complexity: "atomic" },
  { name: "enterprise-search/search", description: "Cross-tool knowledge search", domain: "enterprise-search", pluginCategory: "enterprise-search", skillName: "search", agentName: "enterprise-search-agent", model: "claude-opus-4-6", complexity: "atomic" },
  { name: "product-management/spec", description: "Write product specification", domain: "product-management", pluginCategory: "product-management", skillName: "spec", agentName: "product-management-agent", model: "claude-opus-4-6", complexity: "composite" },
  { name: "marketing/create-an-asset", description: "Create marketing content asset", domain: "marketing", pluginCategory: "marketing", skillName: "create-an-asset", agentName: "marketing-agent", model: "claude-opus-4-6", complexity: "composite" },
  { name: "human-resources/comp-analysis", description: "Compensation analysis", domain: "human-resources", pluginCategory: "human-resources", skillName: "comp-analysis", agentName: "hr-agent", model: "claude-opus-4-6", complexity: "atomic" },
];

export class TaskRouter {
  private catalog: TaskDefinition[];

  constructor(catalog?: TaskDefinition[]) {
    this.catalog = catalog ?? CATALOG;
  }

  /** Route a natural language request to the best matching task */
  route(request: string): TaskDefinition | null {
    const lower = request.toLowerCase();
    let best: TaskDefinition | null = null;
    let bestScore = 0;

    for (const task of this.catalog) {
      let score = 0;
      if (lower.includes(task.domain)) score += 3;
      for (const word of task.skillName.replace(/-/g, " ").split(" ")) {
        if (lower.includes(word)) score += 2;
      }
      for (const word of task.description.toLowerCase().split(" ")) {
        if (word.length > 3 && lower.includes(word)) score += 1;
      }
      if (score > bestScore) {
        bestScore = score;
        best = task;
      }
    }

    return bestScore > 0 ? best : null;
  }

  /** List all tasks, optionally filtered by domain */
  list(domain?: string): TaskDefinition[] {
    if (!domain) return [...this.catalog];
    return this.catalog.filter((t) => t.domain === domain);
  }

  /** Get all unique domains */
  domains(): string[] {
    return [...new Set(this.catalog.map((t) => t.domain))];
  }
}
