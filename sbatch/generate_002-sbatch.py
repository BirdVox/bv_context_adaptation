import os
import sys
sys.path.append("../src")
import localmodule

# Define constants
units = localmodule.get_units()
augmentations = localmodule.get_augmentations()
augmentations.remove("original")
model_name = "002_augment_BirdVox-70k.py"

# Loop along recording units
for unit in units:
    unit_str = str(unit).zfill(2)
    # Loop along augmentations
    for aug_str in augmentations:
        job_name = "002-" + unit_str + "-" + aug_str
        model_name_with_args = " ".join([model_name, unit_str, aug_str])
        file_name = job_name + ".sbatch"
        with open(file_name, "w") as f:
            f.write("#!/bin/bash\n")
            f.write("\n")
            f.write("#BATCH --job-name=" + job_name + "\n")
            f.write("#SBATCH --nodes=1\n")
            f.write("#SBATCH --tasks-per-node=1\n")
            f.write("#SBATCH --cpus-per-task=1\n")
            f.write("#SBATCH --time=2:00:00\n")
            f.write("#SBATCH --mem=4GB\n")
            f.write("#SBATCH --output=slurm_" + job_name + "_%j.out\n")
            f.write("\n")
            f.write("module purge\n")
            f.write("\n")
            f.write("python ../src/" + model_name_with_args)
