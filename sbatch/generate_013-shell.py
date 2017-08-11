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


for aug_kind_str in aug_kinds:
    for trial_id in range(n_trials):
        trial_str = str(trial_id)
        file_path = "013_aug-" + aug_kind_str + "_trial-" + trial_str + ".sh"

        # Open shell file
        with open(file_path, "w") as f:
            # Print header
            f.write(
                "# This shell script executes Slurm jobs for thresholding " +
                "Old Bird onset detection functions: Thrush and Tseep.\n")
            f.write("\n")

            # Loop over recording units
            for unit_str in units:
                # Define job name.
                job_name = "_".join(
                    ["013", "aug-" + aug_kind_str, unit_str,
                     "trial-" + trial_str])
                sbatch_str = "sbatch " + job_name + ".sbatch"

                # Write SBATCH command to shell file.
                f.write(sbatch_str + "\n")

        # Grant permission to execute the shell file.
        # https://stackoverflow.com/a/30463972
        mode = os.stat(file_path).st_mode
        mode |= (mode & 0o444) >> 2
        os.chmod(file_path, mode)
