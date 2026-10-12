"""Validate and summarize the completed ISTI batch; never fill missing values.

python3 tools/benchmark/isti-summary.py doc/measurements/isti-100
"""
import csv
import importlib.util
import json
from pathlib import Path
import statistics
import sys

out = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("batch", Path(__file__).with_name("isti-batch.py"))
batch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(batch)
manifest = json.loads((out / "selection.json").read_text())
states = {p.stem: json.loads(p.read_text()) for p in (out / "models").glob("*.json")}
batch.write_csv(out, manifest["models"], states)
rows = list(csv.DictReader((out / "results.csv").open()))
assert len(rows) == 2 * manifest["count"]
assert len({(r["model_id"], r["quality_target_pixels"]) for r in rows}) == len(rows)
finished = sum(s.get("finished", False) for s in states.values())
counts = {status: sum(s["status"] == status for s in states.values())
          for status in sorted({s["status"] for s in states.values()})}
summary = {"selected_models": manifest["count"], "finished_models": finished,
           "status_counts": counts, "quality_targets": {}}
for tau in batch.TAUS:
    candidates = [r for r in rows if float(r["quality_target_pixels"]) == tau]
    valid = [r for r in candidates if r["round1_allocation_audit_passed"] == "True"
             and r["round2_allocation_audit_passed"] == "True"
             and r["round2_geometry_matches_round1"] == "True"
             and r["round2_comparison_has_foreground"] == "True"]
    savings = [float(r["round2_vs_round1_gpu_saving_pct"]) for r in valid]
    changed = [float(r["round2_vs_round1_textured_changed_pixels_over_8_fraction"]) * 100 for r in valid]
    r1 = sum(int(r["round1_gpu_bytes"]) for r in valid)
    r2 = sum(int(r["round2_gpu_bytes"]) for r in valid)
    def quartiles(values):
        if not values:
            return {}
        q = statistics.quantiles(values, n=4, method="inclusive") if len(values) > 1 else [values[0]] * 3
        return {"min": min(values), "q25": q[0], "median": statistics.median(values),
                "q75": q[2], "max": max(values), "mean": statistics.mean(values)}
    summary["quality_targets"][str(tau)] = {
        "valid_round2_comparisons": len(valid), "complete_control_comparisons": sum(r["row_measurement_complete"] == "True" for r in valid),
        "round2_gpu_saving_pct": quartiles(savings), "size_weighted_gpu_saving_pct": 100 * (1 - r2 / r1) if r1 else None,
        "positive_saving_models": sum(x > 0.01 for x in savings), "saving_over_10pct_models": sum(x >= 10 for x in savings),
        "saving_over_25pct_models": sum(x >= 25 for x in savings), "increased_cache_models": sum(x < -0.01 for x in savings),
        "identical_textured_models": sum(r["round2_vs_round1_textured_identical"] == "True" for r in valid),
        "identical_shaded_models": sum(r["round2_vs_round1_shaded_identical"] == "True" for r in valid),
        "changed_pixels_over_8_pct": quartiles(changed), "models_with_more_than_1pct_changed_pixels": sum(x > 1 for x in changed),
        "positive_saving_and_at_most_1pct_changed_pixels": sum(s > 0.01 and c <= 1 for s, c in zip(savings, changed)),
        "all_nodes_resident_round1": sum(r["round1_resident_nodes"] == r["round1_total_nodes"] for r in valid),
        "all_nodes_resident_round2": sum(r["round2_resident_nodes"] == r["round2_total_nodes"] for r in valid),
    }
    controlled = [r for r in valid if r["row_measurement_complete"] == "True" and
                  r["control_geometry_matches_round1"] == "True" and
                  r["control_texture_payload_matches_round1"] == "True"]
    detailed = summary["quality_targets"][str(tau)]
    detailed["control_payload_matched_models"] = len(controlled)
    detailed["round1_vs_control_gpu_ratio"] = quartiles([float(r["round1_vs_control_gpu_ratio"]) for r in controlled])
    for label in batch.LABELS:
        detailed[label + "_source_relative_textured_psnr_db_finite"] = quartiles([
            float(r[label + "_vs_source_textured_psnr_db"]) for r in controlled
            if r[label + "_vs_source_textured_psnr_db"] != ""])
    detailed["round1_minus_control_source_psnr_db"] = quartiles([
        float(r["round1_vs_source_textured_psnr_db"]) - float(r["control_vs_source_textured_psnr_db"])
        for r in controlled if r["round1_vs_source_textured_psnr_db"] and r["control_vs_source_textured_psnr_db"]])
    detailed["round2_minus_round1_source_psnr_db"] = quartiles([
        float(r["round2_vs_source_textured_psnr_db"]) - float(r["round1_vs_source_textured_psnr_db"])
        for r in controlled if r["round2_vs_source_textured_psnr_db"] and r["round1_vs_source_textured_psnr_db"]])
    for r in valid:
        assert r["round1_gpu_bytes"] != "" and r["round2_gpu_bytes"] != ""
        for label in ("round1", "round2"):
            assert int(r[label + "_gpu_bytes"]) == int(r[label + "_geometry_bytes"]) + int(r[label + "_texture_bytes"])
