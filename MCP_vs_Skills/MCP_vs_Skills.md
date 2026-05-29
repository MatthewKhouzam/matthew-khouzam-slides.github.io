# MCP vs Skills: When to Use Which

## What They Are

**MCP (Model Context Protocol)** is an open standard (released Nov 2024, donated to the Linux Foundation's Agentic AI Foundation in Dec 2025) that provides a universal way to give LLMs tools and real-time data access. It follows a client-server architecture — the AI application contains an MCP client that connects to MCP servers, which expose tools, resources, and prompts. Anthropic calls it "the USB-C port of AI applications." As of early 2026, MCP has 97M+ monthly SDK downloads and 10,000+ active servers, with backing from Anthropic, OpenAI, Google, Microsoft, AWS, and others.

**Skills** are markdown-based instruction sets stored as directories on the filesystem. At their core, a skill is a `SKILL.md` file (with YAML frontmatter metadata, optional scripts, docs, and reference folders) that tells the agent *how* to approach a task. They use progressive disclosure: only metadata loads at startup (~100 tokens), the full body loads when relevant (~5,000 tokens), and additional files load on demand. Introduced by Anthropic in Oct 2025, Skills work across Claude.ai, Claude Code, the Claude Agent SDK, and the Claude API.

## Key Differences

| Dimension | MCP | Skills |
|-----------|-----|--------|
| Nature | Tools and data access | Instructions and workflows |
| How they work | Called on-demand via tool calls | Loaded into context progressively |
| Data | Real-time, live data (APIs, DBs, tickets) | Static reference material and procedures |
| Scope | External systems, network resources | Local file system, coding patterns, conventions |
| Auth | Often requires tokens/OAuth | None needed |
| Creation | Requires writing code (server implementation) | Plain English markdown files |
| Context cost | Progressive discovery (as of MCP 2.0); previously all schemas at startup | Progressive disclosure (only what's needed) |
| Portability | Any AI app with an MCP client (Claude, ChatGPT, Gemini, Cursor) | Primarily Claude ecosystem; open standard as of 2025 |
| Distribution | Hosted servers (local or cloud) | Files in a directory (shareable via git) |
| Persistence | Only active when connected | Always active once installed |
| Analogy | A set of power tools on a workbench | A style guide handed to a developer |

## When to Use MCP

- **Live data access** — current inventory, real-time API responses, database queries, latest emails
- **External system interaction** — creating GitHub PRs, reading Jira tickets, querying Figma, deploying resources
- **Cross-model compatibility** — building tool integrations once for multiple AI models
- **Authenticated operations** — anything requiring API keys, OAuth tokens, or credential management
- **Simple data retrieval** — one API call gets what you need with minimal processing

## When to Use Skills

- **Complex multi-step workflows** — financial modeling, document creation with specific formatting, compliance reviews, data analysis pipelines
- **Encoding organizational knowledge** — brand guidelines, SOPs, domain-specific methodologies, team coding conventions
- **Standardizing AI behavior across a team** — commit skills to the repo so every developer gets identical AI behavior
- **Teaching framework best practices** — "prefer Server Components," "always use named exports," "follow this error handling pattern"
- **Executable code for deterministic operations** — data validation, calculations, file format conversions
- **Multi-tool orchestration** — defining the *order* and *logic* of how multiple tools should be combined

## The Sweet Spot: Using Both Together

They are complementary, not competing. The mental model:

> **MCP gets data to the AI. Skills tell the AI what to do with it.**

As Anthropic explains in their "Skills Explained" blog post, Skills sit alongside prompts, Projects, MCP, and subagents in the Claude stack — each solving a different problem. Skills encode *how* to do something; MCP provides the *ability* to do something the AI couldn't do before.

Example: Connect Notion via its MCP server (15+ tools for CRUD operations), then use a skill to define *how* to create a specific type of page — what sections to include, what research to do, what format to follow.

Example: A deployment skill defines the process ("check CI is green → merge to main → run smoke tests → promote to production"), while GitHub and Playwright MCP servers execute each step.

Example (from IntuitionLabs): A sales workflow where MCP connects to the CRM database and transcription service, while a Skill encodes the logic of *how* to extract key points from a call transcript and map them into the correct CRM fields.

## Anti-Patterns to Avoid

- Putting API documentation in a skill (it goes stale — use a live docs MCP server instead)
- Using an MCP server to enforce coding conventions (use a skill for conventions, a linter for enforcement)
- Installing too many skills (context window bloat — prioritize 5–10 most impactful)
- Duplicating MCP tool instructions in a skill (the MCP server already knows how to create a PR; the skill should describe your *team's PR conventions*)
- Giving the LLM too many MCP tools it doesn't need (causes "context rot" — irrelevant tool schemas consuming tokens and degrading performance)

## Where Things Are Heading

- Skills are gaining traction faster than MCP did at the same stage
- MCP is evolving: streamable HTTP for easier cloud deployment, OAuth 2.1 for user-facing auth, and future solutions for headless microservice auth
- MCP is now vendor-neutral under Linux Foundation governance (Agentic AI Foundation), not tied to any single vendor
- MCP Apps (Jan 2026) allow MCP tools to return interactive UI components (dashboards, forms) directly in the conversation
- For local coding agents (Claude Code, Cursor), skills can substitute for some MCP use cases via CLI-calling scripts
- For agentic microservices running headlessly in the cloud, MCP remains essential — skills don't make sense in that context
- A Python API for programmatically using skills in custom agents exists but is early-stage
- Enterprise evidence: Rakuten reported ~87.5% faster financial reporting with Skills; an e-commerce company automated 50%+ of support tickets saving ~$2M/year

## What About Direct API Access?

Direct API access (hardcoding HTTP calls or SDK usage into your agent) is another option, but it's rigid. You're bound to a single tool — if you build a custom integration against the GitHub REST API, that code only works with GitHub, only in that one agent, and only for the exact endpoints you wired up. There's no discoverability, no standard schema, and no reuse across models or applications. MCP solves this by providing a universal protocol layer: one integration pattern that works across any AI client, with self-describing tools that the model can reason about dynamically. Think of it like the Language Server Protocol (LSP) for IDEs. Before LSP, every editor had to write its own integration for every language — VS Code needed a Python plugin, Vim needed a separate one, and so on. LSP defined clear roles (editor as client, language tooling as server) and created a vibrant ecosystem: build one language server and every editor gets autocomplete, go-to-definition, and diagnostics for free. MCP does the same for AI agents — define one tool server and every AI client can use it. Direct API access is the pre-LSP world: bespoke, brittle, and duplicated everywhere.

Direct API access still makes sense for one-off scripts or tightly controlled pipelines where flexibility isn't needed, but for agentic workflows it quickly becomes a maintenance burden.

---

## References

1. Shaw, "Agent Skills vs MCP: What's the difference?" — [YouTube](https://www.youtube.com/watch?v=6wdvSH61xGw)
2. Sterling, "Claude Skills vs MCP: What's the Difference and When to Use Each?" — [YouTube](https://www.youtube.com/watch?v=qthyl0GCpDo)
3. "Agent Skills or MCP in the era of Claude Code?" — [YouTube](https://www.youtube.com/watch?v=pvxNcQTcIy4)
4. Developer Toolkit, "Skills vs MCP — When to Use Which" — [developertoolkit.ai](https://developertoolkit.ai/en/shared-workflows/skills-ecosystem/skills-vs-mcp/)
5. Anthropic, "Skills explained: How Skills compares to prompts, Projects, MCP, and subagents" — [claude.com/blog](https://claude.com/blog/skills-explained)
6. IntuitionLabs, "Claude Skills vs. MCP: A Technical Comparison for AI Workflows" — [intuitionlabs.ai](https://intuitionlabs.ai/articles/claude-skills-vs-mcp)

---

## Quiz: MCP or Skill?

For each scenario, decide whether you'd reach for an **MCP server**, a **Skill**, or **both**.

| # | Scenario | Answer |
|---|----------|--------|
| 1 | You want Claude to always write React components using Server Components by default and named exports. | **Skill** — coding conventions and patterns, no external access needed. |
| 2 | You need the AI to read your Jira tickets and create GitHub PRs that reference them. | **MCP** — requires live API access to two external systems. |
| 3 | Your team has a 12-step deployment checklist that involves checking CI status, running smoke tests, and promoting to prod. | **Both** — Skill defines the procedure; MCP servers (GitHub, CI, Playwright) execute each step. |
| 4 | You want Claude to format every Excel report with your company's header, color scheme, and specific pivot table layout. | **Skill** — deterministic formatting instructions, no external data needed. |
| 5 | You need the AI to query your Postgres database for the latest sales figures. | **MCP** — requires real-time data access to an external system. |
| 6 | You want all developers on your team to get the same AI coding behavior when they clone the repo. | **Skill** — commit it to the repo; every dev gets identical instructions. |
| 7 | You want Claude to post a message to Slack when a build fails. | **MCP** — requires authenticated access to the Slack API. |
| 8 | You have a complex financial model: take quarterly data, compute variance, flag anomalies, and produce a formatted PDF report. | **Skill** — multi-step procedural workflow with deterministic calculations and formatting. |
| 9 | You want the AI to fetch the latest documentation for a library that updates frequently. | **MCP** — live docs change; a skill would go stale. |
| 10 | You want Claude to always structure PR descriptions with a summary, test plan, and linked ticket — and then actually create the PR. | **Both** — Skill encodes the PR template/conventions; GitHub MCP server creates the PR. |
| 11 | You need the AI to authenticate with OAuth and access a user's Google Drive files. | **MCP** — requires credential handling and external API calls. |
| 12 | You want Claude to analyze call transcripts and map extracted info into specific CRM fields following your team's taxonomy. | **Both** — MCP connects to the transcription service and CRM API; Skill encodes the mapping logic and field taxonomy. |
| 13 | You want the AI to enforce that all SQL queries use parameterized inputs and never use `SELECT *`. | **Skill** — coding standard, no external access. |
| 14 | You need to check real-time inventory levels across three warehouses before recommending a shipping option. | **MCP** — requires live data from external inventory systems. |
| 15 | You want Claude to generate brand-compliant marketing emails in your company's voice and tone. | **Skill** — brand guidelines and writing conventions are static instructions. |

**Rule of thumb:** If it needs to *know how* → Skill. If it needs to *reach out* → MCP. If it needs both → use both.
