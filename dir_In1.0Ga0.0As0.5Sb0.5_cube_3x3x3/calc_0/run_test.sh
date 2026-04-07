#!/usr/bin/env bash
# Job name
#SBATCH --job-name uhh
#SBATCH --partition=highmem
#SBATCH --qos=highmem
#SBATCH --time 24:00:00
#SBATCH -N 2
#SBATCH --tasks-per-node=128
#SBATCH --cpus-per-task=1
#SBATCH --output=uhh.log
export OMP_NUM_THREADS=1
source /work/i254/i254/gentles/tools/setup_sc_qe-7.3.1.sh
name=In1.0Ga0.0As0.5Sb0.5_cube_3x3x3.0
srun -n ${SLURM_NTASKS} pw.x < ${name}.bands.in > ${name}.bands.out


