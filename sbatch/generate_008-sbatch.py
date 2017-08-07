import os
import sys

sys.path.append("../src")
import localmodule


# Define constants
units = localmodule.get_units()
odfs = ["thrush", "tseep"]
n_thresholds = 100
threshold_hop = 10
threshold_range = np.arange(0, n_thresholds, threshold_hop)
n_threshold_groups = len(threshold_range)
script_name = "008_threshold-oldbird.py"
script_path = os.path.join("..", "src", script_name)


# Loop over recording units
for unit_str in units:
    job_name = "_".join(["007", unit_str])
    file_name = job_name + ".sbatch"
    script_path_with_args = " ".join([script_path, unit_str])
    with open(file_name, "w") as f:
        f.write("#!/bin/bash\n")
        f.write("\n")
        f.write("#BATCH --job-name=" + job_name + "\n")
        f.write("#SBATCH --nodes=1\n")
        f.write("#SBATCH --tasks-per-node=1\n")
        f.write("#SBATCH --cpus-per-task=1\n")
        f.write("#SBATCH --time=2:00:00\n")
        f.write("#SBATCH --mem=1GB\n")
        f.write("#SBATCH --output=slurm_" + job_name + "_%j.out\n")
        f.write("\n")
        f.write("module purge\n")
        f.write("\n")
        f.write("# The argument is the name of the recording unit.\n")
        f.write("python " + script_path_with_args)
