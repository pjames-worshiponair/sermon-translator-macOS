# Contributing

Thanks for working on the sermon translator. This doc keeps the workflow predictable so the project stays easy to navigate.

## Branching

Use short, kebab-case branch names prefixed with the phase or area:

```
phase-1/microphone
phase-2/coreml-encoder
fix/vad-threshold
docs/readme-update
```

Branch from `main`. PRs target `main`.

## Commits

Keep commits small and focused. A loose convention:

```
<area>: <imperative summary>

Longer explanation if needed. Reference issues with #N.
```

Examples:
```
audio: capture 16kHz mono mic stream (#3)
cif: load medium.npz and add fire detection (#7)
docs: clarify Phase 6 acceptance criteria
```

## Pull requests

1. One issue per PR where possible.
2. Link the issue in the PR description (`Closes #N`).
3. Fill out the PR template — especially the testing section.
4. Avoid committing model files (`.mlpackage`, `.npz`, MLX weights). Document acquisition in `stt/models/README.md` instead.
5. Run tests / lint locally before pushing.

## Code structure

The STT module follows the layout described in [`stt/README.md`](stt/README.md). When adding a new component:

- One responsibility per file.
- Class-based wrappers around stateful models (encoder, decoder, VAD, CIF).
- Pure functions for stateless transforms (mel).
- Config constants live in `stt/config.py`, not scattered through modules.

## Testing

Every phase issue includes acceptance criteria. Use the fixtures in `stt/tests/fixtures/` (see #12) so results are reproducible across machines.

Do not test against live mic until **Phase 6** — Phases 1–5 should be verified end-to-end with `.wav` files.

## Models

Model artefacts are large and version-sensitive. Never commit them. Instead, document where they come from and how to regenerate them in `stt/models/README.md`.

## Reviews

For solo work this still applies in spirit — read your own diff in the GitHub UI before merging. Catch what your editor missed.
