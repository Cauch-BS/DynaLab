#!/usr/bin/env python3
"""Local UbqShort tutorial run (hot, no restraints)."""

from local_runner import run_local


if __name__ == "__main__":
    run_local(sim_id="00-Hot", is_restr=False)
