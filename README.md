# Larkspur disruption agent: the pod repo

A disruption-care agent for Larkspur Airlines, built on nine tools that already
work (`support/tools.py`, running against a frozen copy of real airline data in
`data/americas/`). You build `agent.py`, which holds what Claude is told about
each tool and the loop that drives them.

**Open `guide/index.html` for the steps.** It starts on **Welcome to your
build**, which is the case study, then the three questions your pod answers out
loud, then **Get set up**. After that it is the build page by page. What you are
building, what to do, what it looks like when it worked, and where to look when
it did not. `guide/Participant-Guide.pdf` is the same thing on paper.

**The same steps run on the build site** at
<https://anthropicpartnerbasecamp.bts.com/>, which your pod opens together in
the room. It opens on the welcome too, and the three Start pages sit under the
first tab. The site adds the build clock at the top of the page and the box
where you paste the evidence code a gate prints. Nothing uploads either way.
Pick your surface once on Get set up and it stays picked.

**Nobody in the pod has an assigned job.** You decide in the moment who does
what. One rule stands. One person pushes the canon at the end of the build and
everyone else takes it. Agree who before the clock runs out.

## The five commands

These five run the whole build.

```bash
git clone <your pod repo URL>      # once
python3 setup.py                   # until it says READY
python3 run.py K7PQ2M --trace      # every build
python3 verify.py 1.2              # every gate
python3 pod_sync.py --take-canon   # at the end of a build
```

`setup.py` checks python, the SDK, git, a real reach to the pod repo, and one
live call to Claude. Every failure it prints names the fix. Run it at your own
desk. There is no offline path in this pack, so a credential that does not work
stops the build.

`run.py` shows the wire, every request and every reply exactly as it went.
`verify.py` checks behavior on the wire and prints your evidence code. `claude`
in this folder gives you `/setup`, `/build`, `/check` and `/readout`. Start
there if you would rather not lead with a terminal.

## One repo, several people

One person in the pod makes this repo from the template the room lead posts in
chat. **Use this template**, then **Create a new repository**, owner their own
account, Private. Then **Settings**, **Collaborators**, **Add people** for every
podmate by GitHub username, plus the room lead's handle, which is in the chat.
The overnight review needs that handle to reach your repo, and a repo nobody
shared gets no file back. Then they post the repo URL in the pod thread, and
nobody else does anything until it is there.

Everyone else has an invitation email waiting. Accept it before you try to
clone, because a private repo refuses you until you do. Clone it rather than
downloading a zip. The checks read git history.

**Nobody commits `agent.py` mid-build. One person pushes the canon at the end
of the build with `python3 pod_sync.py --push-canon`, and everyone else takes
it with `python3 pod_sync.py --take-canon`. Agree who before the clock runs
out.**

Everyone builds their own `agent.py` on their own laptop. Two people editing
one file in one repo gives you a merge conflict inside a loop you are all still
learning to read.

`--take-canon` saves your version to `.workshop/mine/` first and prints the
path. Nothing you wrote is lost, so `diff` it against the canon. If you are
behind or something broke, the pod repo is your checkpoint:

```bash
python3 pod_sync.py --take-canon --force
```

It restores what the pod pushed. Anything gitignored stays gone. Your `.env`
(re-create it from `.env.example`), `.venv/` (rebuild with
`python3 setup.py --fix`), and `.workshop/`, which holds your banked codes and
your bench numbers. Copy `.workshop/` out before you re-clone into a fresh
folder, and copy it back in after. If it is already gone, say so rather than
re-running `bench.py --label before` against the current agent.

## The scripts

| Script | What it does |
|---|---|
| `setup.py` | Checks this machine. `--fix` builds the venv and installs. Run it until READY. |
| `run.py <PNR> --trace` | Runs the agent on one ticket and shows every turn on the wire. `--all` runs the five shapes and writes the totals. |
| `verify.py <step>` | A gate: `1.2`, `1.3`, `1.4`, `2.1`, `2.2`, `3.1`, `4.1`. Run it with no step and it prints the status board. |
| `pod_sync.py` | The pod's canon: `--push-canon`, `--take-canon`, `--status`. |
| `eval_harness.py` | Runs `evals/cases.json`, your pod's own cases, against your agent. |
| `bench.py --label <name>` | Measures a run: latency, tokens, cache, cost per contact. The before/after pair around your lever. |
| `readout.py` | Writes the one page that says what your agent is and what it just did. The canon push publishes it. |

`TEAM.md` is the pod's name and a typed roster, written once by whoever created
the repo. The review reads the names off it. `PITCH.md` and `evals/cases.json`
are the pod's shared record, and they are normal commits. The bench pair never
leaves your laptop.

## Ground rule

If you cannot explain a turn on your own trace (`python3 run.py <PNR>
--trace`), you have not finished the step, whatever the gate says.

## Build 1 evidence

[PITCH.md](PITCH.md#build-1-verification-record---2026-09-16) records the original
five-shape baseline, the retrospective four-fault review, and the distinction
between saved gate codes, local checks, and fresh live verification.
That earlier audit was blocked by unavailable API authentication. Authentication
was subsequently configured and Build 2 gates passed; see the newer live evidence
in [PITCH.md](PITCH.md). The configured model is not proof of code authorship.

On Windows, use UTF-8 for the gate's check marks and generated readout:

```powershell
$env:PYTHONIOENCODING = "utf-8"
.\.venv\Scripts\python.exe -X utf8 verify.py 1.2
```

Run from the repository folder after configuring authentication locally using
the setup instructions. Do not paste credentials into chat or commit them.

## Build 2: availability tool over MCP

Step 2.1's local implementation is preserved in commit `3466528`. After
authentication was configured, that exact agent passed gate 2.1 (`88C-AFB`).
Step 2.2 now discovers `next_available_day` and `fare_rules` through
`mcp_client.tools()`. There is no duplicate local schema or registration:
the server owns both names, and the original nine tools are unchanged.
The shared customer question is in [build2_probe.txt](build2_probe.txt).
The tool checks one passenger's earliest available date, not whole-party
capacity, and makes no hold or booking.

Put your personal key in the ignored `.env` file at the repository root:

```dotenv
ANTHROPIC_API_KEY=your-personal-key
```

The application loads this into its process environment automatically; no
machine-wide environment change is needed. Save as UTF-8 without a BOM.
An existing environment variable takes precedence over this file.

```powershell
.\.venv\Scripts\python.exe -X utf8 -m unittest test_agent -v
.\.venv\Scripts\python.exe -X utf8 run.py --show-tools
.\.venv\Scripts\python.exe -X utf8 run.py K7PQ2M --trace --message "When is the first day I can actually fly?"
.\.venv\Scripts\python.exe -X utf8 run.py --tool-tax
.\.venv\Scripts\python.exe -X utf8 run.py --all --trace
.\.venv\Scripts\python.exe -X utf8 support\mcp_selftest.py
.\.venv\Scripts\python.exe -X utf8 verify.py 2.2
```

Preserve the Build 1 baseline in [PITCH.md](PITCH.md) when recording Build 2
measurements. Unit tests do not prove that Claude chose the tool; only the
live probe and gate establish that.

Gate 2.1 checks a local registration, so it must be run on the local
checkpoint, not on the migrated MCP version. Do not reinstate a local copy
alongside MCP merely to make both gates pass on the same file.

Verified live codes: 2.1 `88C-AFB`, 2.2 `6B2-926`. The final five-shape
MCP sweep returned text for 5/5, with 19 turns and 76,340 input tokens.
The demo API also answered the shared question using `next_available_day`.
