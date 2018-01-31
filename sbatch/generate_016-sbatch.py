import os
import sys

sys.path.append("../src")
import localmodule


# Define constants.
units = localmodule.get_units()
script_name = "016_run-spectral-flux.py"
script_path = os.path.join("..", "..", "..", "src", script_name)


# Create folder.
script_dir = script_name[:-3]
os.makedirs(script_dir, exist_ok=True)
sbatch_dir = os.path.join(script_dir, "sbatch")
os.makedirs(sbatch_dir, exist_ok=True)
slurm_dir = os.path.join(script_dir, "slurm")
os.makedirs(slurm_dir, exist_ok=True)


# Loop over recording units.
for unit_str in units:
    job_name = "_".join(["016", unit_str])
    file_name = job_name + ".sbatch"
    script_list = [script_path, unit_str]
    script_path_with_args = " ".join(script_list)
    with open(file_name, "w") as f:
        f.write("#!/bin/bash\n")
        f.write("\n")
        f.write("#BATCH --job-name=" + job_name + "\n")
        f.write("#SBATCH --nodes=1\n")
        f.write("#SBATCH --tasks-per-node=1\n")
        f.write("#SBATCH --cpus-per-task=1\n")
        f.write("#SBATCH --time=0:10:00\n")
        f.write("#SBATCH --mem=8GB\n")
        f.write("#SBATCH --output=slurm_" + job_name + "_%j.out\n")
        f.write("\n")
        f.write("module purge\n")
        f.write("\n")
        f.write("# The argument is the name of the recording unit.\n")
        f.write("python " + script_path_with_args)
