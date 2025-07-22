"""Artifact guard for capturing per-step execution metadata."""
# © 2025 Russell Nordland | TrueAlphaSpiral (TAS) | Apache-2.0

import json
import hashlib
import time
import subprocess
import pathlib

ART_DIR = pathlib.Path("artifacts")
ART_DIR.mkdir(exist_ok=True)
LEDGER_FILE = pathlib.Path("ledger/artifacts.hash")
LEDGER_FILE.parent.mkdir(exist_ok=True)

def run_step(name: str, code: str):
    """Execute code in bash and record an artifact with metadata."""
    uid = f"{int(time.time()*1000)}-{hashlib.sha256(code.encode()).hexdigest()[:8]}"
    meta = {
        "uid": uid,
        "step": name,
        "code": code,
        "t_start": time.time(),
    }
    try:
        result = subprocess.run([
            "bash",
            "-c",
            code,
        ], capture_output=True, text=True)
        meta.update(
            {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            }
        )
    finally:
        meta["t_end"] = time.time()
        art_path = ART_DIR / f"artifact-{uid}.json"
        art_path.write_text(json.dumps(meta, indent=2))
        digest = hashlib.sha256(art_path.read_bytes()).hexdigest()
        with LEDGER_FILE.open("a") as lf:
            lf.write(f"{digest}  {art_path.name}\n")
    return meta
