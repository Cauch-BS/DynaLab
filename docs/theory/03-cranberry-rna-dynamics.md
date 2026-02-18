# CRANBERRY RNA Dynamics Model

## Purpose
Explain `docs/refs/RNA Dynamics Model.pdf` in implementation terms and clarify what is directly usable in the current DynaLab/Upside codebase versus what remains future work.

## Key Terms
- CRANBERRY
- sugar puckering
- noncanonical base pairing
- coarse-grained RNA
- ConDiv (contrastive-divergence style training)

## Problem
RNA dynamics need a model that can represent:
- native and disordered states
- thermodynamic behavior
- noncanonical interactions
- sugar-pucker transitions

The paper argues that many existing coarse-grained approaches do not cover all of these simultaneously.

Section anchors in the PDF:
- Introduction
- Results and Discussion
- Materials and Methods

## Method
Core model choices:
1. Represent each nucleotide with six coarse-grained sites (phosphate, sugar sites, base sites).
2. Add explicit handling of sugar-puckering transitions (C3'-endo and C2'-endo behavior).
3. Model anisotropic base interactions, including noncanonical pairing geometries.
4. Use parameterized nonbonded terms and many-body bonded terms tied to conformational states.

## Training/Parameterization
Two-stage strategy in the paper:
1. Contrastive-divergence style training for core interaction terms.
2. Fine-tuning against stacking free energies and disordered-state structural observables.

This balances structure, thermodynamics, and cooperative folding behavior.

## Results
Reported outcomes include:
- competitive native-state fluctuation quality
- better agreement for disordered-state and stacking behaviors
- improved melting/cooperativity behavior versus compared baselines
- reversible de novo tetraloop folding in benchmark tests

Interpretation for DynaLab:
- conceptually aligned with Upside's emphasis on efficient coarse-grained dynamics plus data-driven calibration.

## Limitations
- Current repository is protein-focused and does not expose an RNA-native simulation path.
- CRANBERRY energy terms and RNA site definitions are not present in current `src/` or `py/` interfaces.
- Direct reproduction would require new data pipelines, parameter files, and node-level extensions.

## Repo Mapping
What exists today (conceptual analogs):
- spline and interaction machinery: `src/spline.cpp`, `src/sidechain_radial.cpp`, `src/bead_interaction.h`
- simulation and logging infrastructure: `src/main.cpp`, `src/deriv_engine.cpp`
- configuration pipeline: `py/upside_config.py`, `py/advanced_config.py`

What is missing for direct CRANBERRY parity:
- RNA nucleotide coarse-grained site definitions
- sugar-pucker specific bonded/interpolation terms
- noncanonical RNA base-pair interaction parameter sets
- RNA-focused training datasets and scripts

## Glossary
- **Sugar pucker**: Ribose ring conformation mode (often discussed as C3'-endo vs C2'-endo).
- **Noncanonical base pairing**: RNA base interactions beyond canonical Watson-Crick classes.
- **Anisotropic interaction**: Orientation-sensitive potential, not just distance-based.

## Related Guides
- Protein-side grounding: [01-upside-sidechain-free-energy.md](./01-upside-sidechain-free-energy.md)
- Training strategy parallel: [02-upside-trajectory-based-training.md](./02-upside-trajectory-based-training.md)
- Cross-model synthesis: [04-cross-paper-synthesis-and-dynalab-mapping.md](./04-cross-paper-synthesis-and-dynalab-mapping.md)
