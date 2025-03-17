#!/bin/bash

#SBATCH --job-name=run_tests
#SBATCH --time=00:10:00
#SBATCH --output="stdout.txt"
#SBATCH --error="stderr.txt"
#SBATCH --account=plgpympdatampiswe-cpu
#SBATCH --cpus-per-task=1
#SBATCH --partition=plgrid
#SBTACH --ntasks-per-node=1
#SBATCH --mem=5G

module load python
echo "python loaded!"
source ../venv/bin/activate
echo "venv activated!"
#time srun python -m modelrunner run_examples.py
srun python little_script.py
echo "scipt finished!"
