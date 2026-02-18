#!/usr/bin/env python3
"""Local UbqShort tutorial runner (no SLURM, no cluster-specific paths)."""

import os
import shutil
import subprocess as sp
import sys

import numpy as np
import tables as tb


# -----------------------------------------------------------------------------
# Tunable defaults for UbqShort tutorial
# -----------------------------------------------------------------------------
PDB_ID = "00_1ubq"
FF_VER = "2.1"
N_STEPS = 10000
FRAME_INTERVAL = 100

# Temperature / replica settings
T_CONST = 0.8
IS_TRANGE = True
T_MIN = 0.8
T_MAX = 1.2
IS_REPLEX = False
N_REP = 16

# Membrane / pulling settings (kept for parity with legacy scripts)
IS_SOLUTION = True
IS_ROTATE = False
SPACE_TRANS_FILE = "rotZ-table"
MEMB_EXCL_RES = ""
MEMB_THICK = 31.2
IS_CHANNEL = False
IS_CURVED = False
CURVE_RAD = 120.0
CURVE_SIGN = 1
CURVE_DYN = False
USE_LATERALP = False
IS_PULLING = False
IS_TENSION = False


def _paths():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    tutorial_dir = os.path.dirname(script_dir)  # tutorial/04.UbqShort
    all_tutorials_dir = os.path.dirname(tutorial_dir)  # tutorial
    repo_root = os.path.dirname(all_tutorials_dir)

    return {
        "script_dir": script_dir,
        "tutorial_dir": tutorial_dir,
        "repo_root": repo_root,
        "upside_utils_dir": os.path.join(repo_root, "py"),
        "param_dir_base": os.path.join(repo_root, "parameters"),
        "pdb_dir": os.path.join(tutorial_dir, "PDB"),
        "input_dir": os.path.join(tutorial_dir, "up_input"),
        "output_dir": os.path.join(tutorial_dir, "up_output"),
        "log_dir": os.path.join(tutorial_dir, "logs"),
    }


