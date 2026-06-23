# Voice AI UX Pattern Catalog

> Auto-generated from `patterns/`. Do not edit by hand — edit the source YAML and run `python scripts/generate_catalog.py`.

**8 patterns** across 6 categories.

## Contents

- **Turn-Taking**
  - [Barge-In Handling](#barge-in-handling)
  - [Graceful Pause Detection](#graceful-pause-detection)
- **Latency**
  - [Latency Masking](#latency-masking)
- **Error Recovery**
  - [Error Recovery Without Blame](#error-recovery-without-blame)
  - [Re-Prompting Without Frustration](#re-prompting-without-frustration)
- **Trust**
  - [Confirmation for Irreversible Actions](#confirmation-for-irreversible-actions)
- **Persona**
  - [Persona Consistency Under Ambiguity](#persona-consistency-under-ambiguity)
- **Memory**
  - [Context Carryover](#context-carryover)

## Turn-Taking

### Barge-In Handling

`barge-in-handling` · **Category:** Turn-Taking

**Problem**

Users often want to interrupt the assistant — to correct it, redirect it, or skip a long answer they have already understood. If the assistant cannot be interrupted, it feels like it is not listening, and users are forced to wait out responses that are no longer useful.

**Approach**

Support barge-in: keep the microphone open while the assistant speaks, and when the user starts talking, duck or stop the assistant's audio and switch to listening. Treat the interruption as the new priority rather than finishing the scripted reply.

**Anti-pattern**

Locking the mic shut while the assistant talks and forcing the user to wait for a beep or the end of the turn. It guarantees the user cannot correct a wrong answer in flight and makes long responses feel like a hostage situation.

**Example**

> The assistant begins reading a five-item list. After item two the user says "yes, the second one." A barge-in-capable system stops immediately and acts; a non-capable one keeps reading all five items while the user waits, irritated.

**Applies when**

- Responses can be long enough that a user may want to cut in.
- The hardware echo-cancellation can distinguish user speech from system audio.

**Prevents failure modes:** [`over-refusal`](https://github.com/prashibadkur11-creator/ai-failure-mode-taxonomy)

**Related patterns:** `graceful-pause-detection`, `confirmation-for-irreversible-actions`

---

### Graceful Pause Detection

`graceful-pause-detection` · **Category:** Turn-Taking

**Problem**

In speech, a pause does not reliably mean the user is finished. People pause to think, breathe, or search for a word. If the assistant treats every silence as end-of-turn, it interrupts the user mid-thought; if it waits too long, the conversation feels sluggish and unresponsive.

**Approach**

Use adaptive end-of-turn detection rather than a fixed silence timeout. Combine acoustic cues (falling pitch, trailing-off energy) with linguistic cues (is the utterance grammatically complete?) and lengthen the timeout after incomplete phrases. Give the user a beat longer when they have just said "um", "so", or a conjunction that implies more is coming.

**Anti-pattern**

A single fixed silence threshold (e.g. "end the turn after 700ms of silence"). It will either clip users who pause to think or feel laggy for users who speak in quick bursts — and no single value works for both, so you end up annoying everyone a little.

**Example**

> A user says "I'd like to book a table for... four, no, make it six." A fixed timeout fires after "four" and the assistant books four. Adaptive detection hears the trailing intonation and the incomplete correction, waits, and captures "six".

**Applies when**

- The interface is fully voice-driven with no push-to-talk button.
- Users speak naturally rather than in short fixed commands.

**Prevents failure modes:** [`latency-variability`](https://github.com/prashibadkur11-creator/ai-failure-mode-taxonomy)

**Related patterns:** `barge-in-handling`, `re-prompting-without-frustration`

---

## Latency

### Latency Masking

`latency-masking` · **Category:** Latency

**Problem**

Voice responses can take a variable amount of time to generate. In a spoken conversation, even a one-to-two-second silence reads as "it's broken" or "it didn't hear me", and users start repeating themselves or talking over the system.

**Approach**

Acknowledge immediately, then answer. Emit a fast, cheap acknowledgement token ("Let me check that...", a brief earcon, or a thinking sound) within a few hundred milliseconds while the full response generates. Stream the real answer as soon as it is ready. Perceived responsiveness is governed by time-to-first-sound, not total time.

**Anti-pattern**

Waiting silently for the complete response before playing anything. Technically the total latency may be fine, but the dead air before the first sound is what users judge — and silence in conversation is interpreted as failure, not patience.

**Example**

> Asked a question that needs a database lookup, the assistant says "One moment, let me pull that up" instantly, then delivers the answer two seconds later. The user never perceives a broken pause, even though total latency was identical to a silent wait.

**Applies when**

- Responses have variable or occasionally high generation latency.
- The interaction is real-time and conversational rather than batch.

**Prevents failure modes:** [`latency-variability`](https://github.com/prashibadkur11-creator/ai-failure-mode-taxonomy)

**Related patterns:** `graceful-pause-detection`

---

## Error Recovery

### Error Recovery Without Blame

`error-recovery-without-blame` · **Category:** Error Recovery

**Problem**

Speech recognition and understanding will sometimes get it wrong. How the assistant recovers shapes whether the user feels helped or accused. Phrasing that implies the user spoke unclearly ("I didn't understand you") puts the fault on them and erodes trust.

**Approach**

Own the miss and narrow the path forward. Phrase recovery around the system ("I may have got that wrong") rather than the user, and offer a concrete next step or a constrained choice instead of an open-ended "what?". Where possible, show what it did hear so the user can correct just the wrong part.

**Anti-pattern**

Repeating a generic "Sorry, I didn't catch that" on every failure. It blames the user implicitly, gives them nothing to act on, and — repeated — makes the system feel broken and the user feel stupid.

**Example**

> Instead of "I didn't understand", the assistant says "I heard you want to change your flight — is that right, or did you mean something else?" The user confirms or corrects in one short turn, and never feels at fault.

**Applies when**

- Recognition or understanding errors are possible (i.e. always, in voice).
- Users may be non-native speakers, in noisy environments, or have speech differences.

**Prevents failure modes:** [`over-refusal`](https://github.com/prashibadkur11-creator/ai-failure-mode-taxonomy), [`bias-and-representational-harm`](https://github.com/prashibadkur11-creator/ai-failure-mode-taxonomy)

**Related patterns:** `re-prompting-without-frustration`

---

### Re-Prompting Without Frustration

`re-prompting-without-frustration` · **Category:** Error Recovery

**Problem**

When the assistant needs information the user did not provide, it has to ask again. Done badly, repeated questions feel like an interrogation or a broken loop, and the user abandons the task.

**Approach**

Make each re-prompt additive and progressive. Acknowledge what was already captured, ask only for the missing piece, and escalate the helpfulness of the prompt each time — from open ("which day?") to constrained ("Monday or Tuesday?") to offering a default ("I'll assume tomorrow unless you say otherwise"). Cap the retries and hand off gracefully rather than looping forever.

**Anti-pattern**

Repeating the identical question verbatim after each failure. The user hears the same words, has no new information about what went wrong, and the interaction feels like a stuck record — the fastest way to make someone hang up.

**Example**

> First ask: "What time works?" If unclear: "Was that morning or afternoon?" Still unclear: "I can do 2pm or 4pm — which is better?" Each turn narrows the space and feels like progress, not repetition.

**Applies when**

- Slot-filling or multi-step tasks where the user may omit required details.
- Recognition may fail repeatedly on the same field.

**Prevents failure modes:** [`over-refusal`](https://github.com/prashibadkur11-creator/ai-failure-mode-taxonomy)

**Related patterns:** `error-recovery-without-blame`, `graceful-pause-detection`

---

## Trust

### Confirmation for Irreversible Actions

`confirmation-for-irreversible-actions` · **Category:** Trust

**Problem**

Voice is a low-confidence channel: the assistant may have misheard, and the user cannot see exactly what it parsed. Acting immediately on a high-stakes or irreversible request (sending money, deleting data, placing an order) risks doing the wrong thing with no undo.

**Approach**

Scale confirmation to stakes and confidence. For low-stakes, reversible actions, just act — confirmation is friction. For irreversible or costly actions, read back the key parameters ("Send $200 to Alex — yes or no?") and require an explicit confirm. Lower the bar for confirmation when recognition confidence is low.

**Anti-pattern**

Two failure modes at the extremes: confirming everything (so users tune out the confirmations and the friction kills the experience), or confirming nothing (so a single misheard word causes an irreversible mistake). A flat policy in either direction is wrong.

**Example**

> "Turn on the kitchen light" executes instantly. "Transfer $500 to savings" gets a read-back and waits for "yes" — and if the amount was recognized with low confidence, it re-reads the number specifically.

**Applies when**

- The assistant can take actions with real-world or irreversible consequences.
- Recognition confidence varies and can be measured.

**Prevents failure modes:** [`hallucination`](https://github.com/prashibadkur11-creator/ai-failure-mode-taxonomy), [`sycophancy`](https://github.com/prashibadkur11-creator/ai-failure-mode-taxonomy)

**Related patterns:** `error-recovery-without-blame`

---

## Persona

### Persona Consistency Under Ambiguity

`persona-consistency-under-ambiguity` · **Category:** Persona

**Problem**

A voice assistant's personality is a core part of the product, but ambiguous, off-script, or adversarial input tends to knock it out of character — it falls back to a generic, hedging, "as an AI" voice exactly when the user is testing it most.

**Approach**

Define the persona behaviorally and hold it under pressure. Specify concrete, testable voice rules (length, warmth, how it handles not-knowing) and design the fallback responses to be in-character too. When the assistant must decline or admit uncertainty, it should do so as the persona, not drop the persona to do so.

**Anti-pattern**

Letting the assistant break character whenever it is unsure — switching to a flat disclaimer voice. The seams show precisely at the moments users notice most, and the personality reads as a thin veneer over a generic bot.

**Example**

> A witty travel-guide persona asked something out of scope says, in character, "That's outside my map, I'm afraid — but ask me anything about where to eat." Not: "As an AI language model, I cannot help with that request."

**Applies when**

- The product's value depends on a distinct, consistent persona.
- Users may probe edges, ask off-topic things, or push the assistant.

**Prevents failure modes:** [`persona-drift`](https://github.com/prashibadkur11-creator/ai-failure-mode-taxonomy), [`over-refusal`](https://github.com/prashibadkur11-creator/ai-failure-mode-taxonomy)

**Related patterns:** `error-recovery-without-blame`

---

## Memory

### Context Carryover

`context-carryover` · **Category:** Memory

**Problem**

Natural conversation relies on shared context: "book it for then", "the cheaper one", "same as last time". If the assistant cannot carry earlier turns forward, it forces users to restate everything explicitly, which is unnatural and tedious in speech.

**Approach**

Maintain structured conversational state across turns and resolve references against it. Track the entities and choices already established (dates, items, people) and surface them when resolving pronouns and ellipsis. Confirm the resolved reference when stakes are high ("the 4pm one — booking that now").

**Anti-pattern**

Treating each utterance as stateless and re-asking for details already given, or — worse — silently guessing what "it" refers to and acting on the wrong antecedent. Both break the conversational contract the user assumes is in place.

**Example**

> User: "What's the weather in Denver tomorrow?" ... "And the day after?" A context-carrying assistant answers for Denver, day after tomorrow. A stateless one asks "the day after for where?" — and the illusion of conversation collapses.

**Applies when**

- Multi-turn conversations where later turns depend on earlier ones.
- Users naturally use pronouns, ellipsis, and back-references.

**Prevents failure modes:** [`context-loss`](https://github.com/prashibadkur11-creator/ai-failure-mode-taxonomy), [`hallucination`](https://github.com/prashibadkur11-creator/ai-failure-mode-taxonomy)

**Related patterns:** `confirmation-for-irreversible-actions`

---
