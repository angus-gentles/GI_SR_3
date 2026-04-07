#!/usr/bin/env bash
# Job name
#SBATCH --job-name 75s
#SBATCH --partition=highmem
#SBATCH --qos=highmem
#SBATCH --time 24:00:00
#SBATCH -N 5
#SBATCH --tasks-per-node=128
#SBATCH --cpus-per-task=1
#SBATCH --output=scf75.log
export OMP_NUM_THREADS=4
source /work/i254/i254/gentles/tools/setup_qe-test.sh

name=In1.0Ga0.0As0.25Sb0.75_cube_3x3x3
cur=$(pwd)

cd calc_5
srun -n ${SLURM_NPROCS} pw.x -in ${name}.5.scf.in > ${name}.5.scf.out
cd $cur
