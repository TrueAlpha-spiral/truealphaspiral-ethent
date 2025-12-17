"""Run the TAS self-test workflow via a Codex-generated bash script."""
# © 2025 Russell Nordland | TrueAlphaSpiral (TAS) | Apache-2.0

"""
Set ``OPENAI_API_KEY`` in your environment and execute with ``python
codex_tas_runner.py``. The script requests a minimal bash recipe from
GPT-4o-code, runs it, and prints a JSON summary.
"""
import importlib
import importlib.util
import os
import subprocess
import json
import hashlib
import time
from artifact_guard import run_step

def _require_api_key() -> str:
    """Return the OpenAI API key or raise an informative error."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "OPENAI_API_KEY is required to run the self-test"
        )
    return api_key

SYSTEM = """You are a reliable DevOps assistant.
Produce a POSIX-compliant bash script that:
1. Clones https://github.com/truealphaspiral/tas_gpt.git if not present.
2. Creates a Python venv  (.venv)  and installs requirements.
3. Copies examples/config.safe_mode.yaml to config.yaml.
4. Creates ledger/  directory if missing.
5. Runs:  python tas_agent.py --task "self-test"
6. Captures the console output to audit.log.
7. Computes SHA-256 of audit.log and writes it to ledger/self_test.hash
"""


def _load_openai():
    """Return the ``openai`` module or raise an informative error."""
    if importlib.util.find_spec("openai") is None:
        raise ModuleNotFoundError(
            "The 'openai' package is required. Install it with "
            "`pip install openai` before running codex_tas_runner.py."
        )
    return importlib.import_module("openai")

def get_codex_script(openai_client):
    resp = openai_client.ChatCompletion.create(
        model="gpt-4o-code",  # or "gpt-4o"
        messages=[{"role":"system","content":SYSTEM}]
    )
    return resp.choices[0].message.content

def run_bash(script: str) -> subprocess.CompletedProcess:
    """Write the script to a file, run it via ``run_step`` and return the result."""
    with open("run.sh", "w", encoding="utf-8") as f:
        f.write(script)
    os.chmod("run.sh", 0o755)
    meta = run_step("codex_script", f"bash run.sh")
    proc = subprocess.CompletedProcess(
        args=["bash", "run.sh"],
        returncode=meta.get("returncode", 1),
        stdout=meta.get("stdout", ""),
        stderr=meta.get("stderr", ""),
    )
    return proc


def main() -> None:
    openai_client = _load_openai()
    openai_client.api_key = _require_api_key()

    bash_script = get_codex_script(openai_client)
    result = run_bash(bash_script)

    # compute SHA-256 of audit.log after execution
    audit_log = "audit.log"
    ledger = os.path.join("ledger", "self_test.hash")
    hash_val = ""
    if os.path.exists(audit_log):
        with open(audit_log, "rb") as f:
            digest = hashlib.sha256(f.read()).hexdigest()
        os.makedirs("ledger", exist_ok=True)
        with open(ledger, "w") as f:
            f.write(digest)
        hash_val = digest
    elif os.path.exists(ledger):
        with open(ledger, "r") as f:
            hash_val = f.read().strip()

    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "returncode": result.returncode,
        # include the last 10 lines of stdout/stderr for quick diagnostics
        "stdout_tail": result.stdout.splitlines()[-10:],
        "stderr_tail": result.stderr.splitlines()[-10:],
        "audit_hash": hash_val,
    }

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
