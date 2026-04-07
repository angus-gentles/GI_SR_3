#!/usr/bin/env bash
# Job name
#SBATCH --job-name 50s
#SBATCH --partition=highmem
#SBATCH --qos=highmem
#SBATCH --time 24:00:00
#SBATCH -N 5
#SBATCH --tasks-per-node=128
#SBATCH --cpus-per-task=1
#SBATCH --output=scf.log
export OMP_NUM_THREADS=4
source /work/i254/i254/gentles/tools/setup_qe-test.sh

name=In1.0Ga0.0As0.5Sb0.5_cube_3x3x3
cur=$(pwd)

for i in 4 5 6 7 8 9 ; do 
    cd calc_$i
    srun -n ${SLURM_NPROCS} pw.x -in ${name}.${i}.scf.in > ${name}.${i}.scf.out
    cd $cur
done

