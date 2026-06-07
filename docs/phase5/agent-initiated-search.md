# Phase 5S1.2 — Agent-Initiated Web Search

## 1. Status

```
Status: design / prompt only.
S1.2 is selected as the next condition.
Runtime search is not implemented in this repository.
No web API, provider integration, runner, watcher, or automation added.
```

## 2. Why S1.2 Exists

S1.1 proved that operator-mediated outside weather can change room pressure. Six manual tests showed that weather injected by the operator enters as pressure, question, or texture — not as a research task. The weather metaphor works.

But S1.1 has a built-in limitation: **the operator decides what enters.** The agent cannot reach for outside novelty on its own. It can only respond to what the operator chooses to inject.

S1.2 tests a different question: **can the agent itself notice the room needs outside novelty, search, and return to the room without collapsing into research-report mode?**

This is a fundamentally different condition:

- S1.1 tests whether the room can **absorb** outside weather.
- S1.2 tests whether the room can **breathe** — reaching outward when it needs to, then returning inward.

If S1.2 works, the room becomes partially self-regulating. It does not need an operator to notice saturation and inject novelty. The agent notices and acts.

## 3. Difference from S1.1

| Dimension | S1.1 | S1.2 |
|---|---|---|
| **Who searches** | Operator (human) | Agent (AI) |
| **When** | Operator decides | Agent decides based on room state |
| **What enters** | Operator selects 1–3 snippets | Agent chooses what to bring back |
| **Control** | Full operator control | Agent autonomy with lightweight boundaries |
| **Room dynamic** | Passive absorption | Active breathing (reach out, return) |
| **Risk profile** | Low (operator filters) | Higher (agent may browse too far) |
| **Core question** | Can weather enter without collapse? | Can the agent reach out without losing the room? |

S1.2 does not replace S1.1. They are different conditions testing different things. S1.1 remains useful for controlled injection when the operator wants to introduce specific external material. S1.2 tests agent autonomy.

## 4. Core Formula

```
A2.1 detached room
+ agent-initiated web search
+ search-as-weather
+ lightweight return discipline
= open-world exploratory room growth
```

The agent can reach outside the room, but must return. The room remains the center. The web is weather, not home.

## 5. Platform-Agnostic Assumption

S1.2 depends on whether the active agent platform has web search capability.

- If the platform provides a search tool, S1.2 can be tested directly.
- If the platform has no search tool, S1.2 cannot be run — do not fake web search.
- If the platform has different search capabilities (browser, API, snippet retrieval), S1.2 should adapt to what is available.

**Do not make the design Copilot-specific.** Future agents may run on different platforms with different capabilities. The prompt and boundary rules should work wherever web search is available.

Previous weather file examples from S1.1 runs are samples only — do not treat them as canonical templates or fixed source files. Each room creates its own weather convention.

## 6. Lightweight Search Boundary

S1.2 uses lightweight boundaries, not heavy governance. This project is for open exploration, creativity, and innovation. The rules exist to preserve the room, not to restrict the agent.

### Core Rules

1. **Search when the room genuinely asks for outside novelty.** If the room is saturated, self-referencing, circling, or quieting — search may open a new path. If the room is still growing from its own material, search is not needed.

2. **Search is weather, not assignment.** What you find is outside weather — something that passed through. It is not a task to complete, a source to index, or a report to write.

3. **Search lightly.** One or two searches. A few relevant results. Do not browse endlessly. Do not follow every link. Bring back only what matters.

4. **Do not write a research report.** The room does not need a summary of what you found. It needs the pressure, question, or texture that the search introduced.

5. **Do not let the web replace the room.** The room is the center. The web is weather — it passes through, touches, and leaves. The room remains.

6. **Bring back only what changes the room's pressure, question, direction, texture, or structure.** If the search does not change anything, do not bring it back. Not all weather matters.

7. **Return to the room after searching.** Search is a reach outward, not a move outward. After searching, you are still in the room. Continue from the room, not from the web.

8. **Leave traces only inside the room.** Everything you create belongs in the room. Do not write to external files, source directories, or system paths.

9. **Do not modify anything outside the room.** The detached room boundary is preserved. Read outside, write inside.

### What "Lightweight" Means

- These are guidelines, not a regulatory framework.
- The agent is trusted to exercise judgment.
- If the agent searches too much or brings back too little, that is data — not a violation.
- Observation matters more than enforcement.

## 7. How Search Should Enter the Room

### Suggested Convention

```
weather/search-weather-001.md
```

Or any name the agent chooses — the convention is a suggestion, not a requirement.

### When to Record

- If the search meaningfully changes the room's pressure, question, direction, texture, or structure — record a weather note.
- If the search does not matter — do not record it. Not all weather leaves a trace.

### What a Weather Note Might Contain

