---
name: timeln-secondbrain
description: Acts as the user's virtual second brain -- pulls real data from their Timeln account (documents + knowledge graph) via the Timeln MCP server, applies MECE gap analysis and the PARA framework, then returns crisp learning/action recommendations and optionally a D3 knowledge-graph visualization. Trigger whenever the user says "second brain", "thinking partner", "knowledge partner", "what should I learn today", "what should I do today", "connect my ideas", "show my knowledge gaps", "build a knowledge graph", or "what's in my brain", or asks for insight from their past ingested data. Also trigger when the user asks any question prefixed with "based on my past data", "based on what I've learned", or "from my knowledge graph". Always use this skill -- never guess from memory alone.
compatibility: "Requires a free Timeln account (timeln.app/signup) and an API token from Settings -> API Tokens. The MCP server is hosted -- no local install needed."
license: MIT
allowed-tools: mcp__timeln__whoami, mcp__timeln__get_recent_docs, mcp__timeln__search_documents, mcp__timeln__get_document, mcp__timeln__query_knowledge, mcp__timeln__get_topic_entities, mcp__timeln__ingest_text, mcp__timeln__ingest_url
metadata:
  openclaw:
    homepage: https://github.com/goodrahstar/timeln-secondbrain-skill
    install:
      - kind: npx
        package: skills
        args: ["add", "goodrahstar/timeln-secondbrain-skill"]
---

# Timeln Second Brain -- Your Thinking Partner

Your second brain, wired to the user's real Timeln account. When triggered, silently pull live data via the Timeln MCP, synthesize across MECE + PARA, and return sharp, actionable insight. No hallucination -- only real nodes and edges.

## Setup (one-time, user-side)

1. Sign up free at **https://timeln.app/signup**.
2. Get an API token: **Settings -> API Tokens -> Create** in the dashboard.
3. Add the hosted MCP to your agent config.

### Claude Code (`~/.claude.json`) or Cursor (`~/.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "timeln": {
      "url": "https://timeln-mcp-production.up.railway.app/mcp",
      "headers": {
        "Authorization": "Bearer tln_YOUR_TOKEN_HERE"
      }
    }
  }
}
```

No Python install required -- the MCP is hosted.

If `tln_...` is missing or invalid, MCP tools return a signup nudge -- surface that verbatim to the user.

## MCP tools you will call

| Tool | Purpose |
|---|---|
| `whoami` | Confirm token + return email/plan. Always call first. |
| `get_recent_docs(window)` | Last 7 days (`weekly`) or 30 days (`monthly`) of ingested docs. |
| `search_documents(limit, offset)` | Paginated list of all user documents. |
| `get_document(doc_id)` | Fetch a single document by id (with preview). |
| `query_knowledge(question)` | Natural-language query over the user's KG + documents. |
| `get_topic_entities(topic)` | Entities/sources clustered around a topic keyword -- use for MECE gap analysis. |
| `ingest_text(text, title?)` | Add new text content. |
| `ingest_url(url, title?)` | Add a public URL. |

Do not reimplement these -- always go through the MCP.

## Workflow

### Step 1 -- Identify the user
Call `whoami`. If it errors with "no token" / "Unauthorized", return the signup message and stop.

### Step 2 -- Pull recent context
Call `get_recent_docs(window="monthly")`. Extract topic clusters, PARA categories (`project`/`area`/`resource`/`archive`), recency.

### Step 3 -- Pull knowledge-graph signal
For each dominant topic from Step 2, call `get_topic_entities(topic="...")` to get entity clusters and their sources. For direct NL questions, call `query_knowledge(question="...")`.

### Step 4 -- Synthesize with MECE + PARA

**MECE gap analysis** -- map entities into four quadrants:

| Quadrant | Test | Finding |
|---|---|---|
| **Known** | High-frequency entities across many sources | Core expertise |
| **Emerging** | Mid-frequency, recent ingestions | Growing areas |
| **Isolated** | Few sources, weak cross-links | Latent gaps |
| **Missing** | Topics implied by adjacency but absent | Blind spots |

For each gap, write: `[Node A] -> SHOULD CONNECT TO -> [Node B]` -- backed by real data.

**PARA classification** from each doc's `para_category` field:
- **Projects** -- active, time-bound -> ship today
- **Areas** -- ongoing responsibilities -> maintain
- **Resources** -- reference material -> learn from
- **Archive** -- noise -> stop

### Step 5 -- Optional: interactive visualization

If the user asks for a graph, visual, or map (e.g. *"show my knowledge graph"*, *"visualise my brain"*, *"plot my topics"*), the skill handles everything -- no scripts to run:

1. Call `get_topic_entities` for each relevant topic surfaced in steps 3-4.
2. Merge results into `{nodes, links}` -- each node is an entity, each link is a relationship or shared document.
3. Inject the graph data into `kg_interactive_template.html` (replace `__GRAPH_DATA__`) and write the result as `kg_interactive.html` in the workspace root.
4. Open the file so the user sees it immediately.

The user never leaves the chat window -- just ask in natural language and the skill produces a ready-to-open HTML file.

## Output format (always)

```
## Your Brain, Right Now
[1-2 sentence synthesis of what the data shows you're building]

## MECE Map
| | Connected | Isolated |
|---|---|---|
| **Known** | [real nodes] | [real gaps] |
| **Emerging** | [real nodes] | [missing bridges] |

## PARA -- What to Do Today
**Project (ship):** [1-3 hr action tied to a real project node]
**Area (deepen):** [real concept to go deeper on]
**Resource (learn):** [specific saved doc you haven't connected yet]
**Archive (stop):** [what's noise -- backed by data]

## The One Sentence
> [Single sharpest insight from the data]
```

## Handling specific questions

When the user asks a concrete question (not a general "second brain" prompt):

1. `query_knowledge(question="<their question>")` -- NL over their graph + documents.
2. `search_documents` or `get_recent_docs` for titles to cite.
3. Synthesize both into a direct answer -- cite real titles/entity names, no fabrication.

## Rules

- Always go through MCP tools. Never call infrastructure directly.
- Never fabricate node names, titles, or relationships. If a tool returns nothing, say so.
- Never include the user's API token in any output or tool echo.

For examples, see [EXAMPLES.md](EXAMPLES.md).
For MCP API reference, see [REFERENCE.md](REFERENCE.md).
