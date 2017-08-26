import numpy as np
import os
import sys

sys.path.append("../src")
import localmodule


# Define constants
dataset_name = localmodule.get_dataset_name()
aug_kinds = ["all", "noise", "none", "pitch", "stretch"]
script_name = "018_evaluate-icassp-convnet-clips.py"
script_path = os.path.join("..", "src", script_name)


for aug_kind_str in aug_kinds:
    file_path = "018_aug-" + aug_kind_str + ".sh"

        # Open shell file
        with open(file_path, "w") as f:
            # Print header
            f.write(
                "# This shell script executes Slurm jobs for evaluating\n" +
                "# Justin Salamon's ICASSP 2017 convolutional neural network\n" +
                "# on " + dataset_name + " clips.\n")
            f.write("# Augmentation kind: " + aug_kind_str + ".\n")
            f.write("\n")

            # Define job name.
            job_name = "_".join(["018", "aug-" + aug_kind_str])
            sbatch_str = "sbatch " + job_name + ".sbatch"

            f.write(sbatch_str + "\n")

        # Grant permission to execute the shell file.
        # https://stackoverflow.com/a/30463972
        mode = os.stat(file_path).st_mode
        mode |= (mode & 0o444) >> 2
        os.chmod(file_path, mode)
