# Contributing

Workflow conventions for this repo. Keep things predictable, keep history clean.

## Branch model

Git Flow lite:

```
main         ← released / stable only
  ↑
develop      ← integration branch, always working
  ↑
feature/*    ← new functionality
fix/*        ← bug fixes
hotfix/*     ← urgent fixes from main
docs/*       ← docs-only changes
chore/*      ← deps, tooling, refactors
test/*       ← test-only changes
```

Never commit directly to `main` or `develop`. Always go through a PR.

## Branch naming

Format: `{type}/{issue-number}-{short-desc}`

```
feature/3-microphone
feature/4-mel-spectrogram
fix/15-vad-threshold
docs/22-update-readme
chore/8-bump-deps
hotfix/30-crash-on-startup
```

Issue number = the GitHub issue this work closes. Short desc is kebab-case, 2–4 words.

## Daily flow

```bash
# Sync develop
git checkout develop
git pull

# Branch for the issue
git checkout -b feature/3-microphone

# Work in small commits
git add stt/audio/microphone.py
git commit -m "audio: add 16kHz mono stream class (#3)"

# Push early, push often
git push -u origin feature/3-microphone
```

If `develop` moves while you work:

```bash
git checkout develop
git pull
git checkout feature/3-microphone
git rebase develop
```

Use `rebase` for your own unpushed work, `merge` for shared branches.

## Commits

- Imperative mood: `"add X"` not `"added X"`
- Format: `<area>: <summary> (#N)`
- One logical change per commit
- Reference the issue with `(#N)` for auto-linking

Examples:
```
audio: capture 16kHz mono mic stream (#3)
cif: load medium.npz and add fire detection (#7)
docs: clarify Phase 6 acceptance criteria (#9)
```

## Pull requests

1. PR target: `develop` (not `main`)
2. Open as **Draft** early — push more commits as you iterate
3. Title: `<Type>: <summary>` (e.g. `Phase 1: implement microphone.py`)
4. Body: `Closes #N` + fill the PR template
5. When ready, mark **Ready for review**, self-review the diff
6. **Squash-merge** into develop (collapses commits into one)
7. Delete the branch after merge

One issue = one branch = one PR.

## Releases

When a milestone is done, release from `develop` to `main`:

```bash
git checkout main
git pull
git merge --no-ff develop -m "Release: STT Phase 1 complete"
git tag -a v0.1.0 -m "STT microphone + mel"
git push origin main --tags
```

Then create a GitHub Release from the tag with notes drafted from closed issues.

## Code structure

The STT module follows the layout in [`stt/README.md`](stt/README.md). When adding a new component:

- One responsibility per file
- Class-based wrappers around stateful models (encoder, decoder, VAD, CIF)
- Pure functions for stateless transforms (mel)
- Config constants live in `stt/config.py`, not scattered through modules

## Testing

Every phase issue has acceptance criteria. Use the fixtures in `stt/tests/fixtures/` (see #12) so results are reproducible.

Do not test against live mic until **Phase 6** — Phases 1–5 should be verified end-to-end with `.wav` files.

## Models

Never commit model artefacts (`.mlpackage`, `.npz`, MLX weights). Document acquisition in `stt/models/README.md`.

## Reviews

For solo work, read your own diff in GitHub's "Files changed" tab before merging. Catches what your editor missed.

## Rules of thumb

1. Pull before you branch
2. Branches live days, not weeks
3. Push at end of every work session — your laptop isn't a backup
4. Delete merged branches
5. Don't rebase pushed branches others might use (solo: fine)
