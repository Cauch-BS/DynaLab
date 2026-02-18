# Prerequisites for Reading and Using the Theory Set

## Purpose
Confirm that both environment prerequisites and reader prerequisites are in place before using the paper-guided workflows in this repository.

## Key Terms
- Poppler tools
- Python runtime
- optional PDF extraction libraries
- molecular dynamics basics
- coarse-grained model
- force-field parameterization

## Problem
Without a clear baseline for tools and background knowledge, paper concepts are hard to connect to DynaLab/Upside implementation paths.

## Method Flow
1. Verify required command-line tools.
2. Verify Python and package availability.
3. Verify repo runtime dependencies from `README.md`.
4. Identify missing pieces and apply remediation commands.
5. Confirm reader knowledge checklist.
6. Continue to [01-upside-sidechain-free-energy.md](./01-upside-sidechain-free-energy.md).

## Training/Parameterization Context
This document does not train a model. It sets up prerequisites so training and simulation concepts in later guides can be interpreted correctly.

## Environment Prerequisites Audit
Status snapshot from local checks:

| Area | Status | Notes |
|---|---|---|
| PDF rendering tools (`pdftoppm`, `pdfinfo`, `pdftotext`) | Pass | Installed via Poppler. |
| Python runtime (`python3`, `uv`) | Pass | Present. |
| PDF Python libs (`pdfplumber`, `pypdf`, `reportlab`) | Missing | Optional for Markdown authoring; useful for richer extraction/generation. |
| Build tools (`cmake`, `g++`/clang, `h5cc`, `h5c++`) | Pass | Present. |
| Core Python libs from repo `README.md` | Partial | `numpy`, `scipy` present; `tables`, `prody`, `pandas`, `h5py`, `mdtraj`, `pymbar` missing. |
| Environment vars (`UPSIDE_HOME`, `EIGEN_HOME`) | Missing | Needed for standard build/run scripts, not for reading docs. |

## Remediation Commands
Install PDF helper libraries:

```bash
uv pip install reportlab pdfplumber pypdf
```

Install repo Python dependencies from `README.md`:

```bash
uv pip install tables prody pandas h5py mdtraj pymbar
```

Fallback if `uv` is unavailable:

```bash
python3 -m pip install reportlab pdfplumber pypdf tables prody pandas h5py mdtraj pymbar
```

Set expected environment variables for typical local runs:

```bash
export UPSIDE_HOME=/Users/bazelcu/projects/DynaLab
export EIGEN_HOME=/path/to/eigen
```

## Reader Knowledge Prerequisites
Minimum background:
- basic molecular dynamics concepts (state, force, integration step)
- free energy and Boltzmann ensemble intuition
- coarse-grained modeling tradeoffs
- basic optimization concepts (objective, gradient, regularization)

Recommended additional background:
- belief propagation style approximations
- restrained and replica-exchange sampling
- spline-based potential parameterization

## Gap-Filling Mini Reading Path
1. Read paper abstracts and introductions first.
2. Focus on method figures and algorithm loops.
3. Map terms to code in `src/` and `py/` with the next two guides.
4. Revisit results/discussion only after mapping model components.

## Results
- You have a concrete pass/fail checklist for environment readiness.
- You have a clear reading path before touching simulation or training scripts.

## Limitations
- Dependency status can drift as local environments change.
- This checklist is scoped to this repository and these three papers.

## Repo Mapping
- Install and runtime context: `README.md`, `install.sh`, `source_sh`
- Configuration path: `py/upside_config.py`, `py/run_upside.py`
- Parameter inputs: `parameters/common/*`, `parameters/ff_2.1/*`

## Glossary
- **Poppler**: Suite of PDF CLI tools (`pdftoppm`, `pdfinfo`, `pdftotext`).
- **Parameterization**: Fitting force-field terms so simulated behavior matches target data.
- **Replica exchange**: Ensemble method that swaps configurations between temperatures.
