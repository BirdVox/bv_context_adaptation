import numpy as np
import os
import sys
sys.path.append("../src")
import localmodule

# Define constants.
units = localmodule.get_units()
tolerances = localmodule.get_tolerances()
script_name = "007_evaluate-skm.py"
script_path = os.path.join("..", "src", script_name)

# Loop over tolerances.
for tolerance in tolerances:
    tol_ms = int(np.round(1000*tolerance))
    tol_str = "tol" + str(tol_ms)
    # Loop over recording units.
    for unit_str in units:
        job_name = "_".join(["007", tol_str, unit_str])
        file_name = job_name + ".sbatch"
        script_path_with_args = " ".join([script_path, str(tol_ms), unit_str])
        with open(file_name, "w") as f:
            f.write("#!/bin/bash\n")
            f.write("\n")
            f.write("#BATCH --job-name=" + job_name + "\n")
            f.write("#SBATCH --nodes=1\n")
            f.write("#SBATCH --tasks-per-node=1\n")
            f.write("#SBATCH --cpus-per-task=1\n")
            f.write("#SBATCH --time=1:00:00\n")
            f.write("#SBATCH --mem=4GB\n")
            f.write("#SBATCH --output=slurm_" + job_name + "_%j.out\n")
            f.write("\n")
            f.write("module purge\n")
            f.write("\n")
            f.write("# The first argument is the tolerance in milliseconds.\n")
            f.write("# The second argument is the name of the recording unit.\n")
            f.write("python " + script_path_with_args)
