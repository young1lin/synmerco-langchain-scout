#!/usr/bin/env python3
"""Scout Synmerco agents via free synmerco-langchain tools (no API keys)."""
from __future__ import annotations

import argparse
import json
import sys

from synmerco_langchain import get_synmerco_tools


def _tool_map():
    return {t.name: t for t in get_synmerco_tools(include_free_only=True)}


def _as_dict(result):
    if isinstance(result, str):
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return {"raw": result}
    if hasattr(result, "model_dump"):
        return result.model_dump()
    if isinstance(result, dict):
        return result
    return {"raw": result}


def _agents_from(payload):
    if isinstance(payload, list):
        return payload
    if not isinstance(payload, dict):
        return []
    for key in ("agents", "results", "data", "items"):
        val = payload.get(key)
        if isinstance(val, list):
            return val
        if isinstance(val, dict):
            for key2 in ("agents", "results", "items"):
                if isinstance(val.get(key2), list):
                    return val[key2]
    return []


def _pick(agent: dict) -> dict:
    # Print only agentDid, synmercoScore, tier, capabilities
    did = (
        agent.get("agentDid")
        or agent.get("did")
        or agent.get("id")
        or agent.get("agent_did")
    )
    score = agent.get("synmercoScore")
    if score is None:
        score = agent.get("score")
    tier = agent.get("tier") or agent.get("reputationTier")
    caps = agent.get("capabilities") or agent.get("capability") or []
    if isinstance(caps, str):
        caps = [caps]
    return {
        "agentDid": did,
        "synmercoScore": score,
        "tier": tier,
        "capabilities": caps,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "capability",
        help="Capability to search for (e.g. coding, research, writing)",
    )
    args = parser.parse_args(argv)

    tools = _tool_map()
    for required in ("search_agents", "lookup_trust_score", "estimate_fees"):
        if required not in tools:
            print(f"missing tool: {required}", file=sys.stderr)
            return 1

    search = tools["search_agents"].invoke(
        {"capability": args.capability, "limit": 3}
    )
    search_payload = _as_dict(search)
    agents = _agents_from(search_payload)[:3]

    print(f"# search_agents capability={args.capability!r} (up to 3)")
    picked = [_pick(a) for a in agents]
    print(json.dumps(picked, indent=2, default=str))

    if not picked or not picked[0].get("agentDid"):
        print("No agents returned; skipping lookup_trust_score", file=sys.stderr)
        return 2

    first_did = picked[0]["agentDid"]
    trust = tools["lookup_trust_score"].invoke({"did": first_did})
    print(f"\n# lookup_trust_score did={first_did}")
    # Prefer only safe fields if nested
    trust_payload = _as_dict(trust)
    if isinstance(trust_payload, dict):
        safe = {
            k: trust_payload.get(k)
            for k in (
                "agentDid",
                "did",
                "synmercoScore",
                "score",
                "tier",
                "reputationTier",
                "capabilities",
                "transactionCount",
                "completedJobs",
            )
            if k in trust_payload
        }
        print(json.dumps(safe or trust_payload, indent=2, default=str))
    else:
        print(trust_payload)

    fees = tools["estimate_fees"].invoke({"amount": 10000})
    print("\n# estimate_fees amount=10000 (100 USD)")
    print(json.dumps(_as_dict(fees), indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