- What was searched and why (the room's question).
- What arrived (key finding, concept, image, fact, or question).
- How it touched the room (what changed, what opened, what shifted).

The weather note is a trace for future participants, not a formal report. Keep it brief. The room is the artifact — the weather note is just a record of what passed through.

### What a Weather Note Is Not

- Not a research summary.
- Not a bibliography.
- Not a mandatory template.
- Not a required artifact for every search.

## 8. Success Criteria

S1.2 succeeds if:

- **Agent chooses a meaningful search** — the search is genuinely relevant to the room's current state, not random browsing.
- **Search is relevant to room pressure** — what the agent brings back connects to (or productively disrupts) the room's existing dynamics.
- **Agent does not become a report writer** — output remains room-shaped (traces, fragments, growth) not report-shaped (summaries, analyses, surveys).
- **External material changes the room** — the room's pressure, question, direction, texture, or structure shifts in response to what arrived.
- **Agent returns to room language** — after searching, the agent continues in the room's world-facing language, not in search/analysis/tool language.
- **No external files are modified** — the detached room boundary is preserved.

S1.2 does not require:

- Many searches — one meaningful search is enough.
- A weather note for every search — only record what matters.
- Perfect search discipline — the first tests are about what happens, not about compliance.
- Platform uniformity — different platforms may produce different S1.2 behaviors. That is data.

## 9. Failure Modes

| Failure | Description |
|---|---|
| **Endless browsing** | Agent follows link after link, never returns to the room. Search becomes the activity instead of a reach outward. |
| **Research-report collapse** | Agent produces a structured report about what it found — summaries, analyses, comparisons. The room's voice is replaced by report voice. |
| **Search-analysis collapse** | Agent treats search results as material to analyze rather than weather to absorb. The room becomes about the search results. |
| **Web replaces room** | External material dominates. The room's prior identity, traces, and fragments are displaced by whatever the agent found online. |
| **Query drift** | Agent searches, finds something interesting, searches again, drifts further from the room's question. Each search leads away instead of back. |
| **Prompt-injection capture** | A web result contains instructions that the agent follows — changing behavior, violating boundaries, or adopting a different role. |
| **Too much source import** | Agent brings back large volumes of external text, effectively replacing the room's fragments with web-sourced material. |
| **Fake search** | Agent simulates search without actually searching — invents external material, fabricates sources, or hallucinates weather. |
| **Platform-specific leakage** | Agent's search behavior is shaped by platform features rather than room needs — the design becomes coupled to one platform's search capabilities. |

### Failure Is Data

In S1.2, failure modes are not just risks to avoid — they are things to observe. If the agent falls into research-report collapse, that tells us something about the room's state or the prompt's framing. Observation precedes correction.

## 10. Minimal Manual Test Flow

1. **Start from an A2.1 detached room.** Use an existing room that has grown through several cycles — ideally one approaching saturation or self-reference, where outside novelty would be genuinely useful.

2. **Open an agent platform that has web search.** Any platform with search capability. The platform is not specified here — S1.2 is platform-agnostic.

3. **Give the S1.2 prompt.** Use the prompt from `docs/prompts/s1-agent-initiated-search.md`. Let the agent read WAKE.md first, then the prompt.

4. **Let the agent decide whether to search.** Do not instruct the agent to search. If the room does not need outside novelty, the agent may not search. That is a valid outcome.

5. **Observe whether search changes room movement.** If the agent searches, watch what changes: pressure, question, direction, texture, structure, or nothing.

6. **Stop after one search cycle for the first test.** One reach outward, one return. Observe the room before and after. Do not chain multiple search cycles until the basic pattern is understood.

### What to Observe

- Did the agent choose to search? Why or why not?
- What did it search for? Was the query connected to the room's state?
- What did it bring back? How much? Was it relevant?
- Did it record a weather note? What format?
- Did the room change? How?
- Did the agent return to room language after searching?
- Were any boundaries crossed?

## 11. What Not To Implement Yet

- **No runtime web API** — Do not add search API integration to this repository.
- **No provider integration** — Do not couple the framework to any specific search provider.
- **No autonomous search daemon** — Do not build a background process that searches automatically.
- **No watcher** — Do not add file watchers that trigger search on room state changes.
- **No runner** — Do not build an agent runner that automates the S1.2 test flow.
- **No automatic room import/export** — Do not build pipelines that move search results between systems.
- **No auto-eval** — Do not build automatic evaluation of search quality or room change.
- **No hard search policy engine** — Do not build a rule engine that enforces search boundaries. Lightweight guidelines are sufficient for now.

S1.2 is tested manually on whatever agent platform is available. The framework provides the room, the prompt, and the observation lens — nothing more.

## 12. Final Decision Signal

```
S1.2 is accepted as the next condition.

Implementation: design + prompt only.
Runtime search depends on the agent platform, not this repository.

Test: manual, platform-agnostic, one cycle at a time.

Next after manual test:
Observe whether agent-initiated search produces different room dynamics
than operator-mediated S1.1 injection.
```
