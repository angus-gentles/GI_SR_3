#!/usr/bin/env bash
# Job name
#SBATCH --job-name 75
#SBATCH --partition=serial
#SBATCH --qos=serial
#SBATCH --time 24:00:00
#SBATCH -N 1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --output=sqsnshit.log
export OMP_NUM_THREADS=1
source /work/i254/i254/gentles/venvs/sqsgen/bin/activate
ls /work/i254/i254/gentles/venvs/

name=In1.0Ga0.0As0.25Sb0.75_cube_3x3x3
which sqsgen
sqsgen run iteration ${name}.yaml -di parameters -di objective -nm
