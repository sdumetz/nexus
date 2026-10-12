"""Run round 1/2 analytical and binary-export checks using a Unix Makefiles build.

Usage: python3 tests/run_round1.py /path/to/nxsbuild-build-directory
Reuses builder objects so tests exercise the actual exporter without rebuilding
the full toolchain or changing the production executable.
"""
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile

build = Path(sys.argv[1]).resolve()
target = build / "CMakeFiles/nxsbuild.dir"
flags = {}
for line in (target / "flags.make").read_text().splitlines():
    if " = " in line:
        key, value = line.split(" = ", 1)
        flags[key] = shlex.split(value)
link = shlex.split((target / "link.txt").read_text())
with tempfile.TemporaryDirectory(prefix="nexus-round1-tests-") as directory:
    temp = Path(directory)
    obj = temp / "round1.o"
    executable = temp / "round1"
    subprocess.run([
        link[0], *flags["CXX_DEFINES"], *flags["CXX_INCLUDES"], *flags["CXX_FLAGS"],
        "-c", str(Path(__file__).with_name("round1.cpp").resolve()), "-o", str(obj),
    ], check=True)
    link = [str(obj) if arg.endswith("/main.cpp.o") else arg for arg in link]
    output = link.index("-o") + 1
    link[output] = str(executable)
    subprocess.run(link, cwd=build, check=True)
    subprocess.run([str(executable)], cwd=temp, check=True)
