"""Reproduce and retain captures for >1% changed-pixel cases after a batch.

Uses the original records for the CSV; asserts repeated payload hashes,
allocations and image metrics match before retaining the additional captures.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import shutil

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("batch", HERE / "isti-batch.py")
batch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(batch)
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--out", type=Path, required=True)
parser.add_argument("--control", type=Path, required=True)
parser.add_argument("--pair", type=Path, required=True)
parser.add_argument("--node", required=True)
parser.add_argument("--scratch", type=Path, required=True)
args = parser.parse_args()
args.out, args.scratch = args.out.resolve(), args.scratch.resolve()
manifest = json.loads((args.out / "selection.json").read_text())
assert batch.sha(args.control) == manifest["control_binary_sha256"]
assert batch.sha(args.pair) == manifest["pair_binary_sha256"]
checks = []
for model in manifest["models"]:
    mid = model["model_id"]
    record = args.out / "models" / (mid + ".json")
    original = json.loads(record.read_text())
    if original.get("screenshot_directory") or not any(
        c["label"] == "round2" and c["reference"] == "round1" and c["mode"] == "textured"
        and c["changedPixelsOver8Fraction"] > 0.01 for c in original.get("measurement", {}).get("comparisons", [])):
        continue
    scratch = args.scratch / mid
    scratch.mkdir(parents=True, exist_ok=True)
    logs = args.out / "logs" / mid / "image-recheck"
    obj = scratch / "source" / "model.obj"
    commands = [("conversion", [args.node, str(HERE / "gltf-to-obj.mjs"), model["source"], str(obj)], scratch)]
    for label, binary in (("control", args.control), ("pair", args.pair)):
        directory = scratch / label
        directory.mkdir(exist_ok=True)
        command = [str(binary), str(obj)]
        if label == "pair":
            command += ["-o", str(directory / "model.nxs")]
        commands.append((label, command, directory))
    files = {"control": scratch / "control" / "test.nxs", "round1": scratch / "pair" / "model.round1.nxs",
             "round2": scratch / "pair" / "model.round2.nxs"}
    if not all(filename.exists() for filename in files.values()):
        for label, command, directory in commands:
            assert batch.execute(command, directory, logs / (label + ".log"), 600)["status"] == "ok", mid
    full_hashes_equal = True
    for label, filename in files.items():
        repeated_artifact = batch.artifact(filename)
        previous_artifact = original["artifacts"][label]
        full_hashes_equal &= repeated_artifact["sha256"] == previous_artifact["sha256"]
        for key in ("geometry_sha256", "texture_sha256", "file_bytes", "texture_sizes"):
            assert repeated_artifact[key] == previous_artifact[key], (mid, label, key, "payload differs")
    output = scratch / "browser"
    command = [args.node, str(HERE / "run.mjs")]
    for label, filename in files.items():
        command += ["--model", label + "=" + str(filename)]
    command += ["--source", model["source"], "--out", str(output), "--views", "2.5", "--taus", "2,0.1"]
    assert batch.execute(command, HERE.parent.parent, logs / "browser.log", 900)["status"] == "ok", mid
    repeated = json.loads((output / "results.json").read_text())
    for run in repeated["runs"]:
        if run.get("source"):
            continue
        previous = next(r for r in original["measurement"]["runs"] if r["label"] == run["label"] and r["tau"] == run["tau"])
        assert all(run[key] == previous[key] for key in batch.RUN_FIELDS), (mid, run["label"], "allocation differs")
    assert repeated["comparisons"] == original["measurement"]["comparisons"], (mid, "image metrics differ")
    destination = args.out / "screenshots" / mid
    destination.mkdir(parents=True, exist_ok=True)
    for image in output.glob("*.png"):
        shutil.copy2(image, destination / image.name)
    original["screenshot_directory"] = "screenshots/" + mid
    original["image_recheck_matches_original"] = True
    batch.atomic_json(record, original)
    checks.append({"model_id": mid, "full_file_hashes_equal": full_hashes_equal, "geometry_and_texture_payload_hashes_equal": True,
                   "allocations_equal": True, "image_metrics_equal": True})
    shutil.rmtree(scratch)
    print(mid + ": captures retained; payload hashes, allocations and image metrics match", flush=True)
batch.atomic_json(args.out / "image-rechecks.json", checks)
