---
name: timeln-second-brain
description: >-
  Acts as the user's virtual second brain — pulls real data from their Timeln
  account (documents + knowledge graph) via the Timeln MCP server, applies MECE
  gap analysis and the PARA framework, then returns crisp learning/action
  recommendations and optionally a D3 knowledge-graph visualization. Trigger
  whenever the user says "second brain", "thinking partner", "knowledge
  partner", "what should I learn today", "what should I do today", "connect my
  ideas", "show my knowledge gaps", "build a knowledge graph", or "what's in
  my brain", or asks for insight from their past ingested data. Also trigger
  when the user asks any question prefixed with "based on my past data",
  "based on what I've learned", or "from my knowledge graph". Always use this
  skill — never guess from memory alone.
---

# Timeln Second Brain — Your Thinking Partner

Your second brain, wired to the user's real Timeln account. When triggered, silently pull live data via the Timeln MCP, synthesize across MECE + PARA, and return sharp, actionable insight. No hallucination — only real nodes and edges.

## Setup (one-time, user-side)

1. Sign up free at **https://timeln.app/signup**.
2. Get an API token: **Settings → API Tokens → Create** in the dashboard.
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

No Python install required — the MCP is hosted. (For self-host, see README.)

If `tln_...` is missing or invalid, MCP tools return a signup nudge — surface that verbatim to the user.

## MCP tools you will call

| Tool | Purpose |
|---|---|
| `whoami` | Confirm token + return email/plan. Always call first. |
| `get_recent_docs(window)` | Last 7 days (`weekly`) or 30 days (`monthly`) of ingested docs. |
| `search_documents(limit, offset)` | Paginated list of all user documents. |
| `get_document(doc_id)` | Fetch a single document by id (with preview). |
| `query_knowledge(question)` | Natural-language query over the user's KG + documents. |
| `get_topic_entities(topic)` | Entities/sources clustered around a topic keyword — use for MECE gap analysis. |
| `ingest_text(text, title?)` | Add new text content. |
| `ingest_url(url, title?)` | Add a public URL. |

Do not reimplement these — always go through the MCP.

## Workflow

### Step 1 — Identify the user
Call `whoami`. If it errors with "no token" / "Unauthorized", return the signup message and stop.

### Step 2 — Pull recent context
Call `get_recent_docs(window="monthly")`. Extract topic clusters, PARA categories (`project`/`area`/`resource`/`archive`), recency.

### Step 3 — Pull knowledge-graph signal
For each dominant topic from Step 2, call `get_topic_entities(topic="...")` to get entity clusters and their sources. For direct NL questions, call `query_knowledge(question="...")`.

### Step 4 — Synthesize with MECE + PARA

**MECE gap analysis** — map entities into four quadrants:

| Quadrant | Test | Finding |
|---|---|---|
| **Known** | High-frequency entities across many sources | Core expertise |
| **Emerging** | Mid-frequency, recent ingestions | Growing areas |
| **Isolated** | Few sources, weak cross-links | Latent gaps |
| **Missing** | Topics implied by adjacency but absent | Blind spots |

For each gap, write: `[Node A] → SHOULD CONNECT TO → [Node B]` — backed by real data.

**PARA classification** from each doc's `para_category` field:
- **Projects** — active, time-bound → ship today
- **Areas** — ongoing responsibilities → maintain
- **Resources** — reference material → learn from
- **Archive** — noise → stop

### Step 5 — Optional: interactive visualization

If the user asks for a graph/visual/plot, run:

```
python references/build_kg_interactive.py --topics "topic1,topic2,..."
```

It calls `get_topic_entities` for each topic via the MCP, merges into `{nodes, links}`, injects into `references/kg_interactive_template.html`, and writes `kg_interactive.html` to the workspace root. Then `open kg_interactive.html`.

Template features: scroll to zoom, drag to pan, click node to focus, double-click to reset, search box, legend filtering, hover tooltips, dashed red "gap" edges.

## Output format (always)

```
## Your Brain, Right Now
[1–2 sentence synthesis of what the data shows you're building]

## MECE Map
| | Connected | Isolated |
|---|---|---|
| **Known** | [real nodes] | [real gaps] |
| **Emerging** | [real nodes] | [missing bridges] |

## PARA — What to Do Today
**Project (ship):** [1–3 hr action tied to a real project node]
**Area (deepen):** [real concept to go deeper on]
**Resource (learn):** [specific saved doc you haven't connected yet]
**Archive (stop):** [what's noise — backed by data]

## The One Sentence
> [Single sharpest insight from the data]
```

## Handling specific questions

When the user asks a concrete question (not a general "second brain" prompt):

1. `query_knowledge(question="<their question>")` — NL over their graph + documents.
2. `search_documents` or `get_recent_docs` for titles to cite.
3. Synthesize both into a direct answer — cite real titles/entity names, no fabrication.

## Reference files

| File | Role |
|---|---|
| `references/build_kg_interactive.py` | Batch topic queries → `kg_interactive.html`. |
| `references/kg_interactive_template.html` | D3 force-graph template (`__GRAPH_DATA__`). |

## Rules

- Always go through MCP tools. Never call infrastructure directly.
- Never fabricate node names, titles, or relationships. If a tool returns nothing, say so.
- Never include the user's API token in any output or tool echo.
