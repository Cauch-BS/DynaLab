# Theory Guides for `docs/refs/*.pdf`

## Purpose
This folder translates three reference PDFs into a repo-oriented theory guide for DynaLab/Upside users.

## Key Terms
- Upside
- Boltzmann ensemble
- contrastive divergence
- side-chain free energy
- sugar pucker
- noncanonical base pairing

## Scope and Source PDFs
- `docs/refs/Accurate_Calculation_Of_FreeE.pdf`
- `docs/refs/Trajectory_Based_Training.pdf`
- `docs/refs/RNA Dynamics Model.pdf`

These guides are grounded in the papers' named sections (Abstract, Introduction, Methods, Results, Discussion, Materials and Methods) and mapped to code paths in this repository.

## Method Flow
Reading order:
1. Start with [00-prerequisites.md](./00-prerequisites.md)
2. Read [01-upside-sidechain-free-energy.md](./01-upside-sidechain-free-energy.md)
3. Read [02-upside-trajectory-based-training.md](./02-upside-trajectory-based-training.md)
4. Read [03-cranberry-rna-dynamics.md](./03-cranberry-rna-dynamics.md)
5. Finish with [04-cross-paper-synthesis-and-dynalab-mapping.md](./04-cross-paper-synthesis-and-dynalab-mapping.md)

## Concept Map
| Guide | Main question | Main output |
|---|---|---|
| `00-prerequisites.md` | Are environment and background ready? | Setup and knowledge checklist |
| `01-upside-sidechain-free-energy.md` | How does Upside smooth dynamics by integrating side chains? | Mechanistic model view + code anchors |
| `02-upside-trajectory-based-training.md` | How is the force field trained against trajectories? | Training loop view + runtime hooks |
| `03-cranberry-rna-dynamics.md` | How is RNA handled with sugar pucker and noncanonical pairing? | RNA method summary + gap analysis for this repo |
| `04-cross-paper-synthesis-and-dynalab-mapping.md` | How do all three papers fit together for practical use? | Unified framework + implementation checklist |

## Repo Mapping
- Core simulation engine: `src/main.cpp`, `src/rotamer.cpp`, `src/hbond.cpp`, `src/environment.cpp`
- Configuration and run paths: `py/upside_config.py`, `py/run_upside.py`
- Parameter files: `parameters/ff_2.1/*`, `parameters/common/*`
- Worked examples: `tutorial/01.ProofofLife/run.py`, `tutorial/02.EquilibriumDynamics/run.py`, `tutorial/03.PullingDynamics/run.py`

## Limitations
- The RNA paper (CRANBERRY) is newer and conceptually aligned, but no direct RNA engine exists in this repo today.
- Line-exact derivations are intentionally summarized to keep this set implementation-focused.

## Glossary
- **Boltzmann ensemble**: Distribution over states weighted by free energy.
- **Contrastive divergence**: Training objective based on differences between nearby model and target ensembles.
- **Dynamic rotamer 1-body**: Upside option enabling side-chain state updates during simulation.
- **Sugar pucker**: Ribose conformational mode (for example C3'-endo vs C2'-endo) relevant to RNA geometry.
