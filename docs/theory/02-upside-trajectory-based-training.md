# Upside Trajectory-Based Training (Contrastive Divergence)

## Purpose
Explain the method and implications of `docs/refs/Trajectory_Based_Training.pdf`, then connect the training logic to repo entry points and simulation controls.

## Key Terms
- contrastive divergence
- restrained vs unrestrained ensembles
- force-field balancing
- Boltzmann ensemble
- de novo folding

## Problem
Detailed force fields are not automatically better if parameterization quality is the dominant source of error. The paper addresses how to train a fast coarse-grained model so that ensemble behavior improves, not just static structure matching.

Section anchors in the PDF:
- Abstract
- Author Summary
- Introduction
- Methods
- Results
- Discussion

## Method
Core training logic:
1. Define two ensemble views (for example near-native/restrained and freer simulation states).
2. Estimate gradient-like updates from differences between these ensembles.
3. Apply iterative parameter updates to improve native-basin stability while preserving broader ensemble behavior.
4. Re-evaluate folding and thermodynamic observables.

This is a trajectory-aware calibration strategy, not a single-structure fitting procedure.

## Training/Parameterization
Paper emphasis:
- contrastive divergence on many proteins
- joint balancing across interaction terms
- trajectory-level signals drive parameter updates

Repo-adjacent anchors:
- `py/rotamer_parameter_estimation.py`: training/energy-gap style utilities related to Upside parameter fitting.
- `py/run_upside.py`: runtime controls for temperature schedules, swaps, and Monte Carlo intervals.
- `src/main.cpp`: replica exchange, swap sets, Monte Carlo pivot control, and logging outputs.

## Results
From paper results/discussion:
- improved de novo folding performance for small proteins
- better ability to recover realistic Boltzmann-like ensembles
- practical CPU-time reduction due to model efficiency

Interpretation for this repo:
- the training philosophy justifies why simulation controls and diagnostics are first-class, not optional extras.

## Limitations
- Contrastive divergence approximations can be sensitive to sampling quality.
- Success depends on representative training sets and careful regularization.
- Transfer outside protein-like training domains is uncertain without retraining.

## Repo Mapping
Training and config:
- `py/rotamer_parameter_estimation.py`
- `py/upside_config.py`
- `py/run_upside.py`

Runtime and sampling controls:
- `src/main.cpp` (`--replica-interval`, `--swap-set`, `--monte-carlo-interval`)
- `tutorial/02.EquilibriumDynamics/run.py`
- `tutorial/03.PullingDynamics/run.py`

Observable extraction:
- `py/get_info_from_upside_traj.py`
- `py/mdtraj_upside.py`

## Glossary
- **Contrastive divergence**: Parameter update based on discrepancy between nearby model and target distributions.
- **Restrained ensemble**: Simulations constrained near reference conformations.
- **Replica exchange**: Temperature or Hamiltonian swapping scheme to improve sampling.

## Related Guides
- Foundations: [01-upside-sidechain-free-energy.md](./01-upside-sidechain-free-energy.md)
- RNA contrast and extension: [03-cranberry-rna-dynamics.md](./03-cranberry-rna-dynamics.md)
- Synthesis: [04-cross-paper-synthesis-and-dynalab-mapping.md](./04-cross-paper-synthesis-and-dynalab-mapping.md)
