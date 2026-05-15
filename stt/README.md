# STT - Live Transcription

Real-time speech-to-text on Apple Silicon using CoreML encoder + MLX decoder + Silero VAD + CIF word boundary detection.

---

## How it works

```
Microphone (16kHz mono)
    ↓
Silero VAD — detects silence after speech (~400–600ms), triggers encode
    ↓
Mel spectrogram — converts audio to frequency image, padded to 30s
    ↓
CoreML encoder — runs on Apple Neural Engine, outputs acoustic features
    ↓
CIF model — watches encoder features, fires at word boundaries
    ↓
MLX decoder — converts fired features into text words
    ↓
Token buffer — holds words until stable across passes
    ↓
Transcript output — words emitted live as spoken
```

---

## Architecture

### Component roles

| Component | Input | Output | Role |
|---|---|---|---|
| `microphone.py` | — | Raw audio | Captures 16kHz mono mic stream |
| `silero_vad.py` | Raw audio | Speech chunks | Detects sentence end via silence |
| `mel_spectrogram.py` | Speech chunk | Mel frames | Converts audio to 80×3000 mel image |
| `coreml_encoder.py` | Mel frames | Acoustic features | Neural Engine encoding (~10–20ms) |
| `cif_detector.py` | Acoustic features | Word boundary signals | Fires when a word is confirmed |
| `mlx_decoder.py` | Features + signals | Text words | Decodes word by word |
| `token_buffer.py` | Text words | Stable words | Emits only stable, confirmed words |

### Key design decisions

- **VAD triggers encoding** — only encode when speech ends, not on a timer
- **CoreML on Neural Engine** — up to 18x faster encoding, low power
- **CIF for live typewriter effect** — words appear as spoken, not after full sentence
- **Token buffer** — prevents flickering by holding words until stable
- **Safety cap** — encode anyway at 8–10s for long unpaused speech

---

## Project structure

```
live-transcription/
│
├── main.py                        # Entry point, starts the pipeline
│
├── pipeline/
│   └── transcriber.py             # Orchestrates all components together
│
├── audio/
│   └── microphone.py              # Mic input stream, 16kHz mono
│
├── vad/
│   └── silero_vad.py              # Speech/silence detection, triggers encode
│
├── mel/
│   └── mel_spectrogram.py         # Audio → mel spectrogram, pads to 30s
│
├── encoder/
│   └── coreml_encoder.py          # Loads .mlpackage, runs on Neural Engine
│
├── cif/
│   └── cif_detector.py            # Loads medium.npz, fires on word boundaries
│
├── decoder/
│   └── mlx_decoder.py             # Loads MLX weights, decodes features → text
│
├── buffer/
│   └── token_buffer.py            # Stability check, emits confirmed words
│
├── models/
│   ├── coreml/
│   │   └── ggml-base-encoder.mlpackage
│   ├── mlx/
│   │   └── mlx_base/
│   └── cif/
│       └── medium.npz
│
├── config.py                      # VAD threshold, buffer settings, model paths
└── requirements.txt
```

---

## Implementation order

Build and test each phase with a known `.wav` file before moving to the next. Do not use live mic until Phase 6.

### Phase 1 — Audio foundation
- [ ] `microphone.py` — stream raw audio from mic
- [ ] `mel_spectrogram.py` — convert audio to mel, verify output shape `[1, 80, 3000]`

### Phase 2 — Encoding
- [ ] `coreml_encoder.py` — load `.mlpackage`, feed mel, verify encoder output shape
- [ ] Test: feed a `.wav` file through Phase 1–2, print encoder output shape

### Phase 3 — Decoding
- [ ] `mlx_decoder.py` — load MLX weights, feed encoder features, verify text output
- [ ] Test: full pipeline on `.wav` file, should produce rough transcript

### Phase 4 — Word boundary
- [ ] `cif_detector.py` — load `medium.npz`, feed encoder features, verify it fires at words

### Phase 5 — Stability
- [ ] `token_buffer.py` — implement stability check, verify words emit without flickering

### Phase 6 — Sentence detection
- [ ] `silero_vad.py` — integrate VAD, test silence detection on live mic input

### Phase 7 — Connect everything
- [ ] `transcriber.py` — wire all components together
- [ ] `main.py` — entry point, load config, run pipeline

---

## Models

| Model | File | Purpose |
|---|---|---|
| Whisper base (CoreML) | `ggml-base-encoder.mlpackage` | Encoder on Neural Engine |
| Whisper base (MLX) | `mlx_base/` | Decoder on Apple Silicon |
| CIF medium | `medium.npz` | Word boundary detection |

### Generating the CoreML encoder

```bash
git clone https://github.com/ggml-org/whisper.cpp.git
./scripts/generate_coreml_encoder.sh base.en
```

---

## Key parameters (config.py)

| Parameter | Default | Notes |
|---|---|---|
| `VAD_SILENCE_MS` | 500 | Milliseconds of silence before triggering encode |
| `VAD_MAX_DURATION_S` | 10 | Safety cap — encode even without silence |
| `BUFFER_STABILITY_PASSES` | 2 | Passes before a word is emitted |
| `SAMPLE_RATE` | 16000 | Required by Whisper |
| `MEL_FRAMES` | 3000 | Fixed CoreML input size (30s) |
| `COREML_COMPUTE_UNITS` | `CPU_AND_NE` | Best power efficiency |

---

## References

