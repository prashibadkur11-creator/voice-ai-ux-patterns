# Voice AI UX Pattern Library
![License: MIT](https://img.shields.io/github/license/prashibadkur11-creator/voice-ai-ux-patterns) ![CI](https://img.shields.io/github/actions/workflow/status/prashibadkur11-creator/voice-ai-ux-patterns/pattern-ci.yml?branch=main&label=CI)

A catalog of UX patterns for voice AI products. Each pattern covers a design problem
that only shows up when the interface is spoken: turn-taking, latency masking,
barge-in, error recovery, persona consistency, and conversational memory.

Patterns are YAML files with a fixed set of fields, so they can be compared, diffed,
and validated in CI rather than read as prose. There is very little public structured
writing on voice AI UX, which is the gap this fills.

[TODO: what I was designing when I started collecting these, and which one I got wrong first]

## What's here

Each pattern is a YAML file in `patterns/` conforming to [`schema.yaml`](schema.yaml):

| Field | What it captures |
|---|---|
| `problem` | The UX problem, from the user's side |
| `approach` | The recommended solution, concretely |
| `anti_pattern` | The seductive wrong approach, and why it fails |
| `example` | A concrete instance of the pattern |
| `applies_when` | When the pattern is relevant (vs. not) |
| `related_failure_modes` | Links to the AI Failure Mode Taxonomy |
| `related` | Patterns that pair with or trade off against this one |

Every entry names an `anti_pattern`. The tempting wrong approach is usually more
obvious than the right one, so it is worth writing down.

Browse [`CATALOG.md`](CATALOG.md) for the readable, generated view.

## The 8 patterns

- **Graceful Pause Detection**. Knowing when a user is finished vs. just pausing
- **Latency Masking**. Acknowledging instantly so delay doesn't read as failure
- **Barge-In Handling**. Letting users interrupt the assistant mid-response
- **Error Recovery Without Blame**. Recovering from misrecognition without faulting the user
- **Confirmation for Irreversible Actions**. Scaling confirmation to stakes and confidence
- **Re-Prompting Without Frustration**. Asking again progressively, not as a stuck record
- **Persona Consistency Under Ambiguity**. Staying in character under pressure
- **Context Carryover**. Resolving "the cheaper one" / "same as last time" across turns

## How it connects

Each pattern links by `related_failure_modes` to the
[AI Failure Mode Taxonomy](https://github.com/prashibadkur11-creator/ai-failure-mode-taxonomy).
*Latency Masking* prevents `latency-variability`. *Persona Consistency* prevents
`persona-drift`. The taxonomy says how voice AI breaks. This library says how to
design around it.

## Using it

```bash
pip install -r requirements.txt

# Validate all patterns against the schema (what CI runs)
python scripts/validate_patterns.py

# Regenerate the readable catalog from the YAML
python scripts/generate_catalog.py
```

To add a pattern: create `patterns/<id>.yaml` following the schema (the `id` must
match the filename), then regenerate the catalog. Open a PR. Pattern CI validates
every pattern and blocks anything malformed or incomplete.

## Repo layout

```
.
├── schema.yaml                       # pattern field definitions
├── patterns/                         # one YAML per pattern (source of truth)
├── CATALOG.md                        # generated readable catalog
├── scripts/
│   ├── generate_catalog.py           # YAML -> CATALOG.md
│   └── validate_patterns.py          # schema validator (the PR gate)
└── .github/workflows/pattern-ci.yml
```

## Limitations

[TODO: 8 patterns is a starting set, not coverage. What is missing]

[TODO: which of these I have actually shipped vs. read about]

[TODO: the schema validates structure, not whether the advice is right]

[TODO: nothing here covers non-English or noisy-environment voice UX]

## License

MIT.
