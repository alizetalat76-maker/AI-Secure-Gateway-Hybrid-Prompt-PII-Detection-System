"""
run_evaluation.py
-----------------
Runs all prompts from data/final_eval.csv through the gateway API
and prints accuracy, precision, recall, F1, and latency stats.

Make sure the server is running first:
    uvicorn app.main:app --reload
"""

import pandas as pd
import requests
from sklearn.metrics import classification_report, confusion_matrix

API_URL  = "http://localhost:8000/analyze"
DATA_CSV = "data/final_eval.csv"
OUT_CSV  = "results/evaluation_results.csv"

print("Loading dataset...")
df = pd.read_csv(DATA_CSV)
print(f"Total prompts: {len(df)}")

results = []
errors  = 0

for i, row in df.iterrows():
    try:
        resp = requests.post(
            API_URL,
            json={"text": row["prompt"], "input_id": str(row["id"])},
            timeout=30
        )
        data = resp.json()

        results.append({
            "id":             row["id"],
            "prompt":         row["prompt"],
            "language":       row["language"],
            "attack_type":    row["attack_type"],
            "expected":       row["expected_policy"],
            "predicted":      data["decision"],
            "rule_score":     data["rule_score"],
            "semantic_score": data["semantic_score"],
            "final_risk":     data["final_risk"],
            "latency_ms":     data["latency_ms"],
        })

    except Exception as e:
        print(f"  Error on row {row['id']}: {e}")
        errors += 1

print(f"\nCompleted: {len(results)} prompts | Errors: {errors}")

# Save results
out = pd.DataFrame(results)
out.to_csv(OUT_CSV, index=False)
print(f"Results saved to {OUT_CSV}")

# ---- Metrics ----
print("\n========== CLASSIFICATION REPORT ==========")
print(classification_report(out["expected"], out["predicted"]))

print("========== CONFUSION MATRIX ==========")
labels = ["ALLOW", "MASK", "BLOCK"]
cm = confusion_matrix(out["expected"], out["predicted"], labels=labels)
print(f"{'':10}", "  ".join(f"{l:6}" for l in labels))
for label, row_vals in zip(labels, cm):
    print(f"{label:10}", "  ".join(f"{v:6}" for v in row_vals))

# ---- Latency ----
print("\n========== LATENCY SUMMARY ==========")
print(f"Mean latency  : {out['latency_ms'].mean():.1f} ms")
print(f"Median latency: {out['latency_ms'].median():.1f} ms")
print(f"P95 latency   : {out['latency_ms'].quantile(0.95):.1f} ms")
print(f"Max latency   : {out['latency_ms'].max()} ms")

# ---- Per-language breakdown ----
print("\n========== PER LANGUAGE BREAKDOWN ==========")
for lang, group in out.groupby("language"):
    correct = (group["expected"] == group["predicted"]).sum()
    total   = len(group)
    print(f"  {lang:6}: {correct}/{total} correct ({100*correct/total:.0f}%)")

# ---- False positives and negatives ----
fp = out[(out["expected"] != "BLOCK") & (out["predicted"] == "BLOCK")]
fn = out[(out["expected"] == "BLOCK") & (out["predicted"] != "BLOCK")]

print(f"\nFalse Positives (wrongly blocked): {len(fp)}")
for _, r in fp.iterrows():
    print(f"  [{r['id']}] {r['prompt'][:70]}")

print(f"\nFalse Negatives (missed attacks): {len(fn)}")
for _, r in fn.iterrows():
    print(f"  [{r['id']}] {r['prompt'][:70]}")
