<!--
──────────────────────────────────────────────────────────────────────────────
TAS_ASE_DNA  •  Triadic-Braid Pull-Request Template  (Staple-π Edition)
Save as .github/pull_request_template.md
──────────────────────────────────────────────────────────────────────────────
-->

# 🚀  PR Title  
<!-- Use imperative mood: “Add artifact-per-input guard” -->

---

## 📋  Summary
_A concise 2–3 sentence overview of what this PR does and why._

---

## 🧭  Motivation & Context (“Why”)  
* Which bug / feature / RFC does this address?  
* Link to relevant issues, discussions, or external specs (e.g. TAS ledger entry).  

---

## 🛠️  What Changed (“What”)  
| Type | Included |
|------|----------|
| ✅ Feature | <!-- yes / no --> |
| 🐞 Fix | <!-- yes / no --> |
| 📝 Docs | <!-- yes / no --> |
| 🧪 Tests | <!-- yes / no --> |
| ♻️ Refactor | <!-- yes / no --> |

**High-level list:**  
- bullet 1  
- bullet 2  

---

## 🔬  How to Test (“How”)  
```bash
# 1. Prep
export OPENAI_API_KEY=•••
git clone https://github.com/openai/PROJECT.git
git checkout <this-branch>

# 2. Run the suite
bash tas_gpt_setup.sh             # or make test
python codex_tas_runner.py
```

Expected result: all checks **PASS**, ITL child hash appended.

---

## 📝  Documentation Updates  
*Docs PR / section link, or “n/a”.*

---

## ✅  Checklist  

- [ ] **CLA signed** (if required by repo).  
- [ ] Unit / integration **tests added** or updated.  
- [ ] **Docs** reflect new behaviour / API.  
- [ ] **π-staple perspective check** passed (`run_step` produces artifact JSON).  
- [ ] **Artifact guard hashes** committed (`artifacts/artifact-*.json`).  
- [ ] **ITL lineage**:  
  - Parent hash: `c3513adde82a…5df55e80`  
  - Child hash (this PR): `<!-- paste after CI -->`  
- [ ] Code follows **house style** (American spelling: artifact, center, color).  
- [ ] No breaking changes without migration guide.  
- [ ] Security / privacy implications reviewed.

---

## 🔗  Reviewer Guide  

| Focus area | Reviewer |
|------------|----------|
| Code logic | @maintainer-name |
| π-Staple / ITL hash | @tas-guardian |
| Docs clarity | @tech-writer |
| Security | @sec-team |

\n<!-- End of triadic-braid PR template -->
