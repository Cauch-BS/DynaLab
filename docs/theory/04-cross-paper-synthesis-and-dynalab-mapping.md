# Cross-Paper Synthesis and DynaLab Mapping

## Purpose
Combine the three reference papers into one practical decision framework for modeling, training, and extension work in this repository.

## Key Terms
- representation choice
- smoothing strategy
- training signal
- validation targets
- transfer risk

## Problem
Each paper solves part of the same larger problem:
- represent biomolecular systems compactly
- preserve important physics
- train parameters from meaningful ensemble signals
- validate against behavior, not only static structure

The challenge is deciding how these pieces should guide concrete work in DynaLab/Upside.

## Method
Unified framework:
1. Choose representation (protein-centric Upside today; RNA extension path future).
2. Choose smoothing/inference layer (integrated side-chain free energy for proteins).
3. Choose training objective (trajectory-aware contrastive divergence style).
4. Choose validation set (folding, ensembles, thermodynamics, and specific observables).
5. Feed outcomes back into parameter updates and repeat.

## Training/Parameterization
Comparative view:

| Paper | Primary training signal | Main objective |
|---|---|---|
| Side-chain free-energy paper | side-chain conformation likelihood | accurate and fast side-chain energetics |
| Trajectory-based training paper | restrained vs freer ensemble contrast | balanced force-field terms for folding/ensembles |
| CRANBERRY paper | ConDiv + experimental/disordered fine-tuning | RNA structure plus thermodynamic realism |

Practical implication:
- DynaLab already contains infrastructure for the first two columns in protein workflows.
- RNA would require new representation and parameter sources before applying the third directly.

## Results
Cross-paper conclusions:
- Coarse-graining can improve both speed and quality when parameterization is done against the right ensemble-level targets.
- Smoothing and training must be co-designed, not treated as independent steps.
- Validation should include native and non-native/disordered behavior.

## Limitations
- Current repository does not yet include RNA-specific simulation kernels.
- Some training scripts are legacy and may need modernization before large re-training campaigns.
- Paper results do not transfer automatically to new domains without matched data and retraining.

## Repo Mapping
Current protein-ready stack:
- engine and energies: `src/main.cpp`, `src/rotamer.cpp`, `src/hbond.cpp`, `src/environment.cpp`
- config and run entry points: `py/upside_config.py`, `py/run_upside.py`
- training-related utilities: `py/rotamer_parameter_estimation.py`
- practical examples: `tutorial/01.ProofofLife/run.py`, `tutorial/02.EquilibriumDynamics/run.py`, `tutorial/03.PullingDynamics/run.py`

RNA extension candidate insertion points:
- add new CG feature nodes in `src/coord_map.cpp` and energy terms in `src/*` interaction files
- extend config surface in `py/upside_config.py`
- introduce RNA parameter packs under `parameters/`

## Practical Checklist for Future Work
1. Confirm target domain: protein-only or protein-plus-RNA.
2. Lock representation and state variables before writing new potentials.
3. Define training ensembles and observables up front.
4. Build validation matrix that includes dynamics and thermodynamics.
5. Treat parameterization as iterative, with explicit failure-mode tracking.

## Glossary
- **Representation**: Chosen degrees of freedom in the coarse-grained model.
- **Training signal**: Data-derived quantity used to update parameters.
- **Validation observable**: Measured output used to assess model adequacy.

## Related Guides
- Index: [README.md](./README.md)
- Setup: [00-prerequisites.md](./00-prerequisites.md)
- Protein method details: [01-upside-sidechain-free-energy.md](./01-upside-sidechain-free-energy.md)
- Protein training details: [02-upside-trajectory-based-training.md](./02-upside-trajectory-based-training.md)
- RNA method details: [03-cranberry-rna-dynamics.md](./03-cranberry-rna-dynamics.md)
