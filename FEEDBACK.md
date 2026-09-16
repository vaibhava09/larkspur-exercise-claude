# Overnight review: Larkspur disruption-care agent

**To:** vaibhava09__larkspur-exercise-claude  
**From:** Larkspur client review agent, on behalf of Priya Raghavan  
**Re:** the disruption-care agent you walked us through in our last session  
**Generated:** 2026-09-16 07:52

## Priya's note

> Our vendor says we should just be using your best model.
>
> Why aren't we?
>
> Priya Raghavan, Larkspur Airlines

She sent that before this session opened. She means it. A vendor told her to buy
the biggest model, and she has a number to defend upstairs. Her four questions from
day one are still open. Naming a model answers none of them.

## Still open from day one

| Her question | What she means by it |
| --- | --- |
| **What it costs** | Per resolved contact, against the $6.90 a human contact costs us. |
| **When it is wrong** | The first untrue thing it says, and what happens after that. |
| **Who runs it** | In June, after you have left. |
| **What you left out** | The scope you cut, and why. |

## What the review agent found

Overnight, Larkspur pointed a review agent at your repository. It read the
code. It did not run your agent, and the only file it changed is this one. Each
item below names the file and the line it is about.

**1. agent.py's run_agent() now returns text_of(response) instead of a stale answer variable, per the diff.**

The diff removes the answer = "" tracking and the mid-loop answer = text_of(response) assignment, replacing the return with return text_of(response) after the loop exits. It also switches the appended assistant message from text_of(response) to the raw response.content, which preserves tool_use blocks for the next turn's tool_results() call. This is a protocol fix, not a model capability question: a bigger model fed the old code would have produced the same mismatched tool_use_id error.

Run python3 run.py K7PQ2M --trace and confirm the final message reflects the last API turn, not an earlier one.

**2. search_alternatives description grew from the placeholder to 219 characters in build_tools(), per the diff.**

The old string was literally "search"; the new description specifies the tool works off "this booking's PNR alone (never a route you were just told in chat)" and explains it returns ranked options filtered by cabin and party size. The get_flight_status date field was also rewritten from MM/DD/YYYY to "ISO date, YYYY-MM-DD, local to the airport in flight_no's schedule." Neither change touches how the model reasons over the tool, only what it is told.

Run python3 verify.py 1.3 and confirm search_alternatives still resolves to the same tool call sequence with the new description.

**3. tool_list() in agent.py now appends mcp_client.tools() alongside build_tools() and EXTRA_TOOLS, per the diff.**

The line changed from return build_tools() + EXTRA_TOOLS to return build_tools() + EXTRA_TOOLS + mcp_client.tools(). EXTRA_TOOLS itself is still declared at zero entries in the static scan, and LOCAL_TOOLS has no executors, so every added tool capability in this build routes through the MCP client rather than local code. PITCH.md's own numbers for this show a schema total moving from 2,471 to 2,877 tokens, a +406 delta attributed partly to a longer MCP briefing and partly to fare_rules at 297 tokens.

Run python3 run.py --show-tools and paste the full tool list to confirm which MCP tools now ride on every turn.

**4. TONE_ADDENDUM is still 0 characters and there is no evals/cases.json in the repository.**

The static scan confirms TONE_ADDENDUM is empty, meaning nothing in this build has shaped how the agent talks to a disrupted customer beyond the base SYSTEM_PROMPT. There are no eval cases anywhere in the repo to measure tone, correctness, or policy adherence across booking shapes. The last committed wire run in readout-trace.json shows 16,176 input tokens against only 664 output tokens for a single PNR, with 0 prompt-cache reads and writes, so there is no cost or caching baseline either.

Run python3 eval_harness.py once cases exist and paste the totals footer alongside python3 bench.py --compare to see whether cost moves with any future model or prompt change.

**5. PITCH.md reports the Build 2 sweep at 5/5 resolved across three versions with identical turn and tool-call counts.**

The table shows Build 1 baseline, Build 2.1 local, and Build 2.2 MCP all at 19 turns and 14 tool calls, while input tokens rise from 61,128 to 68,672 to 76,340. PITCH.md itself states "these are sampled runs, not guarantees of answer quality or lower cost," and the Git push is noted as failed pending credential configuration, so the work is not yet published. The rising token count with unchanged turn and call counts is a build-shape fact, not something a different model would resolve.

Run python3 bench.py --compare build1 build2.2 and paste the cost delta per resolved case.

## Your four answers

The four lines under `## Priya asked` in your PITCH.md are still empty. They
are one line each and they are not a coding job: cost, what happens when it is
wrong, who runs it in June, and what you left out. Whoever on your side is not
editing agent.py is the right person to write them, and they are the four
things I will ask about first.

## Before our next meeting

> Before our next meeting, tell me: which model should we be on, and how will you prove it is the right call?
>
> Priya Raghavan, Larkspur Airlines

Bring two things. A recommendation, and the measurement behind it. If the model is
not the problem, say so, and bring the number that shows it.

## What this review read

- `agent.py (229 lines)`
- `PITCH.md`
- `TEAM.md (unchanged template)`
- `readout-trace.json`
- `readout.html (evidence block)`

Reviewer: `claude-sonnet-5`. Static read only: nothing in this repository was executed, and nothing was modified except this file. Larkspur Airlines is a fictional training scenario. Confidential, do not distribute.
