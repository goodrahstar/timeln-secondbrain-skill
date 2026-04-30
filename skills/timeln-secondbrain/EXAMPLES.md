# Examples

## "second brain" -- daily debrief

**User:** second brain, what should I ship today?

**Agent** (after calling `whoami`, `get_recent_docs`, `get_topic_entities` on 4 topics):

```
## Your Brain, Right Now
The last 30 days skew heavily toward shipping an MCP + knowledge-graph product,
with fresh but disconnected reading on cold outreach and landing-page CRO.

## MECE Map
|             | Connected                              | Isolated                                              |
|-------------|----------------------------------------|-------------------------------------------------------|
| **Known**   | marketing, SEO, social media           | design tools (saved 3 docs, zero edges to rest)       |
| **Emerging**| paid ads, content strategy             | cold-email deliverability (4 docs, no GTM bridge)     |

## PARA -- What to Do Today
**Project (ship):** Finish the hosted MCP endpoint -- two of your last five docs
  are about remote MCP transports.
**Area (deepen):** Knowledge-graph query routing -- you have 12 nodes under
  "Graph RAG" but only 2 edges into "query strategy".
**Resource (learn):** "SMTP warm-up playbook" (saved 6 days ago, never revisited).
  It bridges your cold-outreach gap.
**Archive (stop):** The three personal-finance articles -- fully disconnected from
  everything else, pure noise.

## The One Sentence
> Your graph says you're one bridge -- "cold outreach -> GTM loop" -- away from
> turning the product work into real distribution.
```

---

## "based on my past data" -- specific question

**User:** Based on my past data, what do I know about retention strategy?

**Agent:**

```
Querying your knowledge graph for "retention strategy"...

Found 7 relevant documents:
1. "The Hook Model" (saved 3 weeks ago) -- Nir Eyal's trigger-action-reward loop
2. "SaaS Churn Benchmarks 2024" (saved 1 month ago) -- industry data
3. "Onboarding email sequences" (saved 2 weeks ago) -- activation tactics

Cross-links I found:
- "Hook Model" connects to "onboarding sequences" via shared entity: "habit formation"
- Gap: you have zero saves on "pricing and retention" -- a common blind spot

Your current knowledge: strong on activation (onboarding), weak on long-term
habit design and pricing-as-retention.
```

---

## "show my knowledge graph" -- visualization

**User:** Show my knowledge graph for AI agents

**Agent:**

Calls `get_topic_entities` for "AI agents", "MCP", "LLM", builds node/link data,
injects into `kg_interactive_template.html`, opens `kg_interactive.html`.

The user sees an interactive D3 force graph in their browser -- drag, zoom, click
nodes to follow sources, search by name, filter by topic cluster.

---

## Trigger phrases

Any of these kick off the skill automatically:

- `second brain` / `thinking partner` / `knowledge partner`
- `what should I learn today?` / `what should I do today?`
- `connect my ideas` / `show my knowledge gaps`
- `build a knowledge graph` / `what's in my brain?`
- `based on my past data, ...`
- `based on what I've learned, ...`
- `from my knowledge graph, ...`
