# Using Mortal from the Backend

This document outlines how to build Mortal and integrate it with the backend.

## Build Mortal

1. **Install prerequisites** – A Python environment and a recent Rust compiler are required. Using [miniconda](https://docs.conda.io/en/latest/miniconda.html) and [rustup](https://rustup.rs/) is recommended.
2. **Clone the repository**
   ```bash
   git clone https://github.com/Equim-chan/Mortal.git
   cd Mortal
   ```
3. **Create and activate a conda environment**
   ```bash
   conda env create -f environment.yml
   conda activate mortal
   ```
4. **Install PyTorch** – Follow the [PyTorch installation guide](https://pytorch.org/get-started/locally/). Only the `torch` package is required.
5. **Build and install `libriichi`**
   ```bash
   cargo build -p libriichi --lib --release
   # Linux
   cp target/release/libriichi.so mortal/libriichi.so
   # Windows (MSYS2)
   cp target/release/riichi.dll mortal/libriichi.pyd
   ```
6. **Verify the build**
   ```bash
   cd mortal
   python - <<'PY'
import libriichi
help(libriichi)
PY
   ```

## Backend Integration

Once Mortal is built, the backend can start the AI as a subprocess that communicates via the MJAI protocol. A thin wrapper will launch the `mortal` executable, send game state events, and read the resulting actions. The high level flow is:

1. Start `mortal <player_id>` with the model directory mounted or passed via `--model-dir`.
2. Convert `GameState` objects to MJAI events using `ai_adapter`.
3. Write each event to the process's STDIN and parse JSON responses from STDOUT.
4. Apply the chosen action to the engine and continue the game loop.

This approach keeps Mortal decoupled from the core engine while allowing any MJAI-compatible AI to be used.
