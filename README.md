# Voice AI UX Pattern Library

A structured, forkable catalog of UX patterns specific to **voice AI products** —
the design problems that only show up when the interface is spoken: turn-taking,
latency masking, barge-in, error recovery, persona consistency, and conversational
memory.

Voice AI is an underserved PM discipline — there is very little public, structured
writing on it. This library captures the patterns as reusable, comparable entries
rather than prose, so they can be applied, forked, and extended like the rest of an
AI product toolkit.

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

The `anti_pattern` field is the heart of each entry — naming the tempting wrong way
and why it fails is what separates lived experience from a glossary.

Browse [`CATALOG.md`](CATALOG.md) for the readable, generated view.

## The 8 patterns

- **Graceful Pause Detection** — knowing when a user is finished vs. just pausing
- **Latency Masking** — acknowledging instantly so delay doesn't read as failure
- **Barge-In Handling** — letting users interrupt the assistant mid-response
- **Error Recovery Without Blame** — recovering from misrecognition without faulting the user
- **Confirmation for Irreversible Actions** — scaling confirmation to stakes and confidence
- **Re-Prompting Without Frustration** — asking again progressively, not as a stuck record
- **Persona Consistency Under Ambiguity** — staying in character under pressure
- **Context Carryover** — resolving "the cheaper one" / "same as last time" across turns

## How it connects

Each pattern links by `related_failure_modes` to the
[AI Failure Mode Taxonomy](https://github.com/prashibadkur11-creator/ai-failure-mode-taxonomy)
— e.g. *Latency Masking* prevents `latency-variability`, *Persona Consistency* prevents
`persona-drift`. The taxonomy says how voice AI breaks; this library says how to design
around it.

## Using it

```bash
pip install -r requirements.txt

# Validate all patterns against the schema (what CI runs)
python scripts/validate_patterns.py

# Regenerate the readable catalog from the YAML
python scripts/generate_catalog.py
```

To add a pattern: create `patterns/<id>.yaml` following the schema (the `id` must
match the filename), then regenerate the catalog. Open a PR — **Pattern CI**
validates every pattern and blocks anything malformed or incomplete.

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

## License

MIT.
