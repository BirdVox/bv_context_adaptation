import numpy as np
import os
import sys

sys.path.append("../src")
import localmodule


# Define constants
aug_kinds = ["all", "noise", "original", "pitch", "stretch"]
units = localmodule.get_units()
n_trials = 10
script_name = "013_train-icassp-convnet.py"
script_path = os.path.join("..", "src", script_name)


# Loop over kind of augmentations
for aug_kind_str in aug_kinds:

    # Loop over recording units
    for unit_str in units:

        # Loop over trials.
        for trial_id in range(n_trials):
            trial_str = "-".join(["trial", str(trial_id)])

            # Define job name.
            job_name = "_".join(
                ["013", "aug-" + aug_kind_str, unit_str, trial_str])
            file_name = job_name + ".sbatch"
            script_path_with_args = " ".join(
                [script_path, aug_kind_str, unit_str, trial_str])

            # Write call to python in SBATCH file.
            with open(file_name, "w") as f:
                f.write("#!/bin/bash\n")
                f.write("\n")
                f.write("#BATCH --job-name=" + job_name + "\n")
                f.write("#SBATCH --nodes=1\n")
                f.write("#SBATCH --tasks-per-node=1\n")
                f.write("#SBATCH --cpus-per-task=1\n")
                f.write("#SBATCH --time=12:00:00\n")
                f.write("#SBATCH --mem=16GB\n")
                f.write("#SBATCH --output=slurm_" + job_name + "_%j.out\n")
                f.write("\n")
                f.write("module purge\n")
                f.write("module load cuda/8.0.44\n")
                f.write("module load cudnn/8.0v5.1\n")
                f.write("\n")
                f.write("# The first argument is the kind of augmentation.\n")
                f.write("# The second argument is the name of the recording unit.\n")
                f.write("# The third argument is name of trial.\n")
                f.write("python " + script_path_with_args)