def run_local(sim_id, is_restr=False, restr_list="1-5:10,13,15,22-27:70-73", continue_sim=False):
    p = _paths()
    sys.path.insert(0, p["upside_utils_dir"])

    try:
        import run_upside as ru
    except ImportError as exc:
        raise RuntimeError("Could not import run_upside from py/") from exc

    for direc in (p["input_dir"], p["output_dir"], p["log_dir"]):
        if not os.path.exists(direc):
            os.makedirs(direc)

    config_fns = [os.path.join(p["output_dir"], f"{sim_id}.{rep}.up") for rep in range(N_REP)]
    log_file = os.path.join(p["log_dir"], f"{sim_id}.out")

    if continue_sim:
        missing = [fn for fn in config_fns if not os.path.exists(fn)]
        if missing:
            raise RuntimeError(
                "continue_sim=True but some trajectories are missing: " + ", ".join(missing)
            )

    if not continue_sim:
        pdb_path = os.path.join(p["pdb_dir"], f"{PDB_ID}.pdb")
        cmd = [
            sys.executable,
            os.path.join(p["upside_utils_dir"], "PDB_to_initial_structure.py"),
            pdb_path,
            os.path.join(p["input_dir"], PDB_ID),
            "--record-chain-breaks",
            "--allow-unexpected-chain-breaks",
            "--disable-recentering",
        ]
        sp.check_call(cmd)

    param_dir_common = os.path.join(p["param_dir_base"], "common")
    param_dir_ff = os.path.join(p["param_dir_base"], f"ff_{FF_VER}")

    if not continue_sim:
        kwargs = dict(
            rama_library=os.path.join(param_dir_common, "rama.dat"),
            rama_sheet_mix_energy=os.path.join(param_dir_ff, "sheet"),
            reference_state_rama=os.path.join(param_dir_common, "rama_reference.pkl"),
            hbond_energy=os.path.join(param_dir_ff, "hbond.h5"),
            rotamer_placement=os.path.join(param_dir_ff, "sidechain.h5"),
            dynamic_rotamer_1body=True,
            rotamer_interaction=os.path.join(param_dir_ff, "sidechain.h5"),
            environment_potential=os.path.join(param_dir_ff, "environment.h5"),
            bb_environment_potential=os.path.join(param_dir_ff, "bb_env.dat"),
            chain_break_from_file=os.path.join(p["input_dir"], f"{PDB_ID}.chain_breaks"),
            initial_structure=os.path.join(p["input_dir"], f"{PDB_ID}.initial.npy"),
        )

        if IS_ROTATE:
            kwargs["spatial_transform_from_table"] = SPACE_TRANS_FILE

        if not IS_SOLUTION:
            kwargs["surface"] = True
            kwargs["membrane_thickness"] = MEMB_THICK
            if MEMB_EXCL_RES:
                kwargs["membrane_exclude_residues"] = MEMB_EXCL_RES
            if IS_CHANNEL:
                kwargs["channel_membrane_potential"] = os.path.join(param_dir_ff, "membrane.h5")
            else:
                kwargs["membrane_potential"] = os.path.join(param_dir_ff, "membrane.h5")
            if USE_LATERALP:
                kwargs["membrane_lateral_potential"] = os.path.join(p["input_dir"], "lateral.dat")

        if IS_CURVED:
            kwargs["use_curvature"] = True
            kwargs["curvature_radius"] = CURVE_RAD
            kwargs["curvature_sign"] = CURVE_SIGN

        ru.upside_config(os.path.join(p["input_dir"], f"{PDB_ID}.fasta"), config_fns[0], **kwargs)

        if is_restr:
            ru.advanced_config(config_fns[0], restraint_groups=restr_list.split(":"))

        for rep in range(1, N_REP):
            shutil.copyfile(config_fns[0], config_fns[rep])
    else:
        if IS_PULLING:
            for rep in range(N_REP):
                with tb.open_file(config_fns[rep], "a") as t:
                    tip_pos = t.root.output.tip_pos[-1]
                    g = t.root.input.potential.MovingConst3D
                    if "start_pos" not in g:
                        t.create_earray(g, "start_pos", obj=tip_pos)
                    else:
                        g.start_pos[:] = tip_pos
                    g._v_attrs.initialized_by_coord = 0

        ru.continue_sim(config_fns)

        if IS_CURVED and CURVE_DYN:
            for rep in range(N_REP):
                with tb.open_file(config_fns[rep], "a") as t:
                    curv_last = t.root.output.Const3D_0[-1, 0, :]
                    t.root.input.potential.Const3D_curvature_center.value[0, :] = curv_last

    if CURVE_DYN:
        extra_args = ["--curvature-changer-interval", "10"]
    else:
        extra_args = ["--integrator", "mv", "--inner-step", "2"]

    if not IS_TRANGE:
        temps = [T_CONST] * N_REP
        swap_sets = None
        rep_int = None
    else:
        temps = np.geomspace(T_MIN, T_MAX, num=N_REP)
        if IS_REPLEX:
            swap_sets = ru.swap_table2d(1, N_REP)
            rep_int = 20.0
        else:
            swap_sets = None
            rep_int = None

    if IS_SOLUTION:
        dis_recenter = IS_ROTATE or IS_PULLING
        dis_z_recenter = True
    else:
        dis_recenter = True
        dis_z_recenter = True

    with open(log_file, "w") as log:
        # run_upside emits stdout; keep a local log for parity with old scripts
        log.write(f"Starting local run for {sim_id}\n")
        log.write(f"Configs: {' '.join(config_fns)}\n")
        log.flush()

        job = ru.run_upside(
            "",
            config_fns,
            N_STEPS,
            FRAME_INTERVAL,
            n_threads=N_REP,
            replica_interval=rep_int,
            swap_sets=swap_sets,
            temperature=temps,
            disable_recentering=dis_recenter,
            disable_z_recentering=dis_z_recenter,
            extra_args=extra_args,
            seed=np.random.randint(10000),
            log_level="detailed",
            verbose=True,
        )
        rc = job.wait()

    if rc != 0:
        raise RuntimeError(f"Simulation failed for {sim_id} (rc={rc})")


if __name__ == "__main__":
    # Default behavior if someone runs this file directly.
    run_local(sim_id="00-Hot", is_restr=False)
