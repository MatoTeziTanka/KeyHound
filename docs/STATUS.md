# KeyHound Status

Date: 2025-10-30

- GPU: Deferred on legacy GRID K1 (Kepler). CPU-only mode active.
- VM191: Running solver in CPU mode with quiet logging to `run.log`.
- EOL: Timestamped JSON artifacts, logs, and DB moved to `EOL/` to declutter.

Run CPU-only:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
PYTHONWARNINGS=ignore python3 main.py --puzzle 66 --log-level WARNING > run.log 2>&1 &
```

Enable GPU later:

```bash
nvidia-smi  # verify driver
python3 main.py --puzzle 66 --gpu --log-level INFO | tee run_gpu.log
```


