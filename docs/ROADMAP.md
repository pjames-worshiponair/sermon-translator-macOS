# Project roadmap

High-level direction for the sermon translator macOS project. Detailed work happens in GitHub Issues / Milestones; this file is the bird's-eye view.

## Vision

Real-time, on-device sermon translation on Apple Silicon. Input: live preacher audio. Output: spoken translation in the listener's language, low latency, no cloud.

## Modules

### 1. STT — Speech-to-Text (current focus)

Real-time English transcription via Whisper CoreML encoder + MLX decoder + Silero VAD + CIF. See [`stt/README.md`](../stt/README.md).

Tracked under milestone **STT: Live Transcription Pipeline** (issues #1–#12).

### 2. Translation

On-device translation from English to one or more target languages. Likely candidates: an MLX-converted seq2seq model (NLLB, M2M-100, or a distilled variant).

Not yet started. Will get its own milestone and issues once STT Phase 7 is closing.

### 3. TTS — Text-to-Speech

Generate the translated speech. Options to explore: Apple's AVSpeechSynthesizer (zero cost, lower quality) vs. an MLX-hosted neural TTS (XTTS, Piper, etc).

Not yet started.

### 4. macOS app shell

SwiftUI app that wires the three modules together, exposes settings (target language, voice, mic device), and runs the pipeline. The Python modules likely run as a sidecar process the Swift app talks to over a local socket or via PythonKit.

Not yet started.

## Sequencing

The modules are mostly independent in implementation but chained at runtime, so they can be built in parallel after STT proves out. STT first because it's the highest-risk piece — if the latency budget doesn't work end-to-end on Apple Silicon, the whole project needs a rethink.

## Open questions

- Target languages for v1?
- Acceptable end-to-end latency target (preacher → translated audio)?
- Distribution model — TestFlight, direct download, Mac App Store?
- Whisper base.en vs. small.en vs. medium.en — accuracy / latency / power tradeoff?
