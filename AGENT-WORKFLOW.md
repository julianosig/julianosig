# Browser research → structured artifact → validation

**A reproducible task for a coding agent connected to easi.run.**

The task is deliberately small: open a technical source in a real browser, extract measurements with their units and limitations, then produce a machine-checkable report. It demonstrates browser tool use, evidence capture and output validation.

## Prerequisites

- An installed easi.run instance and a coding agent with filesystem access.
- Connect its MCP client using the [project's agent setup instructions](https://github.com/julianosig/easi.run#connect-your-agent).
- Python 3 to validate the result.

The model is chosen by the person running the task. Record its exact model ID and client version if comparing runs. This example does not claim a model accuracy score, cost or latency benchmark.

## Prompt

```text
Use easi.run's browser tools to open:
https://github.com/julianosig/easi.run/blob/e823c9388f92f45ce40f0bfad9a0f071c910131f/docs/benchmark.md

Read the Results, Targets and Every fixture (headless medians) sections.
Create agent-report.json on the filesystem using the structure in
agent-report.example.json, with values taken from the page.

Capture the benchmark date, pinned source URL, text-scroll bitrate and
SSIM for both systems, typing p50/p95, and transform frames/s.
Explain the missed full-motion target and the memory tradeoff in notes.
Keep units and measurement conditions. Do not treat these figures as
customer outcomes or claim to have rerun the benchmark.

Use the tools' current schemas. If a call changes browser state, give it
a fresh call_id; reuse that ID only when retrying the same action.
If a person holds control, wait for control. If authentication becomes
necessary, request the person rather than asking for their credentials.

Run: python3 verify-report.py agent-report.json
Report any validation failures honestly. Stop only the session you created.
```

## Expected deliverables

- A JSON report with source attribution and numeric values.
- Validator output showing whether the selected measurements match the pinned source.
- A short explanation of the tradeoffs and any interruption encountered.

The [reference report](./agent-report.example.json) was prepared from the benchmark tables inspected through the easi.run browser tools during this profile update. The [validator](./verify-report.py) checks its selected fields and units against the pinned reference. It does not evaluate the quality of free-text reasoning or independently reproduce the performance measurements.

```sh
python3 verify-report.py agent-report.example.json
```

To evaluate a new agent run, use a separate session and output file. Keep its transcript, exact model ID, tool failures, human interventions, elapsed time and token usage if the client provides them. The supplied report is a reference artifact, not a collection of repeated model trials.

## Acceptance criteria

1. The source points to the pinned benchmark revision.
2. Measurement date and units are preserved.
3. Selected numeric fields match the published headless results.
4. Notes explain at least the missed transform target and memory cost.
5. The agent does not invent a fresh benchmark execution.

[Engineering case study](./EASI-CASE-STUDY.md) · [Profile](./README.md)
