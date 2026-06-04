"""Central configuration for the STT live-transcription pipeline.

These values are referenced across the audio, VAD, mel, encoder, CIF,
decoder, and buffer stages. See stt/README.md for the parameter table
and architecture overview.
"""

from pathlib import Path

# --- Paths ---
STT_DIR = Path(__file__).resolve().parent
MODELS_DIR = STT_DIR / "models"

COREML_ENCODER_PATH = MODELS_DIR / "coreml" / "ggml-base-encoder.mlpackage"
MLX_DECODER_DIR = MODELS_DIR / "mlx" / "mlx_base"
CIF_MODEL_PATH = MODELS_DIR / "cif" / "medium.npz"

# --- Audio capture (microphone.py) ---
SAMPLE_RATE = 16000        # Hz, required by Whisper
CHANNELS = 1               # mono mic stream

# --- Voice activity detection (silero_vad.py) ---
VAD_THRESHOLD = 0.5        # speech-probability above this counts as speech
VAD_SILENCE_MS = 500       # silence after speech before triggering encode
VAD_MAX_DURATION_S = 10    # safety cap: encode even without a silence trigger

# --- Mel spectrogram (mel_spectrogram.py) ---
N_MELS = 80                # mel bins -> N_MELS x MEL_FRAMES image
MEL_FRAMES = 3000          # fixed CoreML input size (30s @ 160-sample hop)

# --- CoreML encoder (coreml_encoder.py) ---
COREML_COMPUTE_UNITS = "CPU_AND_NE"   # Neural Engine, best power efficiency

# --- Token buffer (token_buffer.py) ---
BUFFER_STABILITY_PASSES = 2   # passes a word must persist before it is emitted
