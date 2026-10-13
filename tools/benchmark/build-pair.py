"""Link the shared-hierarchy experiment driver against a completed Makefiles builder.

python3 tools/benchmark/build-pair.py BUILD_DIR model.gltf -o /path/to/prefix.nxs
Builder options after BUILD_DIR are forwarded unchanged. Run in a scratch
directory because the builder writes intermediate hierarchy files there.
"""
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
import shutil

build = Path(sys.argv[1]).resolve()
target = build / "CMakeFiles/nxsbuild.dir"
flags = {}
for line in (target / "flags.make").read_text().splitlines():
    if " = " in line:
        key, value = line.split(" = ", 1)
        flags[key] = shlex.split(value)
link = shlex.split((target / "link.txt").read_text())
with tempfile.TemporaryDirectory(prefix="nexus-build-pair-") as directory:
    temp = Path(directory)
    obj, executable = temp / "pair.o", temp / "pair"
    subprocess.run([
        link[0], *flags["CXX_DEFINES"], *flags["CXX_INCLUDES"], *flags["CXX_FLAGS"],
        "-c", str(Path(__file__).with_name("build-pair.cpp").resolve()), "-o", str(obj),
    ], check=True)
    link = [str(obj) if arg.endswith("/main.cpp.o") else arg for arg in link]
    link[link.index("-o") + 1] = str(executable)
    subprocess.run(link, cwd=build, check=True)
    if len(sys.argv) == 4 and sys.argv[2] == "--compile-only":
        shutil.copy2(executable, sys.argv[3])
    else:
        subprocess.run([str(executable), *sys.argv[2:]], check=True)
