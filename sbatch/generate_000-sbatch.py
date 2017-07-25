import os
import sys
sys.path.append("../src")
import localmodule

# Define constants
units = localmodule.get_units()
script_name = "000_generate_BirdVox-70k_wav.py"
script_path = os.path.join("..", "src", script_name)

# Loop over recording units
for unit in units:
    unit_str = "unit" + str(unit).zfill(2)
    job_name = "_".join(["000", unit_str])
    file_name = job_name + ".sbatch"
    script_path_with_args = " ".join([script_path, str(unit).zfill(2)])
    with open(file_name, "w") as f:
        f.write("#!/bin/bash\n")
        f.write("\n")
        f.write("#BATCH --job-name=" + job_name + "\n")
        f.write("#SBATCH --nodes=1\n")
        f.write("#SBATCH --tasks-per-node=1\n")
        f.write("#SBATCH --cpus-per-task=1\n")
        f.write("#SBATCH --time=0:30:00\n")
        f.write("#SBATCH --mem=4GB\n")
        f.write("#SBATCH --output=slurm_" + job_name + "_%j.out\n")
        f.write("\n")
        f.write("module purge\n")
        f.write("\n")
        f.write("# The integer passed to the Python script 000_generate_BirdVox-70k_wav.py\n")
        f.write("# corresponds to the ID of the recording unit in the list [1, 2, 3, 5, 7, 10].\n")
        f.write("python " + script_path_with_args)
