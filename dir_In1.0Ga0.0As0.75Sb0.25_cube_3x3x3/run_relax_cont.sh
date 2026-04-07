#!/usr/bin/env bash
# Job name
#SBATCH --job-name 50s
#SBATCH --partition=standard
#SBATCH --qos=standard
#SBATCH --time 24:00:00
#SBATCH -N 4
#SBATCH --tasks-per-node=128
#SBATCH --cpus-per-task=1
#SBATCH --output=cont.cont.log
export OMP_NUM_THREADS=4
source /work/i254/i254/gentles/tools/setup_qe-test.sh

name=In1.0Ga0.0As0.75Sb0.25_cube_3x3x3
cur=$(pwd)
cd calc_3
srun -n ${SLURM_NPROCS} pw.x -in ${name}.3.relax.in > ${name}.3.relax.out
cd $cur
