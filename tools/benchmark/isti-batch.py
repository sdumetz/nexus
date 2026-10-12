"""Deterministic, resumable ISTI sampling, builds, browser measurements and CSV.

python3 tools/benchmark/isti-batch.py --dataset /path/ISTI_dataset \
  --control /path/v4-fixes/nxsbuild --pair /path/build-pair \
  --node /path/node --out doc/measurements/isti-100 --scratch /tmp/isti-100

Requires Pillow for reading image headers. Browser use needs localhost access.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import random
import shutil
import signal
import struct
import subprocess
import threading
import time
import tempfile
import urllib.parse
import warnings
from PIL import Image

HERE = Path(__file__).resolve().parent
LABELS = ("control", "round1", "round2")
TAUS = (2, 0.1)
RUN_FIELDS = ("gpuBytes", "geometryBytes", "textureBytes", "legacyEstimatedCacheBytes",
              "residentNodes", "totalNodes", "liveTextures", "baseTexels", "mipTexels",
              "drawnTriangles", "allocationAuditPassed")
RUN_NAMES = ("gpu_bytes", "geometry_bytes", "texture_bytes", "legacy_estimate_bytes",
             "resident_nodes", "total_nodes", "resident_textures", "base_texels", "mip_texels",
             "drawn_triangles", "allocation_audit_passed")
METRICS = ("identical", "psnrDb", "meanAbsoluteChannelDifference", "changedPixelsOver8Fraction",
           "silhouetteIoU", "modelPixels")
METRIC_NAMES = ("identical", "psnr_db", "mean_abs_channel_difference", "changed_pixels_over_8_fraction",
                "foreground_iou", "foreground_pixels")
PAIRS = (("round1", "control"), ("round2", "control"), ("round2", "round1"),
         ("control", "source"), ("round1", "source"), ("round2", "source"))


def atomic_json(filename, data):
    filename.parent.mkdir(parents=True, exist_ok=True)
    temp = filename.with_suffix(filename.suffix + ".tmp")
    temp.write_text(json.dumps(data, indent=2, allow_nan=False) + "\n")
    temp.replace(filename)


def sha(filename):
    with open(filename, "rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def select_models(dataset, count, seed):
    eligible, excluded = [], []
    for directory in sorted(dataset.glob("RWT*"), key=lambda p: int(p.name[3:])):
        files = sorted(directory.glob("*.gltf"))
        if len(files) != 1:
            excluded.append({"id": directory.name, "reason": "not exactly one glTF"})
            continue
        try:
            g = json.loads(files[0].read_text())
            primitives = []
            def visit(index):
                node = g["nodes"][index]
                if "mesh" in node:
                    primitives.extend(g["meshes"][node["mesh"]]["primitives"])
                for child in node.get("children", []):
                    visit(child)
            for index in g["scenes"][g.get("scene", 0)]["nodes"]:
                visit(index)
            triangles = sum((g["accessors"][p["indices"]]["count"] if "indices" in p else
                             g["accessors"][p["attributes"]["POSITION"]]["count"]) // 3
                            for p in primitives if p.get("mode", 4) == 4)
            if len(g.get("images", [])) != 1 or not all("TEXCOORD_0" in p["attributes"] for p in primitives):
                raise ValueError("requires one source atlas and UVs on all primitives")
            image_file = directory / urllib.parse.unquote(g["images"][0]["uri"])
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", Image.DecompressionBombWarning)
                with Image.open(image_file) as image:
                    width, height = image.size
            if not (10000 <= triangles <= 150000 and max(width, height) <= 4096):
                raise ValueError("outside 10k–150k triangles / maximum 4K atlas")
            metadata = json.loads((directory / "metadata.json").read_text())
            eligible.append({"model_id": directory.name, "name": metadata.get("name", ""),
                             "category": metadata.get("category", ""), "author": metadata.get("author", ""),
                             "license": metadata.get("license", ""), "source_url": metadata.get("uri", ""),
                             "input_triangles": triangles, "input_texture_width": width,
                             "input_texture_height": height, "input_texels": width * height,
                             "source": str(files[0].resolve()), "source_sha256": sha(files[0]),
                             "texture_sha256": sha(image_file),
                             "buffer_sha256": {b["uri"]: sha(directory / urllib.parse.unquote(b["uri"])) for b in g["buffers"]}})
        except Exception as error:
            excluded.append({"id": directory.name, "reason": str(error)})
    if len(eligible) < count:
        raise ValueError(f"Only {len(eligible)} eligible models, requested {count}")
    selected = sorted(random.Random(seed).sample(eligible, count), key=lambda m: int(m["model_id"][3:]))
    return selected, eligible, excluded


def execute(command, cwd, logfile, timeout):
    logfile.parent.mkdir(parents=True, exist_ok=True)
    with logfile.open("w") as stream:
        process = subprocess.Popen(command, cwd=cwd, stdout=stream, stderr=subprocess.STDOUT,
                                   start_new_session=True)
        try:
            code = process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                pass
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            return {"status": "timeout", "timeout_seconds": timeout}
    return {"status": "ok" if code == 0 else "failed", "exit_code": code}


def artifact(filename):
    """Static export diagnostics; residency still comes from the browser audit."""
    data = filename.read_bytes()
    nodes, patches, textures = struct.unpack_from("<III", data, 60)
    geometry = hashlib.sha256()
    for i in range(nodes - 1):
        offset, vertices, faces = struct.unpack_from("<IHH", data, 88 + 44 * i)
        geometry.update(data[offset * 256:offset * 256 + vertices * 26 + faces * 6])
    start = 88 + nodes * 44 + patches * 12
    offsets = [struct.unpack_from("<I", data, start + 68 * i)[0] * 256 for i in range(textures)]
    sizes, base, mips = [], 0, 0
    for begin, end in zip(offsets, offsets[1:]):
        with Image.open(io.BytesIO(data[begin:end])) as image:
            w, h = image.size
        sizes.append([w, h])
        base += w * h
        while True:
            mips += w * h
            if w == h == 1:
                break
            w, h = max(1, w // 2), max(1, h // 2)
    return {"file_bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
            "geometry_sha256": geometry.hexdigest(), "texture_sha256": hashlib.sha256(data[offsets[0]:offsets[-1]]).hexdigest(),
            "export_nodes": nodes - 1, "export_textures": len(sizes),
            "export_base_texels": base, "export_mip_texels": mips, "texture_sizes": sizes}


def rows_for(model, state):
    report = state.get("measurement", {})
    artifacts = state.get("artifacts", {})
    for tau in TAUS:
        row = {key: model[key] for key in ("model_id", "name", "category", "input_triangles",
                                         "input_texture_width", "input_texture_height", "input_texels")}
        row.update(status=state.get("status", "pending"), quality_target_pixels=tau,
                   camera_distance_radii=2.5, viewport_width=1280, viewport_height=800,
                   texture_error_ratio=1, control_status=state.get("control", {}).get("status", "pending"),
                   pair_status=state.get("pair", {}).get("status", "pending"),
                   render_status=state.get("render", {}).get("status", "pending"),
                   diagnostic=state.get("error", ""), screenshot_directory=state.get("screenshot_directory", ""))
        for label in LABELS:
            static = artifacts.get(label, {})
            for key in ("file_bytes", "export_nodes", "export_textures", "export_base_texels", "export_mip_texels"):
                row[label + "_" + key] = static.get(key, "")
            run = next((r for r in report.get("runs", []) if r["label"] == label and r["tau"] == tau), {})
            for key, name in zip(RUN_FIELDS, RUN_NAMES):
                row[label + "_" + name] = run.get(key, "")
        for a, b in PAIRS:
            for mode in ("textured", "shaded"):
                c = next((c for c in report.get("comparisons", []) if c["label"] == a and c["reference"] == b
                          and c["tau"] == tau and c["mode"] == mode), {})
                for key, name in zip(METRICS, METRIC_NAMES):
                    value = c.get(key, "")
                    # Infinite PSNR is represented by a blank plus identical=True.
                    row[f"{a}_vs_{b}_{mode}_{name}"] = "" if value is None else value
        for a, b in (("round1", "control"), ("round2", "control"), ("round2", "round1")):
            av, bv = row[a + "_gpu_bytes"], row[b + "_gpu_bytes"]
            row[f"{a}_vs_{b}_gpu_ratio"] = av / bv if av != "" and bv else ""
            row[f"{a}_vs_{b}_gpu_saving_pct"] = 100 * (1 - av / bv) if av != "" and bv else ""
        for key in ("file_bytes", "export_base_texels"):
            av, bv = row["round2_" + key], row["round1_" + key]
            row["round2_vs_round1_" + key + "_saving_pct"] = 100 * (1 - av / bv) if av != "" and bv else ""
        a, b = artifacts.get("round1"), artifacts.get("round2")
        control = artifacts.get("control")
        row["round2_geometry_matches_round1"] = a["geometry_sha256"] == b["geometry_sha256"] if a and b else ""
        row["control_geometry_matches_round1"] = control["geometry_sha256"] == a["geometry_sha256"] if control and a else ""
        row["control_texture_payload_matches_round1"] = control["texture_sha256"] == a["texture_sha256"] if control and a else ""
        row["round2_resized_textures"] = sum(x != y for x, y in zip(a["texture_sizes"], b["texture_sizes"])) if a and b else ""
        row["row_measurement_complete"] = all(row[label + "_allocation_audit_passed"] is True for label in LABELS)
        row["round2_comparison_has_foreground"] = bool(row.get("round2_vs_round1_textured_foreground_pixels"))
        yield row


def write_csv(out, models, states):
    rows = [row for model in models for row in rows_for(model, states.get(model["model_id"], {}))]
    with tempfile.NamedTemporaryFile(mode="w", newline="", dir=out, prefix="results-", suffix=".tmp", delete=False) as stream:
        temp = Path(stream.name)
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    temp.replace(out / "results.csv")
    graph = []
    for row in rows:
        g = {key: row[key] for key in ("model_id", "name", "category", "input_triangles", "input_texels",
                                      "quality_target_pixels", "status", "row_measurement_complete",
                                      "round2_comparison_has_foreground", "round2_resized_textures")}
        for label in LABELS:
            for key in ("gpu_bytes", "geometry_bytes", "texture_bytes", "file_bytes"):
                v = row[label + "_" + key]
                g[label + "_" + key.removesuffix("_bytes") + "_mib"] = v / 1048576 if v != "" else ""
        for key in ("round1_vs_control_gpu_saving_pct", "round2_vs_control_gpu_saving_pct",
                    "round2_vs_round1_gpu_saving_pct", "round2_vs_round1_file_bytes_saving_pct",
                    "round2_vs_round1_export_base_texels_saving_pct"):
            g[key] = row[key]
        for a, b in PAIRS:
            if b == "control" and a == "round2":
                continue
            for key in ("identical", "psnr_db", "changed_pixels_over_8_fraction"):
                name = f"{a}_vs_{b}_textured_{key}"
                value = row[name]
                if key.endswith("_fraction"):
                    name = name.removesuffix("_fraction") + "_pct"
                    value = value * 100 if value != "" else ""
                g[name] = value
        g["round2_vs_round1_shaded_identical"] = row["round2_vs_round1_shaded_identical"]
        graph.append(g)
    with tempfile.NamedTemporaryFile(mode="w", newline="", dir=out, prefix="graph-", suffix=".tmp", delete=False) as stream:
        temp = Path(stream.name)
        writer = csv.DictWriter(stream, fieldnames=list(graph[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(graph)
    temp.replace(out / "graph.csv")


def compact_report(report):
    for run in report.get("runs", []):
        for key in ("textures", "residentNodeIds"):
            run.pop(key, None)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--control", type=Path, required=True)
    parser.add_argument("--pair", type=Path, required=True)
    parser.add_argument("--node", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--scratch", type=Path, required=True)
    parser.add_argument("--count", type=int, default=100)
    parser.add_argument("--seed", type=int, default=20261012)
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--build-timeout", type=int, default=600)
    args = parser.parse_args()
    for key in ("dataset", "control", "pair", "out", "scratch"):
        setattr(args, key, getattr(args, key).resolve())
    args.out.mkdir(parents=True, exist_ok=True)
    args.scratch.mkdir(parents=True, exist_ok=True)
    manifest_file = args.out / "selection.json"
    if manifest_file.exists():
        manifest = json.loads(manifest_file.read_text())
        if manifest["count"] != args.count or manifest["seed"] != args.seed or manifest["dataset"] != str(args.dataset):
            raise ValueError("Existing selection does not match arguments; use a new output directory")
        if manifest["control_binary_sha256"] != sha(args.control) or manifest["pair_binary_sha256"] != sha(args.pair):
            raise ValueError("Builder binaries differ from the frozen experiment; use a new output directory")
        models = manifest["models"]
    else:
        models, eligible, excluded = select_models(args.dataset, args.count, args.seed)
        manifest = {"dataset": str(args.dataset), "count": args.count, "seed": args.seed,
                    "eligible_count": len(eligible), "eligibility": "10k–150k triangles, one atlas <=4096 on each side, UVs",
                    "control_commit": "1fe489d", "experiment_commit": "f763879", "builder_defaults": True,
                    "control_binary_sha256": sha(args.control), "pair_binary_sha256": sha(args.pair),
                    "quality_targets": TAUS, "camera_distance_radii": 2.5, "viewport": [1280, 800],
                    "models": models, "eligible_model_ids": [m["model_id"] for m in eligible], "excluded": excluded}
        atomic_json(manifest_file, manifest)
    states = {}
    for model in models:
        filename = args.out / "models" / (model["model_id"] + ".json")
        if filename.exists():
            states[model["model_id"]] = json.loads(filename.read_text())
    write_csv(args.out, models, states)
    browser_lock = threading.Lock()
    keep_images = {m["model_id"] for m in models[:8]}

    def work(model):
        mid = model["model_id"]
        if states.get(mid, {}).get("finished"):
            return mid, states[mid], True
        state = {"status": "running", "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
        scratch = args.scratch / mid
        # These are runner-owned temporary intermediates, recreated on resume.
        if scratch.exists():
            shutil.rmtree(scratch)
        scratch.mkdir()
        logdir = args.out / "logs" / mid
        try:
            obj = scratch / "source" / "model.obj"
            conversion = execute([args.node, str(HERE / "gltf-to-obj.mjs"), model["source"], str(obj)],
                                 scratch, logdir / "conversion.log", 120)
            state["conversion"] = conversion
            if conversion["status"] != "ok":
                raise RuntimeError("Source conversion failed; see conversion.log")
            for label in ("control", "pair"):
                directory = scratch / label
                directory.mkdir()
                command = [str(args.control), str(obj)] if label == "control" else [str(args.pair), str(obj), "-o", str(directory / "model.nxs")]
                state[label] = execute(command, directory, logdir / (label + ".log"), args.build_timeout)
            filenames = {"control": scratch / "control" / "test.nxs",
                         "round1": scratch / "pair" / "model.round1.nxs",
                         "round2": scratch / "pair" / "model.round2.nxs"}
            state["artifacts"] = {}
            for label, filename in filenames.items():
                stage = "control" if label == "control" else "pair"
                if state[stage]["status"] == "ok" and filename.exists():
                    state["artifacts"][label] = artifact(filename)
            if not {"round1", "round2"}.issubset(state["artifacts"]):
                raise RuntimeError("Paired build failed; see pair.log")
            output = scratch / "browser"
            command = [args.node, str(HERE / "run.mjs")]
            for label in LABELS:
                if label in state["artifacts"]:
                    command += ["--model", label + "=" + str(filenames[label])]
            command += ["--source", model["source"], "--out", str(output), "--views", "2.5", "--taus", "2,0.1"]
            # Build in parallel, but run one software-GL browser at a time.
            with browser_lock:
                state["render"] = execute(command, HERE.parent.parent, logdir / "browser.log", 900)
            if (output / "results.json").exists():
                state["measurement"] = compact_report(json.loads((output / "results.json").read_text()))
            comparisons = state.get("measurement", {}).get("comparisons", [])
            significant = any(c["label"] == "round2" and c["reference"] == "round1" and
                              c["changedPixelsOver8Fraction"] > 0.05 for c in comparisons)
            if mid in keep_images or significant:
                destination = args.out / "screenshots" / mid
                destination.mkdir(parents=True, exist_ok=True)
                for image in output.glob("*.png"):
                    shutil.copy2(image, destination / image.name)
                state["screenshot_directory"] = "screenshots/" + mid
            if state["render"]["status"] != "ok":
                raise RuntimeError("Browser measurement incomplete; see browser.log")
            state["status"] = "ok" if "control" in state["artifacts"] else "partial_control_failed"
            if "control" not in state["artifacts"]:
                state["error"] = "Control build failed; round1/round2 measurements available"
        except Exception as error:
            state["status"] = "failed"
            state["error"] = str(error)
        finally:
            state["finished"] = True
            state["ended"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            atomic_json(args.out / "models" / (mid + ".json"), state)
            shutil.rmtree(scratch, ignore_errors=True)
        return mid, state, False

    print(f"Selected {len(models)} / {manifest['eligible_count']} eligible models; CSV: {args.out / 'results.csv'}", flush=True)
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = [executor.submit(work, model) for model in models]
        for index, future in enumerate(as_completed(futures), 1):
            mid, state, resumed = future.result()
            states[mid] = state
            write_csv(args.out, models, states)
            print(f"{index}/{len(models)} {mid}: {state['status']}{' (resumed)' if resumed else ''} {state.get('error', '')}", flush=True)
    atomic_json(args.out / "completion.json", {"models": len(models), "status_counts": {
        status: sum(state["status"] == status for state in states.values())
        for status in sorted({s["status"] for s in states.values()})}})


if __name__ == "__main__":
    main()
