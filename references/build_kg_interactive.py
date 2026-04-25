#!/usr/bin/env python3
"""Build kg_interactive.html by pulling topic subgraphs from the Timeln REST API.

Usage:
    python build_kg_interactive.py --topics "Claude,MCP,LLM,Founder,GTM"

Env:
    TIMELN_API_TOKEN       required — bearer token from timeln.app
    TIMELN_API_BASE_URL    optional — defaults to https://apis.timeln.app
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from urllib.parse import quote

import httpx

REF = Path(__file__).resolve().parent
TEMPLATE = REF / "kg_interactive_template.html"
OUT = Path.cwd() / "kg_interactive.html"

API_BASE = os.getenv("TIMELN_API_BASE_URL", "https://apis.timeln.app").rstrip("/")


def fetch_topic(client: httpx.Client, topic: str) -> dict:
    """Pull entities and their sources for a topic, and shape them into
    {nodes, links} so the D3 template can render them.

    The MCP's `get_topic_entities` tool calls the entity-extraction endpoint,
    which returns a flat list of entities grouped by source (KG, document
    context, neighbor search). We convert that into a simple hub-and-spoke
    graph where the topic is the hub and each entity is a spoke.
    """
    r = client.post(
        f"{API_BASE}/api/playground/analytics/entity-extraction",
        json={"question": topic},
    )
    r.raise_for_status()
    payload = r.json()

    nodes: list[dict] = [{"id": topic, "cluster": slugify(topic), "degree": 0, "kind": "topic"}]
    links: list[dict] = []
    seen: set[str] = {topic}

    by_source = payload.get("entities_by_source", {})
    for source_name, bucket in by_source.items():
        for ent in bucket.get("entities", []) or []:
            if not ent or ent in seen:
                continue
            seen.add(ent)
            nodes.append({"id": ent, "cluster": slugify(topic), "degree": 0, "kind": source_name})
            links.append({"source": topic, "target": ent, "rel": source_name, "gap": False})

    return {"nodes": nodes, "links": links}


def slugify(topic: str) -> str:
    return topic.lower().replace(" ", "_").replace("-", "_")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--topics",
        required=True,
        help="Comma-separated list of topic keywords (e.g. 'Claude,MCP,LLM').",
    )
    args = ap.parse_args()

    token = os.getenv("TIMELN_API_TOKEN")
    if not token:
        sys.exit(
            "TIMELN_API_TOKEN not set. Sign up at https://timeln.app/signup "
            "and copy a token from Settings → API Tokens."
        )

    topics = [t.strip() for t in args.topics.split(",") if t.strip()]

    node_map: dict[str, dict] = {}
    links: list[dict] = []
    seen: set[tuple[str, str, str]] = set()

    headers = {"Authorization": f"Bearer {token}"}
    with httpx.Client(timeout=30.0, headers=headers) as client:
        for topic in topics:
            cluster = slugify(topic)
            try:
                sub = fetch_topic(client, topic)
            except httpx.HTTPStatusError as e:
                print(f"  ! {topic}: {e.response.status_code}", file=sys.stderr)
                continue

            for node in sub.get("nodes", []):
                nid = node.get("id") or node.get("name")
                if not nid:
                    continue
                if nid not in node_map:
                    node_map[nid] = {"id": nid, "cluster": cluster, "degree": 0}

            for link in sub.get("links", []):
                src = link.get("source") or link.get("from")
                tgt = link.get("target") or link.get("to")
                rel = link.get("rel") or link.get("type", "RELATED")
                if not src or not tgt:
                    continue
                key = (src, tgt, rel)
                if key in seen:
                    continue
                seen.add(key)
                links.append(
                    {"source": src, "target": tgt, "rel": rel, "gap": False}
                )
                node_map.setdefault(
                    src, {"id": src, "cluster": cluster, "degree": 0}
                )
                node_map.setdefault(
                    tgt, {"id": tgt, "cluster": cluster, "degree": 0}
                )

    for e in links:
        if e["source"] in node_map:
            node_map[e["source"]]["degree"] += 1
        if e["target"] in node_map:
            node_map[e["target"]]["degree"] += 1

    graph_data = {"nodes": list(node_map.values()), "links": links}
    payload = json.dumps(graph_data, ensure_ascii=False)

    html = TEMPLATE.read_text(encoding="utf-8")
    if "__GRAPH_DATA__" not in html:
        sys.exit("Template missing __GRAPH_DATA__ placeholder")
    OUT.write_text(html.replace("__GRAPH_DATA__", payload), encoding="utf-8")
    print(f"Wrote {OUT} ({len(graph_data['nodes'])} nodes, {len(links)} edges)")


if __name__ == "__main__":
    main()
