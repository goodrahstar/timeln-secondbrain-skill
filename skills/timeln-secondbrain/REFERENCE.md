# MCP API Reference

All tools are provided by the hosted Timeln MCP server at:
`https://timeln-mcp-production.up.railway.app/mcp`

Authentication: `Authorization: Bearer tln_YOUR_TOKEN_HERE` header.

---

## whoami

Confirm the token is valid and return the authenticated user's info.

**Parameters:** none

**Returns:**
```json
{
  "email": "user@example.com",
  "plan": "free",
  "document_count": 142
}
```

**On failure:** returns a signup nudge string -- surface it verbatim to the user.

---

## get_recent_docs

Fetch documents ingested in the last 7 or 30 days.

**Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `window` | string | `"monthly"` | `"weekly"` (7 days) or `"monthly"` (30 days) |

**Returns:** array of document objects with `id`, `title`, `url`, `summary`, `topics`, `para_category`, `created_at`.

---

## search_documents

Paginated list of all documents in the user's library.

**Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `limit` | int | 20 | Max results per page |
| `offset` | int | 0 | Pagination offset |

**Returns:** `{ total, documents: [...] }`

---

## get_document

Fetch a single document by ID with full preview text.

**Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| `doc_id` | string | Document ID from search_documents or get_recent_docs |

**Returns:** full document object including `preview_text`, `entities`, `graph_edges`.

---

## query_knowledge

Natural-language query over the user's full knowledge graph and documents.

**Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| `question` | string | Any natural language question |

**Returns:** answer string with cited document titles/IDs.

---

## get_topic_entities

Entities and source documents clustered around a topic keyword.

**Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| `topic` | string | Topic keyword (e.g. "AI agents", "marketing", "retention") |

**Returns:**
```json
{
  "topic": "AI agents",
  "entities": [
    { "name": "LangChain", "frequency": 8, "sources": ["doc_1", "doc_4"] },
    { "name": "MCP", "frequency": 5, "sources": ["doc_2"] }
  ],
  "edges": [
    { "source": "LangChain", "target": "MCP", "weight": 3 }
  ]
}
```

---

## ingest_text

Add plain text content to the user's Timeln library.

**Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `text` | string | yes | The text content to save |
| `title` | string | no | Optional title |

---

## ingest_url

Add a public URL to the user's Timeln library.

**Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `url` | string | yes | Public URL to ingest |
| `title` | string | no | Optional override title |

---

## Visualization template

`kg_interactive_template.html` -- D3 force-graph template included in this skill folder.

Replace `__GRAPH_DATA__` with a JSON object: `{ nodes: [...], links: [...] }`.

Node shape: `{ id, label, group, frequency }`
Link shape: `{ source, target, weight, type }` -- set `type: "gap"` for dashed red gap edges.

Features: scroll to zoom, drag to pan, click node to focus, double-click to reset,
search box, legend filter, hover tooltips.
