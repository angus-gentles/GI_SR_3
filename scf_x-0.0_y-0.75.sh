#!/usr/bin/env bash
# Job name
#SBATCH --job-name s-75
#SBATCH --partition=highmem
#SBATCH --qos=highmem
#SBATCH --time 24:00:00
#SBATCH -N 5
#SBATCH --tasks-per-node=128
#SBATCH --cpus-per-task=1
#SBATCH --output=log_files/do_scf_0.0_0.75.log
export OMP_NUM_THREADS=1
source /work/i254/i254/gentles/tools/setup_supercell.sh
source run_them_functions.sh

run_them_scf 0.0 0.75 3
