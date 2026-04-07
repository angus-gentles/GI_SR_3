#!/usr/bin/env bash
# Job name
#SBATCH --job-name res
#SBATCH --partition=highmem
#SBATCH --qos=highmem
#SBATCH --time 24:00:00
#SBATCH -N 5
#SBATCH --tasks-per-node=128
#SBATCH --cpus-per-task=1
#SBATCH --output=just_here.log

source /work/i254/i254/gentles/tools/setup_supercell.sh
base=In0.0Ga1.0As0.25Sb0.75_cube_3x3x3.8
srun -n ${SLURM_NPROCS} pw.x -i ${base}.scf.in > ${base}.scf.out