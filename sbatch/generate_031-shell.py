import numpy as np
import os
import sys

sys.path.append("../src")
import localmodule


# Define constants
dataset_name = localmodule.get_dataset_name()
aug_kinds = ["all", "all-but-noise", "none"]
folds = localmodule.fold_units()
units = localmodule.get_units()
n_trials = 10
script_name = "031_predict-pcen-convnet-clips.py"
script_str = script_name[:3]
script_folder =  script_name[:-3]
script_path = os.path.join("..", "..", "..", "src", script_name)


# Create folders.
os.makedirs(script_folder, exist_ok=True)
sbatch_dir = os.path.join(script_folder, "sbatch")
os.makedirs(sbatch_dir, exist_ok=True)
slurm_dir = os.path.join(script_folder, "slurm")
os.makedirs(slurm_dir, exist_ok=True)


# Loop over augmentation kinds.
for aug_kind_str in aug_kinds:

    # Loop over trials.
    for trial_id in range(n_trials):
        trial_str = str(trial_id)
        file_name = "_".join([
            script_str, "aug-" + aug_kind_str, "trial-" + trial_str + ".sh"])
        file_path = os.path.join(sbatch_dir, file_name)

        # Open shell file.
        with open(file_path, "w") as f:
            # Print header
            f.write(
                "# This shell script executes Slurm jobs for running predictions\n" +
                "# with Justin Salamon's ICASSP 2017 convolutional neural network\n" +
                "# on " + dataset_name + ".\n")
            f.write("# Trial ID: " + trial_str + ".\n")
            f.write("# Augmentation kind: " + aug_kind_str + ".\n")
            f.write("\n")

            # Loop over test units.
            for test_unit_str in units:

                # Retrieve fold such that unit_str is in the test set.
                fold = [f for f in folds if test_unit_str in f[0]][0]
                validation_units = fold[2]
                predict_units = validation_units + [test_unit_str]

                # Loop over prediction units.
                for predict_unit_str in predict_units:
                    # Define job name.
                    job_name = "_".join([
                        script_str,
                        "aug-" + aug_kind_str,
                        "test-" + test_unit_str,
                        "trial-" + trial_str,
                        "predict-" + predict_unit_str])
                    sbatch_str = "sbatch " + job_name + ".sbatch"

                    # Write SBATCH command to shell file.
                    f.write(sbatch_str + "\n")
                f.write("\n")

        # Grant permission to execute the shell file.
        # https://stackoverflow.com/a/30463972
        mode = os.stat(file_path).st_mode
        mode |= (mode & 0o444) >> 2
        os.chmod(file_path, mode)
