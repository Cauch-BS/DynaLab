#!/usr/bin/env python3
"""Compatibility entrypoint for legacy UbqShort invocation.

This now runs locally (no SLURM), and contains no cluster-specific paths.
"""

import sys

from local_runner import run_local


if __name__ == "__main__":
    sim_id = sys.argv[1] if len(sys.argv) > 1 else "00-Hot"
    is_restr = "RH" in sim_id or "Res" in sim_id
    run_local(sim_id=sim_id, is_restr=is_restr)
