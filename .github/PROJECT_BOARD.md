# Recommended GitHub Project board

GitHub Projects (v2) can't be created via the current MCP tooling, so this file documents the recommended setup. Mirror it manually in **Projects → New project → Board view**.

## Project name

`Sermon Translator macOS`

## Columns

| Column | Purpose | When to move here |
|---|---|---|
| **Backlog** | Not started, not yet scheduled | Default for new issues |
| **Ready** | Up next, unblocked | Dependencies closed, ready to pick up |
| **In Progress** | Actively being worked on | When a branch is opened |
| **In Review** | PR open, awaiting review | When PR is opened |
| **Blocked** | Waiting on external input | Note the blocker in a comment |
| **Done** | Closed / merged | Auto on issue close |

## Automation (built-in)

- Issue added to project → **Backlog**
- PR opened referencing issue → **In Review**
- Issue closed / PR merged → **Done**

## Suggested swim lanes / labels

Group by **label** for a per-module view:

- `stt` — speech-to-text
- `tts` — text-to-speech (future)
- `translate` — translation (future)
- `app` — macOS app shell (future)

Or group by **phase** label (`phase-1` … `phase-7`) for STT progress at a glance.

## Initial population

At the time of writing, these issues exist and should be added:

- #1 [Epic] STT Live Transcription
- #2 Setup
- #3–#11 Per-file implementation issues (Phases 1–7)
- #12 Test fixtures

All start in **Backlog** except #2, which can move to **Ready** immediately.

## Milestones

Create these manually in **Issues → Milestones**:

1. **STT: Live Transcription Pipeline** — covers issues #1–#12
2. **TTS: Text-to-Speech** (placeholder, future module)
3. **Translation Module** (placeholder, future module)
4. **macOS App Integration** (placeholder, future module)

Assign issues #1–#12 to milestone 1 to get a clean progress bar.