summary["control_geometry_mismatch_models"] = sorted({r["model_id"] for r in rows if r["control_geometry_matches_round1"] == "False"})
summary["round2_geometry_mismatch_models"] = sorted({r["model_id"] for r in rows if r["round2_geometry_matches_round1"] == "False"})
summary["incomplete_model_ids"] = [m["model_id"] for m in manifest["models"] if not states.get(m["model_id"], {}).get("finished")]
summary["failed_model_ids"] = [mid for mid, state in states.items() if state["status"] != "ok"]
batch.atomic_json(out / "summary.json", summary)
lines = ["# Aggregate ISTI results", "", f"Completed {finished} of {manifest['count']} selected models.",
         "", "[Plotting CSV](graph.csv) · [Detailed CSV](results.csv) · [Method and columns](README.md)", "",
         "GPU savings compare round 2 with round 1 at the same camera and quality target. Models receive equal weight in medians; byte-weighted savings compare the sum of cache bytes.", "",
         "| Target pixels | Valid models | Models saving cache | Median saving | Mean saving | Byte-weighted saving | Models saving ≥25% | Models with >1% changed pixels |",
         "|---:|---:|---:|---:|---:|---:|---:|---:|"]
for tau, q in summary["quality_targets"].items():
    if not q["valid_round2_comparisons"]:
        continue
    lines.append(f"| {tau} | {q['valid_round2_comparisons']} | {q['positive_saving_models']} | "
                 f"{q['round2_gpu_saving_pct']['median']:.2f}% | {q['round2_gpu_saving_pct']['mean']:.2f}% | "
                 f"{q['size_weighted_gpu_saving_pct']:.2f}% | {q['saving_over_25pct_models']} | "
                 f"{q['models_with_more_than_1pct_changed_pixels']} |")
lines += ["", "Changed pixels use an 8/255 maximum RGB-channel difference over foreground pixels. This threshold is a diagnostic, not a perceptual equivalence guarantee.", "",
          "| Target pixels | All nodes resident in round 1 | Identical textured images | Identical shaded images | Median round 1/control cache ratio | Median source-relative PSNR improvement, round 1/control | Median source-relative PSNR change, round 2/round 1 |",
          "|---:|---:|---:|---:|---:|---:|---:|"]
for tau, q in summary["quality_targets"].items():
    if not q["valid_round2_comparisons"]:
        continue
    lines.append(f"| {tau} | {q['all_nodes_resident_round1']} | {q['identical_textured_models']} | "
                 f"{q['identical_shaded_models']} | {q['round1_vs_control_gpu_ratio'].get('median', 0):.3f} | "
                 f"{q['round1_minus_control_source_psnr_db'].get('median', 0):.3f} dB | "
                 f"{q['round2_minus_round1_source_psnr_db'].get('median', 0):.3f} dB |")
lines += ["", f"Model status counts: `{json.dumps(counts, sort_keys=True)}`.", "",
          f"Control/round 1 geometry mismatches: {len(summary['control_geometry_mismatch_models'])}. "
          f"Round 1/round 2 geometry mismatches: {len(summary['round2_geometry_mismatch_models'])}.", "",
          "## Cases to inspect", "",
          "| Model | Target | Cache saving | Textured PSNR between rounds | Pixels differing >8/255 | Captures |",
          "|---|---:|---:|---:|---:|---|"]
for row in rows:
    changed = row["round2_vs_round1_textured_changed_pixels_over_8_fraction"]
    if changed and float(changed) > 0.01:
        path = row["screenshot_directory"]
        captures = f"[PNGs]({path}/)" if path else "Not retained"
        lines.append(f"| {row['model_id']} | {row['quality_target_pixels']} | "
                     f"{float(row['round2_vs_round1_gpu_saving_pct']):.2f}% | "
                     f"{float(row['round2_vs_round1_textured_psnr_db']):.2f} dB | "
                     f"{100 * float(changed):.2f}% | {captures} |")
(out / "aggregate.md").write_text("\n".join(lines) + "\n")
print(json.dumps(summary, indent=2))
