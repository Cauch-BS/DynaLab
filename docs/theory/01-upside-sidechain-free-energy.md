# Upside Side-Chain Free Energy Model

## Purpose
Explain the core method from `docs/refs/Accurate_Calculation_Of_FreeE.pdf` and map it to active DynaLab/Upside code paths.

## Key Terms
- side-chain integration
- rotamer states
- belief propagation
- free-energy smoothing
- chi1 prediction

## Problem
The paper targets a central bottleneck in protein MD: slow sampling caused by detailed side-chain friction and expensive exploration of rugged landscapes.

Section anchors in the PDF:
- Abstract
- Introduction
- Methods (`Upside model`, `Side chain free energy evaluation`)
- Results
- Discussion

## Method
Core idea:
- Keep explicit backbone dynamics.
- Represent side chains with discrete rotamer-like states.
- Approximate side-chain free energy each step.
- Propagate free-energy derivatives back to backbone coordinates.

Conceptual inner loop (as described in Methods/Fig. 1):
1. Build backbone-dependent side-chain coordinates.
2. Initialize side-chain state probabilities.
3. Solve approximate pairwise-consistent side-chain distributions.
4. Compute side-chain free energy and derivatives.
5. Use derivatives in backbone force integration.

This is why dynamics can move on a smoother effective landscape than all-atom simulations with explicit side-chain rattling.

## Training/Parameterization
Paper framing:
- Parameters are fit to maximize likelihood of observed side-chain conformations (especially chi1) from structural data.
- The objective emphasizes matching side-chain statistics while preserving computational speed.

In repo terms:
- side-chain interaction parameters are loaded from `parameters/ff_2.1/sidechain.h5`
- dynamic side-chain updates are controlled by `--dynamic-rotamer-1body`

## Results
High-level takeaways from paper sections Results/Discussion:
- strong chi1 state prediction relative to established packers
- significant speed gains for side-chain treatment
- practical de novo folding capability for selected small systems

Interpretation for this repo:
- this paper is the conceptual basis for the rotamer/free-energy blocks that dominate Upside-specific behavior.

## Limitations
- Approximate side-chain inference introduces model bias.
- Accuracy depends on parameter quality and training data coverage.
- Coarse-grained representation can miss atomistic edge cases.

## Repo Mapping
Primary implementation anchors:
- `src/rotamer.cpp`: side-chain state graph, solve steps, rotamer free-energy logging.
- `src/hbond.cpp`: backbone and hydrogen-bond energy coupling used with smoothed dynamics.
- `src/environment.cpp`: environment coverage terms coupled to residue-level energetics.
- `py/upside_config.py`: wiring of rotamer/environment/hbond settings.

Configuration and parameters:
- `py/run_upside.py`: options such as `--rotamer-placement`, `--rotamer-interaction`, `--dynamic-rotamer-1body`.
- `parameters/ff_2.1/sidechain.h5`
- `parameters/ff_2.1/hbond.h5`
- `parameters/ff_2.1/environment.h5`
- `parameters/common/rama.dat`

Usage examples:
- `tutorial/01.ProofofLife/run.py`
- `tutorial/02.EquilibriumDynamics/run.py`

## Glossary
- **Rotamer**: Discrete side-chain conformation state.
- **chi1**: First side-chain dihedral angle, common packing accuracy target.
- **Free-energy smoothing**: Using integrated side-chain effects to reduce ruggedness of backbone dynamics.

## Related Guides
- Prerequisites: [00-prerequisites.md](./00-prerequisites.md)
- Training extension: [02-upside-trajectory-based-training.md](./02-upside-trajectory-based-training.md)
- Cross-paper synthesis: [04-cross-paper-synthesis-and-dynalab-mapping.md](./04-cross-paper-synthesis-and-dynalab-mapping.md)
