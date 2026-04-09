-- ═══════════════════════════════════════════════════════════
-- Migration 001: Knowledge Work Plugins
-- Seeds skills, agent_manifests, and mcp_servers tables
-- with data from vendors/knowledge-work-plugins (17 plugins)
-- and vendors/financial-services-plugins (5 plugins)
-- ═══════════════════════════════════════════════════════════

-- ── Knowledge-work skills ───────────────────────────────

INSERT INTO skills (name, description, trigger_pattern) VALUES
-- sales (9 skills)
('account-research', 'Research a company or person and get actionable sales intel', 'research [company], look up [person], intel on [prospect]'),
('call-prep', 'Prepare for a sales call with account context and attendee research', 'prep me for my call with [company]'),
('call-summary', 'Process call notes — extract action items, decisions, follow-ups', 'summarize this call'),
('competitive-intelligence', 'Research competitors and build interactive battlecards', 'competitive analysis for [company]'),
('create-an-asset', 'Generate tailored sales assets (landing pages, decks, one-pagers)', 'create a [asset type] for [prospect]'),
('daily-briefing', 'Start your day with a prioritized sales briefing', 'daily briefing, start my day'),
('draft-outreach', 'Research a prospect then draft personalized outreach', 'draft outreach to [person]'),
('forecast', 'Generate a weighted sales forecast with scenarios', 'forecast, sales projection'),
('pipeline-review', 'Analyze pipeline health — prioritize deals, flag risks', 'pipeline review, deal health'),
-- data (10 skills)
('analyze', 'General analytical reasoning over datasets', 'analyze [data]'),
('build-dashboard', 'Build interactive dashboards from data', 'build dashboard for [metrics]'),
('create-viz', 'Create custom visualizations', 'visualize [data]'),
('data-context-extractor', 'Contextual feature extraction from data', 'extract context from [data]'),
('data-visualization', 'Chart and graph generation', 'chart [data], plot [metrics]'),
('explore-data', 'Exploratory data analysis', 'explore [dataset]'),
('sql-queries', 'SQL query generation and optimization', 'write SQL for [question]'),
('statistical-analysis', 'Statistical tests and modeling', 'run stats on [data]'),
('validate-data', 'Data quality and integrity checks', 'validate [data]'),
('write-query', 'Ad-hoc query authoring', 'write query for [question]'),
-- engineering (10 skills)
('architecture', 'System architecture review', 'review architecture'),
('code-review', 'Code review workflows', 'review this code'),
('debug', 'Systematic debugging workflows', 'debug [error]'),
('deploy-checklist', 'Pre/post deployment verification', 'deployment checklist'),
('documentation', 'Technical and product documentation', 'document [component]'),
('incident-response', 'Incident triage and coordination', 'incident response'),
('standup', 'Standup summary and prep', 'standup, daily sync'),
('system-design', 'System design guidance', 'design [system]'),
('tech-debt', 'Technical debt assessment and prioritization', 'assess tech debt'),
('testing-strategy', 'Test planning and strategy', 'testing strategy for [feature]')
ON CONFLICT (name) DO NOTHING;

-- ── Knowledge-work agent manifests ──────────────────────

INSERT INTO agent_manifests (name, model_override, allowed_tools, manifest_path) VALUES
('sales-agent', 'claude-opus-4-6', ARRAY['Read','Glob','Grep','Bash','Write','WebFetch','WebSearch'], '.claude/agents/sales-agent.md'),
('data-analyst', 'claude-opus-4-6', ARRAY['Read','Glob','Grep','Bash','Write','Edit'], '.claude/agents/data-analyst.md'),
('engineering-agent', 'claude-opus-4-6', ARRAY['Read','Glob','Grep','Bash','Write','Edit'], '.claude/agents/engineering-agent.md'),
('compliance-reviewer', 'claude-opus-4-6', ARRAY['Read','Glob','Grep'], '.claude/agents/compliance-reviewer.md'),
('finance-agent', 'claude-opus-4-6', ARRAY['Read','Glob','Grep'], '.claude/agents/finance-agent.md'),
('marketing-agent', 'claude-opus-4-6', ARRAY['Read','Glob','Grep','Bash','Write','Edit','WebFetch','WebSearch'], '.claude/agents/marketing-agent.md'),
('design-agent', 'claude-opus-4-6', ARRAY['Read','Glob','Grep','Write','Edit'], '.claude/agents/design-agent.md'),
('hr-agent', 'claude-opus-4-6', ARRAY['Read','Glob','Grep','Write'], '.claude/agents/hr-agent.md'),
('operations-agent', 'claude-opus-4-6', ARRAY['Read','Glob','Grep','Bash'], '.claude/agents/operations-agent.md'),
('product-management-agent', 'claude-opus-4-6', ARRAY['Read','Glob','Grep','Bash'], '.claude/agents/product-management-agent.md'),
('customer-support-agent', 'claude-opus-4-6', ARRAY['Read','Glob','Grep','Bash'], '.claude/agents/customer-support-agent.md'),
('enterprise-search-agent', 'claude-opus-4-6', ARRAY['Read','Glob','Grep','Bash','WebFetch','WebSearch'], '.claude/agents/enterprise-search-agent.md'),
('bio-research-agent', 'claude-opus-4-6', ARRAY['Read','Glob','Grep','Bash','Write','Edit'], '.claude/agents/bio-research-agent.md'),
('productivity-agent', 'claude-opus-4-6', ARRAY['Read','Glob','Grep','Bash'], '.claude/agents/productivity-agent.md'),
('partner-built-agent', 'claude-opus-4-6', ARRAY['Read','Glob','Grep','Bash','Write','WebFetch','WebSearch'], '.claude/agents/partner-built-agent.md'),
('cowork-plugin-agent', 'claude-opus-4-6', ARRAY['Read','Glob','Grep','Write','Edit'], '.claude/agents/cowork-plugin-agent.md'),
('pdf-viewer-agent', 'claude-opus-4-6', ARRAY['Read','Glob','Grep','Bash'], '.claude/agents/pdf-viewer-agent.md')
ON CONFLICT (name) DO NOTHING;

-- ── MCP servers from knowledge-work plugins ─────────────

INSERT INTO mcp_servers (id, name, transport, description) VALUES
('mcp-slack', 'Slack', 'http', 'https://mcp.slack.com/mcp'),
('mcp-hubspot', 'HubSpot', 'http', 'https://mcp.hubspot.com/anthropic'),
('mcp-notion', 'Notion', 'http', 'https://mcp.notion.com/mcp'),
('mcp-linear', 'Linear', 'http', 'https://mcp.linear.app/mcp'),
('mcp-figma', 'Figma', 'http', 'https://mcp.figma.com/mcp'),
('mcp-amplitude', 'Amplitude', 'http', 'https://mcp.amplitude.com/mcp'),
('mcp-intercom', 'Intercom', 'http', 'https://mcp.intercom.com/mcp'),
('mcp-apollo', 'Apollo', 'http', 'https://api.apollo.io/mcp'),
('mcp-clay', 'Clay', 'http', 'https://api.clay.com/v3/mcp'),
('mcp-zoominfo', 'ZoomInfo', 'http', 'https://mcp.zoominfo.com/mcp'),
('mcp-ms365', 'Microsoft 365', 'http', 'https://microsoft365.mcp.claude.com/mcp')
ON CONFLICT (id) DO NOTHING;

-- ── Task queue types for knowledge-work ─────────────────

-- Ensure the tasks.type CHECK constraint includes knowledge_work
-- (already present in base schema: type IN ('code', 'knowledge_work', 'financial'))
