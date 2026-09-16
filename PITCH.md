# PITCH.md

Six lines and a lever. Your words. The last two are scored.

## Current participant and evidence

Participant: **Vaibhav Agarwal**. All five gates were rerun successfully
under this corrected name on 2026-09-16; use these codes instead of the
earlier Room 14 codes in the historical records below.

| Gate | Evidence code | Live result |
| --- | --- | --- |
| 1.2 | 5AD-037 | 4 API turns, 3 tool calls, final end_turn and non-empty text |
| 1.3 | 746-C60 | Nine original tools present; flight status returned data |
| 1.4 | 848-424 | All five shapes resolved with at least one tool call |
| 2.1 | ADD-651 | Local next_available_day chosen on attempt 1; non-empty text |
| 2.2 | 339-EB9 | MCP next_available_day chosen on attempt 1; no duplicate ownership |

Gate 2.1 was rerun on the exact local agent from `3466528`, then the final
MCP agent was restored and the other four gates were rerun on it. The
corrected-name local probe consumed 9,980 input tokens across 2 tool calls;
the MCP probe consumed 11,267 across 2. Schema counts remain 2,471 and 2,877.
Historical baseline and sweep measurements below have not been relabelled
as new runs. The Git push failed because GitHub authentication could not
prompt; publication remains pending until Git credentials are configured.

## Build 2 live evidence - 2026-09-16

Authentication is now configured in the ignored local `.env`; it loaded
successfully for live API calls. The earlier authentication failures below
are historical, not the current status. No key is included in this record.

- Step 2.1: `88C-AFB`, banked for `Room 14 - Vaibhav Agarwal`.
  The exact local agent from commit `3466528` passed on attempt 1:
  `next_available_day` was registered locally, chosen without its name in
  the customer message, and returned a non-empty response.
  Probe: 10,480 input tokens, 3 tool calls; schema total: 2,471 tokens.
- Step 2.2: `6B2-926`, same participant. Both MCP tools were discovered;
  all 11 offered names were unique, with no duplicate local registration.
  `next_available_day` fired on attempt 1 and the response was non-empty.
  Final gate probe: 11,267 input tokens, 2 tool calls; schema total: 2,877.
- Schema delta: +406 tokens. The per-tool removal counts changed from 386
  for the local availability schema to 495 for its longer MCP briefing,
  while `fare_rules` contributes 297. Do not attribute the entire increase
  to transport or to `fare_rules` alone; the availability briefing changed
  too. The supplied gate's summary names only the added tool.
- Explicit MCP trace: K7PQ2M, "When is the first day I can actually fly?"
  selected `lookup_booking`, `get_flight_status`, and
  `next_available_day [mcp]`; ended on `end_turn` after 3 API turns.
  Response reported earliest availability on 2025-05-08.
- Demo HTTP check at localhost:4390 returned a non-empty answer for the same
  customer question and included `next_available_day` in `tool_names`.
  This verifies the demo API, not a manual browser interaction.
- Supplied MCP self-test: 31/31 PASS. Local-tool tests passed before
  migration; both final mocked MCP ownership/dispatch tests pass.

| Version | Sweep time | Resolved | Turns | Tool calls | Input tokens | Output tokens |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| Build 1 baseline | 14:54:55 | 5/5 | 19 | 14 | 61,128 | 3,043 |
| Build 2.1 local | 16:18:52 | 5/5 | 19 | 14 | 68,672 | 3,338 |
| Build 2.2 MCP | 16:21:52 | 5/5 | 19 | 14 | 76,340 | 3,251 |

All five rows in each new sweep ended on `end_turn` without errors.
These are sampled runs, not guarantees of answer quality or lower cost.
The original baseline remains recorded below even though the latest-run
files now contain Build 2 evidence.

The application calls the configured `claude-sonnet-5` model. This is
runtime configuration and successful API execution, not proof that Sonnet
authored the code. Implementation assistance was Copilot SDK in VS Code;
no subagents were called. Website banking and podmates taking the canon
must still be done by the participants. Builds 3 and 4 are out of scope.

## Build 1 verification record - 2026-09-16

Historical audit before the Build 2 work above; its blocked and unpublished
statuses describe that earlier moment.

This is an audit record, not the participant's pitch or original step 1.1 notes.
The earlier claim that Build 1 was completely verified was too strong:
`verify.py` without a step displays saved codes; it does not rerun the gates.

### Original baseline (step 1.4)

Preserved from `.workshop/last_run.json`, generated `2026-09-16T14:54:55`.
These are historical measurements, not results of today's verification attempt.