- [Lightning-SimulWhisper](https://github.com/altalt-org/Lightning-SimulWhisper) — base implementation this project adapts
- [Silero VAD](https://github.com/snakers4/silero-vad)
- [MLX](https://github.com/ml-explore/mlx)
- [whisper.cpp CoreML](https://github.com/ggml-org/whisper.cpp)Live Transcription

Real-time speech-to-text on Apple Silicon using CoreML encoder + MLX decoder + Silero VAD + CIF word boundary detection.

---

## How it works

```
Microphone (16kHz mono)
    ↓
Silero VAD — detects silence after speech (~400–600ms), triggers encode
    ↓
Mel spectrogram — converts audio to frequency image, padded to 30s
    ↓
CoreML encoder — runs on Apple Neural Engine, outputs acoustic features
    ↓
CIF model — watches encoder features, fires at word boundaries
    ↓
MLX decoder — converts fired features into text words
    ↓
Token buffer — holds words until stable across passes
    ↓
Transcript output — words emitted live as spoken
```

---

## Architecture

### Component roles

| Component | Input | Output | Role |
|---|---|---|---|
| `microphone.py` | — | Raw audio | Captures 16kHz mono mic stream |
| `silero_vad.py` | Raw audio | Speech chunks | Detects sentence end via silence |
| `mel_spectrogram.py` | Speech chunk | Mel frames | Converts audio to 80×3000 mel image |
| `coreml_encoder.py` | Mel frames | Acoustic features | Neural Engine encoding (~10–20ms) |
| `cif_detector.py` | Acoustic features | Word boundary signals | Fires when a word is confirmed |
| `mlx_decoder.py` | Features + signals | Text words | Decodes word by word |
| `token_buffer.py` | Text words | Stable words | Emits only stable, confirmed words |

### Key design decisions

- **VAD triggers encoding** — only encode when speech ends, not on a timer
- **CoreML on Neural Engine** — up to 18x faster encoding, low power
- **CIF for live typewriter effect** — words appear as spoken, not after full sentence
- **Token buffer** — prevents flickering by holding words until stable
- **Safety cap** — encode anyway at 8–10s for long unpaused speech

---

## Project structure

```
live-transcription/
│
├── main.py                        # Entry point, starts the pipeline
│
├── pipeline/
│   └── transcriber.py             # Orchestrates all components together
│
├── audio/
│   └── microphone.py              # Mic input stream, 16kHz mono
│
├── vad/
│   └── silero_vad.py              # Speech/silence detection, triggers encode
│
├── mel/
│   └── mel_spectrogram.py         # Audio → mel spectrogram, pads to 30s
│
├── encoder/
│   └── coreml_encoder.py          # Loads .mlpackage, runs on Neural Engine
│
├── cif/
│   └── cif_detector.py            # Loads medium.npz, fires on word boundaries
│
├── decoder/
│   └── mlx_decoder.py             # Loads MLX weights, decodes features → text
│
├── buffer/
│   └── token_buffer.py            # Stability check, emits confirmed words
│
├── models/
│   ├── coreml/
│   │   └── ggml-base-encoder.mlpackage
│   ├── mlx/
│   │   └── mlx_base/
│   └── cif/
│       └── medium.npz
│
├── config.py                      # VAD threshold, buffer settings, model paths
└── requirements.txt
```

---

## Implementation order

Build and test each phase with a known `.wav` file before moving to the next. Do not use live mic until Phase 6.

### Phase 1 — Audio foundation
- [ ] `microphone.py` — stream raw audio from mic
- [ ] `mel_spectrogram.py` — convert audio to mel, verify output shape `[1, 80, 3000]`

### Phase 2 — Encoding
- [ ] `coreml_encoder.py` — load `.mlpackage`, feed mel, verify encoder output shape
- [ ] Test: feed a `.wav` file through Phase 1–2, print encoder output shape

### Phase 3 — Decoding
- [ ] `mlx_decoder.py` — load MLX weights, feed encoder features, verify text output
- [ ] Test: full pipeline on `.wav` file, should produce rough transcript

### Phase 4 — Word boundary
- [ ] `cif_detector.py` — load `medium.npz`, feed encoder features, verify it fires at words

### Phase 5 — Stability
- [ ] `token_buffer.py` — implement stability check, verify words emit without flickering

### Phase 6 — Sentence detection
- [ ] `silero_vad.py` — integrate VAD, test silence detection on live mic input

### Phase 7 — Connect everything
- [ ] `transcriber.py` — wire all components together
- [ ] `main.py` — entry point, load config, run pipeline

---

## Models

| Model | File | Purpose |
|---|---|---|
| Whisper base (CoreML) | `ggml-base-encoder.mlpackage` | Encoder on Neural Engine |
| Whisper base (MLX) | `mlx_base/` | Decoder on Apple Silicon |
| CIF medium | `medium.npz` | Word boundary detection |

### Generating the CoreML encoder

```bash
git clone https://github.com/ggml-org/whisper.cpp.git
./scripts/generate_coreml_encoder.sh base.en
```

---

## Key parameters (config.py)

| Parameter | Default | Notes |
|---|---|---|
| `VAD_SILENCE_MS` | 500 | Milliseconds of silence before triggering encode |
| `VAD_MAX_DURATION_S` | 10 | Safety cap — encode even without silence |
| `BUFFER_STABILITY_PASSES` | 2 | Passes before a word is emitted |
| `SAMPLE_RATE` | 16000 | Required by Whisper |
| `MEL_FRAMES` | 3000 | Fixed CoreML input size (30s) |
| `COREML_COMPUTE_UNITS` | `CPU_AND_NE` | Best power efficiency |

---

## References

- [Lightning-SimulWhisper](https://github.com/altalt-org/Lightning-SimulWhisper) — base implementation this project adapts
- [Silero VAD](https://github.com/snakers4/silero-vad)
- [MLX](https://github.com/ml-explore/mlx)
- [whisper.cpp CoreML](https://github.com/ggml-org/whisper.cpp)