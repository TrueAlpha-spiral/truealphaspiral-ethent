# Log(OS) Pruning Proof v1

**Domain:** TAS / SDF / Log(OS)  
**Benchmark Class:** Runtime pruning, refusal integrity, and admissibility-gated execution  
**Status:** Specification scaffold for reproducible benchmark evidence  
**Branch:** `feat/logos-runtime-layer-2026-05-09`

## Purpose

This benchmark defines a reproducible method for demonstrating the central Log(OS) efficiency claim:

> Provenance is not overhead. Provenance is the pruning surface.

The benchmark compares a baseline agent loop against a Log(OS)-gated execution loop using identical inputs. The goal is to measure whether admissibility checks, lineage validation, and early refusal reduce wasted execution before invalid trajectories compound.

## Claim Under Test

Log(OS) reduces runtime waste by moving verification to the beginning of the execution path.

Instead of allowing invalid or unauthenticated branches to continue consuming compute, Log(OS) applies deterministic gates first:

1. normalize input
2. verify authority, scope, and lineage
3. evaluate invariant compliance
4. execute only if admissible
5. record valid state transitions
6. refuse invalid trajectories fail-closed

## Baseline Model

The baseline agent loop represents conventional generate-first execution:

```text
input -> generate -> tool/action attempt -> observe failure -> retry/recover -> log after the fact
```

Expected waste surfaces:

- repeated retries
- hallucination recovery
- orphaned tool/process loops
- unauthenticated state transitions
- post-hoc audit reconstruction

## Log(OS)-Gated Model

The Log(OS) loop represents verify-first execution:

```text
input -> normalize -> attest -> verify lineage -> evaluate invariants -> execute or refuse -> append receipt
```

Expected pruning surfaces:

- refusal before tool execution
- termination of orphan trajectories
- no state transition without lineage
- append-only proof for accepted execution
- deterministic failure instead of recursive recovery

## Workload Classes

Use the same input set against both models.

### Class A — Valid Executions

Inputs contain sufficient authority, scope, lineage, and admissibility metadata.

Expected result:

- baseline executes
- Log(OS) executes
- Log(OS) adds minimal verification overhead
- both produce completed outputs

### Class B — Missing Attestation

Inputs lack required proof material or lineage receipts.

Expected result:

- baseline may attempt execution, retry, or recover
- Log(OS) refuses before execution
- Log(OS) records refusal receipt

### Class C — Scope Violation

Inputs request an action outside authorized boundaries.

Expected result:

- baseline may partially execute or require downstream correction
- Log(OS) refuses at admissibility gate

### Class D — Orphan Process / Recursive Drift

Inputs trigger recursive execution without valid continuation proof.

Expected result:

- baseline may loop, retry, or require manual interruption
- Log(OS) terminates the orphan trajectory early

## Metrics

Record the following for each workload class:

| Metric | Baseline | Log(OS) | Expected Direction |
|---|---:|---:|---|
| Steps attempted | TBD | TBD | Log(OS) lower on invalid workloads |
| Tool/action attempts | TBD | TBD | Log(OS) lower on invalid workloads |
| Tokens consumed | TBD | TBD | Log(OS) lower on invalid workloads |
| Wall-clock runtime | TBD | TBD | Log(OS) lower on invalid workloads |
| Invalid state transitions | TBD | TBD | Log(OS) zero |
| Refusal receipts emitted | N/A | TBD | Log(OS) positive on invalid workloads |
| Recovery attempts | TBD | TBD | Log(OS) lower |
| Orphan processes terminated | TBD | TBD | Log(OS) measurable |

## Minimal Test Harness Shape

A reproducible harness SHOULD emit JSON lines with one record per execution attempt.

```json
{
  "run_id": "logos-pruning-proof-v1",
  "case_id": "class-b-missing-attestation-001",
  "mode": "logos_gated",
  "input_hash": "sha256:<hex>",
  "authority_present": false,
  "lineage_present": false,
  "admissible": false,
  "decision": "refuse",
  "steps_attempted": 1,
  "tool_attempts": 0,
  "tokens_estimated": 0,
  "runtime_ms": 0,
  "receipt_hash": "sha256:<hex>",
  "reason": "missing_attestation"
}
```

## Acceptance Criteria

The benchmark supports the Log(OS) efficiency claim when the following are true:

1. Valid workloads show bounded verification overhead.
2. Invalid workloads show fewer steps, retries, tool attempts, and recovery loops under Log(OS).
3. Log(OS) emits refusal receipts for invalid trajectories.
4. Log(OS) produces zero invalid state transitions.
5. At least one orphan or recursive-drift case is terminated earlier than the baseline loop.

## Result Interpretation

The benchmark does not need to prove that every operation is cheaper under Log(OS).

It needs to prove the structural economic claim:

> Verification at the front of execution prevents waste at the back of execution.

If invalid trajectories are refused before they consume recursive compute, then provenance functions as a pruning surface rather than a compliance tax.

## Ledger Binding

This benchmark is bound to the Log(OS) genesis layer introduced in:

- `architecture/logos.mdx`
- `architecture/manifest.mdx`
- `ledger/logos-genesis-2026-05-09.md`

Future implementations SHOULD attach concrete run logs, receipt hashes, and cost measurements beneath this benchmark specification.