| PNR | Turns | Tool calls | Input tokens | Output tokens | Stop reason |
| --- | ---: | ---: | ---: | ---: | --- |
| K7PQ2M | 4 | 3 | 13,033 | 611 | end_turn |
| M3XR8T | 4 | 3 | 12,963 | 597 | end_turn |
| T9WN4C | 4 | 3 | 12,920 | 598 | end_turn |
| G2HL9V | 3 | 2 | 9,224 | 577 | end_turn |
| R8KD3F | 4 | 3 | 12,988 | 660 | end_turn |
| Total | 19 | 14 | 61,128 | 3,043 | 5/5 returned text |

The two baseline numbers are **19 total turns** and **61,128 input tokens**.
This does not establish answer quality, tone safety, or future live passes.

### Four faults: retrospective evidence, not an original prediction

Comparison of initial commit `621e973` with `HEAD` shows:

- SEEN IN ORIGINAL CODE: `run_agent()` sent assistant text without the
  `tool_use` blocks whose IDs the next tool results referenced.
- SEEN IN ORIGINAL SCHEMA: `build_tools()` described `search_alternatives`
  only as "search".
- SEEN IN ORIGINAL SCHEMA: `build_tools()` described the flight-status date
  as `MM/DD/YYYY` instead of the ISO date now specified.
- RETROSPECTIVE PREDICTION: behind the protocol failure, `run_agent()` would
  return text from the previous tool-request turn, not the final response.

All four corrections already exist in `agent.py`; no agent code was changed
in this audit. The original failing trace and a prediction written before
the fixes are not established by these artifacts and cannot be recreated
as contemporaneous evidence.

### Verification and attribution

- Local checks passed: Python syntax; exactly nine original tool names;
  every tool description at least 40 characters; API-turn ceiling of eight;
  saved five-shape totals agree and every row ends on `end_turn`.
- Mock-only checks passed: full assistant content is replayed with tool
  results, the final response supplies the returned text, and repeated
  `tool_use` stops at eight API turns. These are not live gate passes.
- Regenerated `readout.html` and `readout-trace.json` from the current
  architecture and saved trace using `python -X utf8 readout.py`, not a new
  API conversation. The readout labels the single conversation separately
  from the historical five-shape sweep.
- Saved codes remain: 1.2 `CCB-839`, 1.3 `AA2-4BE`, 1.4 `F42-3B4`,
  under `Room 14 - Vaibhav Agarwal`. Website banking is not verified.
- Fresh `.\.venv\Scripts\python.exe verify.py 1.2` exited 1 before any
  successful API turn, with:

  ```text
  TypeError: "Could not resolve authentication method. Expected one of api_key, auth_token, or credentials to be set. Or for one of the `X-Api-Key` or `Authorization` headers to be explicitly omitted"
  ```

- Retried gate 1.2 after the user reported local authentication configured;
  it again exited 1 with the same error. A value-hidden diagnostic found no
  repository `.env`, no available API key, bearer token or Bedrock token,
  and no detected SDK OAuth profile in this process.
- Credential detection returned `unknown`. Gates 1.3 and 1.4, the live
  five-shape rerun, and demo conversations were not rerun because they
  require the same unavailable authentication. Status: BLOCKED, not passed.
- `support/data.py` configures the application model as `claude-sonnet-5`.
  The saved trace does not record model identity, and the fresh gate failed
  authentication. This supports configuration only, not a claim that Claude
  Sonnet 5 authored the fixes or performed this audit.
- Audit assistance: AI assistant using Copilot SDK in VS Code; no subagents.
- Canon publication and podmates taking the canon remain unverified. The
  initial check showed two commits ahead of cached `origin/main`; by the
  final check, `HEAD` and `origin/main` both pointed to `ef9ff7f`. This audit
  ran no fetch or push. The new audit documents and regenerated readout
  remain uncommitted; podmates taking the canon is still unverified.

After restoring authentication locally, rerun gates 1.2, 1.3 and 1.4 and
`run.py --all --trace`, keeping the original baseline above. Repeat the demo
checks for K7PQ2M, G2HL9V and R8KD3F; the agreed pod committer then publishes
the canon and everyone else takes it. The pod roster still needs the
participants' actual names, not inferred names.

## Where the context went

The saved single-ticket trace has its largest input on turn 4 (the final answer): 4,054 input tokens versus turn 3's 3,323, because every turn resends the conversation so far, including previous tool results; trimming or summarizing that history can reduce input size, while prompt caching can reduce the billed cost of eligible repeated content without shortening the context. This single-ticket trace is separate from the five-shape baseline above.

Built:
Does:
Number:
Guardrail:
Next:
Still broken:
Lever: <cost | speed | intelligence>

## Priya asked

Costs:
Wrong:
Runs it:
Left out:
