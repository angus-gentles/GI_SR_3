# GI_SR_3

This directory contains the `GI_SR_3` alloy-supercell workflow and its generated results for the `3x3x3` supercell variant. It is a working area for generating special quasirandom structures, preparing Quantum ESPRESSO inputs, running relaxation and SCF calculations, and collecting band-gap and HDF5 summary outputs.

## What this directory is for

Compared with the older `GI_SR` workflow, this directory is centered on `3x3x3` cells and a more compact set of helper scripts. In practice, it combines:

- input templates and interpolation data,
- helper code for structure generation and QE input writing,
- per-composition calculation directories,
- summary plots, logs, and aggregated HDF5 results.

Because code and results live together here, this should be treated as an active project workspace rather than as a clean standalone package.

## Top-level layout

The contents fall into a few main groups.

### Core inputs

- `base.cube_3x3x3.crys`: template crystal structure for the `3x3x3` workflow.
- `base.sqsgen.yaml` and `base.gallides.yaml`: sqsgenerator-style templates for structure generation.
- `input_data.json`: base QE namelist data.
- `pseudopotentials.json`: pseudopotential mapping used when writing QE inputs.
- `U_base.json`: endpoint Hubbard `U` values used for interpolation.
- `a_base.json`: endpoint lattice constants used for alloy interpolation.
- `ksection_relax.txt`, `ksection_scf.txt`, and `ksection_bands.txt`: k-point path/section files for different QE stages.

### Workflow code and launch helpers

- `tools/`: reusable Python and shell helpers for structure generation, QE input writing, and post-relax extraction.
- `run_them_functions.sh`: shell functions that automate repeated relax/SCF workflows across generated configurations.
- `run_x-*.sh` and `scf_x-*.sh`: batch launch scripts for selected compositions.
- `make_base_crys.py`: small helper for converting a base YAML/result pair into a crystal or XYZ view.
- `analyse_bandgaps.py`, `make_bowing_graph.py`, and `test_bandgaps.py`: analysis helpers for post-processing the calculated results.

### Generated calculation data

- `dir_In..._cube_3x3x3/`: per-composition working directories.
- inside each `dir_*` directory: typically multiple `calc_*` subdirectories containing relax and SCF inputs/outputs.
- `log_files/`: stored logs from runs or summaries.

### Aggregated outputs

- `GI_SR_3.results.hdf5`, `GI_SR_2.results.hdf5`, and `GI_SR_4D.results.hdf5`: collected result datasets.
- `Ga_AsSb.bandgap.png` and related figures: composition-dependent summary plots.

## Typical workflow

The common workflow in this directory is:

1. Choose a composition, for example by selecting `x`, `y`, and `N=3`.
2. Generate or load the SQS-based structure description.
3. Convert the structure into a `.crys` file.
4. Interpolate the Hubbard `U` values for the alloy.
5. Write the QE relaxation input.
6. Run the relaxation job.
7. Extract the relaxed crystal coordinates.
8. Write the QE SCF input.
9. Run the SCF job and collect the resulting quantities into plots or HDF5 summaries.

The repeated multi-case version of this workflow is mostly driven by `run_them_functions.sh`.

## Tools directory

The local `tools/` directory contains the small reusable pieces for this workflow, including:

- `IGAS_supercell.py`: writes QE inputs from `.crys` or YAML-derived structures.
- `first_process.py`: generates SQS outputs and matching `.crys` / `.xyz` files.
- `quantum_espresso_first_step.py`: prepares the initial relaxation input.
- `quantum_espresso_scf.py`: prepares the follow-up SCF input.
- `relax_crys.py`: extracts the lowest-energy relaxed structure from QE output.
- `write_Uin.py`: writes composition-dependent Hubbard `U` values.
- `yaml_class.py` and `yaml_files.py`: YAML conversion helpers.
- `remove_wfc.sh`: deletes large QE scratch files after runs.

## Environment assumptions

This directory assumes a cluster-style execution environment with:

- Slurm variables such as `SLURM_NPROCS`,
- Quantum ESPRESSO available on the execution path or through sourced setup scripts,
- the shared `/work/i254/i254/gentles` filesystem layout,
- the required Python packages available in the configured environments.

Many scripts also assume they are run from specific working directories and that companion files such as `input_data.json`, `pseudopotentials.json`, `U_base.json`, and the relevant `ksection` files are nearby.

## Suggested starting points

If you are trying to understand or reuse this directory, start with:

- `run_them_functions.sh` for the high-level batch workflow,
- `input_data.json`, `U_base.json`, `a_base.json`, and the `ksection_*.txt` files for the physical and QE setup,
- the `tools/` scripts for the reusable implementation details,
- one representative `dir_In..._cube_3x3x3/` directory to see the generated structure of a real run.
