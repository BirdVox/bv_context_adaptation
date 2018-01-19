import numpy as np
import os
import sys

sys.path.append("../src")
import localmodule


# Define constants.
aug_kinds = ["all", "all-but-noise", "none"]
units = localmodule.get_units()
script_name = "045_evaluate-add-convnet-full-audio.py"
script_path = os.path.join("..", "..", "..", "src", script_name)
dataset_name = localmodule.get_dataset_name()
n_trials = 10


# Create folder.
script_dir = script_name[:-3]
os.makedirs(script_dir, exist_ok=True)
sbatch_dir = os.path.join(script_dir, "sbatch")
os.makedirs(sbatch_dir, exist_ok=True)
slurm_dir = os.path.join(script_dir, "slurm")
os.makedirs(slurm_dir, exist_ok=True)


# Define thresholds.
icassp_thresholds = 1.0 - np.linspace(0.0, 1.0, 201)[:-1]
n_thresholds = len(icassp_thresholds)


# Loop over augmentations.
for aug_kind_str in aug_kinds:

    # Loop over test units.
    for test_unit_str in units:

        # Retrieve fold such that unit_str is in the test set.
        folds = localmodule.fold_units()
        fold = [f for f in folds if test_unit_str in f[0]][0]
        test_units = fold[0]
        training_units = fold[1]
        validation_units = fold[2]
        predict_units = test_units + validation_units


        # Loop over trials.
        for trial_id in range(n_trials):

            # Define file path.
            file_path = os.path.join(sbatch_dir,
                script_name[:3] + "_" +\
                "aug-" + aug_kind_str + "_" +\
                "test-" + test_unit_str + "_" +\
                "trial-"+ str(trial_id) + ".sh")

            # Open shell file
            with open(file_path, "w") as f:
                # Print header
                f.write(
                    "# This shell script executes Slurm jobs for thresholding\n" +
                    "# predictions of convolutional\n" +
                    "# neural network with adaptive threshold on " +
                    dataset_name + " full audio\n" +
                    "# with logmelspec input.\n")
                f.write("# Augmentation kind: " + aug_kind_str + ".\n")
                f.write("# Test unit: " + test_unit_str + ".\n")
                f.write("# Trial ID: " + str(trial_id) + ".\n")
                f.write("\n")

                # Loop over test units.
                for predict_unit_str in predict_units:

                    # Define job name.
                    job_name = "_".join([
                        script_name[:3],
                        "aug-" + aug_kind_str,
                        "test-" + test_unit_str,
                        "predict-" + predict_unit_str,
                        "trial-" + str(trial_id)
                    ])
                    sbatch_str = "sbatch " + job_name + ".sbatch"
                    f.write(sbatch_str + "\n")

            # Grant permission to execute the shell file.
            # https://stackoverflow.com/a/30463972
            mode = os.stat(file_path).st_mode
            mode |= (mode & 0o444) >> 2
            os.chmod(file_path, mode)
