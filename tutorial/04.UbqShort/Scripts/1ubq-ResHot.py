#!/usr/bin/env python3
"""Local UbqShort tutorial run (hot with restraints)."""

from local_runner import run_local


if __name__ == "__main__":
    run_local(sim_id="00-RH", is_restr=True, restr_list="1-5:10,13,15,22-27:70-73")
