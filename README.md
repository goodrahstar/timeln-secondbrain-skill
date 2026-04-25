<p align="center">
  <img src="docs/ascii-banner.svg" alt="TIMELN SECOND BRAIN" width="760" />
</p>

<h1 align="center">Timeln Second Brain</h1>

<p align="center">
  <em>A second brain for your AI, wired to your own knowledge graph.</em>
</p>

<p align="center">
  <a href="https://timeln.app/download/skill"><img alt="Docs" src="https://img.shields.io/badge/docs-timeln.app-ea580c?style=flat-square" /></a>
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/license-MIT-black?style=flat-square" /></a>
  <a href="https://modelcontextprotocol.io"><img alt="MCP" src="https://img.shields.io/badge/MCP-compatible-6366f1?style=flat-square" /></a>
  <a href="https://claude.com/claude-code"><img alt="Claude Code" src="https://img.shields.io/badge/Claude%20Code-ready-d97706?style=flat-square" /></a>
  <a href="https://timeln.app/signup"><img alt="Get Timeln" src="https://img.shields.io/badge/Try%20on-timeln.app-ea580c?style=flat-square" /></a>
</p>

<p align="center">
  <img src="docs/demo.gif" alt="Demo" width="720" />
</p>

```bash
git clone https://github.com/timeln/timeln-second-brain ~/.claude/skills/timeln-second-brain
```

**What you get:**
- 🧠 Your AI answers grounded in **your** documents — no hallucinations.
- 🗺️ MECE gap analysis + PARA framework, applied live to your real knowledge graph.
- 📊 One command away from an interactive D3 visualization of what you know.

See it live: **[timeln.app/download/skill](https://timeln.app/download/skill)** · Read the launch post: **[timeln.app/blog/timeln-second-brain-skill](https://timeln.app/blog/timeln-second-brain-skill)**

---

## What is this?

A Claude Code / Cursor skill that turns your Timeln library into a live second brain for your AI. Ask *"what should I learn today?"* or *"connect my ideas"* and get answers grounded in the documents and knowledge graph you've actually built — no hallucinations.

It works by:
- **`SKILL.md`** — the reasoning recipe (MECE gap analysis + PARA + D3 viz).
- **Hosted Timeln MCP** — a Model Context Protocol server that bridges your agent to the Timeln REST API. No Python, no local daemon.
- **Your Timeln account** — where the real data lives.

No Timeln account → the skill loads, but tools return a friendly *"sign up at timeln.app"* nudge. One signup at **[timeln.app/signup](https://timeln.app/signup)** and everything lights up.

---

## 60-second install

### 1 — Sign up & grab a token

1. **[timeln.app/signup](https://timeln.app/signup)** — free, Google SSO, no credit card.
2. Save a few links with the [Chrome extension](https://chromewebstore.google.com/) or paste them into the dashboard.
3. **[app.timeln.app](https://app.timeln.app) → Settings → API Tokens → Create**. Copy the `tln_...` token (shown once).

### 2 — Add the skill to your agent

```bash
git clone https://github.com/timeln/timeln-second-brain ~/.claude/skills/timeln-second-brain
```

Claude Code and Cursor both auto-discover `SKILL.md` files in these folders:
- Claude Code: `~/.claude/skills/`
- Cursor: `~/.cursor/skills/` (or `.cursor/skills/` inside a project)

### 3 — Point your agent at the hosted MCP

#### Claude Code — `~/.claude.json`

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

#### Cursor — `~/.cursor/mcp.json`

Same JSON as above.

Restart your agent. Type `/mcp` to confirm `timeln` is listed with a green dot.

### 4 — Try it

```
second brain, what should I ship today?
what should I learn today?
based on my past data, what are my biggest gaps?
```

The skill triggers automatically on any of those phrases.

---

## What the skill does

1. Calls `whoami` to confirm your token.
2. Pulls your recent documents (`get_recent_docs`) and subgraphs by topic (`get_topic_entities`).
3. Applies **MECE gap analysis** (known / emerging / isolated / missing) and **PARA** (projects / areas / resources / archive).
4. Returns a crisp, opinionated recommendation.
5. Optionally generates an interactive D3 force-graph (`kg_interactive.html`).

See [`examples/second-brain.md`](examples/second-brain.md) for a sample output.

---

## MCP tools exposed

| Tool | Purpose |
|---|---|
| `whoami` | Confirm token, return email + plan. |
| `get_recent_docs(window)` | Docs from the last "weekly" or "monthly" window. |
| `search_documents(limit, offset)` | Paginated list of all your documents. |
| `get_document(doc_id)` | Single document by id. |
| `query_knowledge(question)` | Natural-language query over your KG + docs. |
| `get_topic_entities(topic)` | Entities + sources connected to a topic. |
| `ingest_text(text, title?)` | Add plain text to your Timeln library. |
| `ingest_url(url, title?)` | Add a public URL. |

All tools forward the bearer token from the `Authorization` header.

---

## Self-hosting the MCP (optional)

Prefer to run the MCP in-process instead of calling the hosted one? It's a single Python file:

```bash
pip install -r mcp/requirements.txt
```

Then use this config instead:

```json
{
  "mcpServers": {
    "timeln": {
      "command": "python",
      "args": ["/absolute/path/to/timeln-second-brain/mcp/server.py"],
      "env": { "TIMELN_API_TOKEN": "tln_YOUR_TOKEN_HERE" }
    }
  }
}
```

See [`mcp/README.md`](mcp/README.md) for env vars and SSE transport details.

### Self-hosting Timeln itself

Pointing at a self-hosted Timeln backend? Override the base URL on either transport:

- **Hosted MCP** → not applicable; use self-host option below.
- **Local MCP** → set `TIMELN_API_BASE_URL=https://your-timeln.example.com` in the `env` block.

---

## Trigger phrases

Say any of these to your agent:

- "second brain" • "thinking partner" • "knowledge partner"
- "what should I learn today?" / "what should I do today?"
- "connect my ideas" • "show my knowledge gaps"
- "build a knowledge graph" • "what's in my brain?"
- "based on my past data, ..."

---

## License

MIT — see [LICENSE](LICENSE).
