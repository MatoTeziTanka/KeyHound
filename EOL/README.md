EOL (End of Life) Archive
=========================

Purpose
-------
This directory stores files that are no longer actively used, legacy outputs, or temporary artifacts. They are preserved here for reference and can be safely ignored by day-to-day development.

Contents
--------
- Timestamped JSON result files from benchmarking, monitoring, and scan runs
- Other deprecated or legacy assets as identified during cleanup

Policy
------
- Do not delete files from this directory until confirmed unnecessary
- New artifacts should not be written here by default; use `data/` or `monitoring/` instead
- If any file becomes needed again, move it back to an appropriate location



\n- Archived GSMG solver moved from root to EOL/gsmg_puzzle_solver.py (2025-10-30). Use GSMG.IO repo for active work; future integration via --gsmg planned.
