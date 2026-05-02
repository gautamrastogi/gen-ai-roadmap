#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


TRACKER_PATH = Path(__file__).resolve().parent.parent / "data" / "TOKEN_SAVINGS_TRACKER.csv"


def parse_int(value: str) -> int:
    value = (value or "").strip()
    if not value:
        return 0
    try:
        return int(value)
    except ValueError:
        return 0


def main() -> int:
    if not TRACKER_PATH.exists():
        print(f"Tracker file not found: {TRACKER_PATH}")
        return 1

    baseline_tokens = 0
    hybrid_tokens = 0
    baseline_count = 0
    hybrid_count = 0
    total_local_calls = 0
    total_local_latency = 0
    latency_rows = 0

    with TRACKER_PATH.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            mode = (row.get("mode") or "").strip().lower()
            tokens = parse_int(row.get("total_cloud_tokens", "0"))
            local_calls = parse_int(row.get("local_mcp_calls", "0"))
            local_latency = parse_int(row.get("avg_local_latency_ms", "0"))

            total_local_calls += local_calls
            if local_latency > 0:
                total_local_latency += local_latency
                latency_rows += 1

            if mode == "baseline":
                baseline_tokens += tokens
                baseline_count += 1
            elif mode == "hybrid":
                hybrid_tokens += tokens
                hybrid_count += 1

    print("=== Token Savings Report ===")
    print(f"Baseline tasks: {baseline_count}")
    print(f"Hybrid tasks:   {hybrid_count}")
    print(f"Baseline tokens total: {baseline_tokens}")
    print(f"Hybrid tokens total:   {hybrid_tokens}")
    print(f"Total local MCP calls: {total_local_calls}")
    if latency_rows > 0:
        print(f"Avg local latency: {round(total_local_latency / latency_rows, 2)} ms")
    else:
        print("Avg local latency: n/a")

    if baseline_tokens <= 0:
        print("Savings: n/a (baseline token total is zero)")
        return 0

    savings = ((baseline_tokens - hybrid_tokens) / baseline_tokens) * 100
    print(f"Estimated cloud token savings: {round(savings, 2)}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
