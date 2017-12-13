import numpy as np
import os
import sys

sys.path.append("../src")
import localmodule


# Define constants
aug_kinds = ["all", "all-but-noise", "none"]
folds = localmodule.fold_units()
units = localmodule.get_units()
n_trials = 10
script_name = "033_predict-pcen-convnet-full-audio.py"
script_path = os.path.join("..", "..", "..", "src", script_name)
script_str = script_name[:3]
script_folder =  script_name[:-3]


# Create folders.
os.makedirs(script_folder, exist_ok=True)
sbatch_dir = os.path.join(script_folder, "sbatch")
os.makedirs(sbatch_dir, exist_ok=True)
slurm_dir = os.path.join(script_folder, "slurm")
os.makedirs(slurm_dir, exist_ok=True)


# Loop over kind of augmentations
for aug_kind_str in aug_kinds:

    # Loop over recording units
    for test_unit_str in units:
        # Retrieve fold such that unit_str is in the test set.
        fold = [f for f in folds if test_unit_str in f[0]][0]
        validation_units = fold[2]
        predict_units = validation_units + [test_unit_str]

        # Loop over trials.
        for trial_id in range(n_trials):
            trial_str = "-".join(["trial", str(trial_id)])


            for predict_unit_str in predict_units:
                # Define job name.
                job_name = "_".join([
                    script_str,
                    "aug-" + aug_kind_str,
                    "test-" + test_unit_str,
                    trial_str,
                    "predict-" + predict_unit_str])
                file_name = job_name + ".sbatch"
                file_path = os.path.join(sbatch_dir, file_name)
                script_path_with_args = " ".join([
                    script_path,
                    aug_kind_str,
                    test_unit_str,
                    trial_str,
                    predict_unit_str])

                # Define slurm name.
                slurm_prefix = "../slurm/"
                slurm_suffix = "%j.out"
                slurm_name = slurm_prefix + "_".join([job_name, slurm_suffix])

                # Write call to python in SBATCH file.
                with open(file_path, "w") as f:
                    f.write("#!/bin/bash\n")
                    f.write("\n")
                    f.write("#BATCH --job-name=" + job_name + "\n")
                    f.write("#SBATCH --nodes=1\n")
                    f.write("#SBATCH --tasks-per-node=1\n")
                    f.write("#SBATCH --cpus-per-task=1\n")
                    f.write("#SBATCH --time=6:00:00\n")
                    f.write("#SBATCH --mem=1GB\n")
                    f.write("#SBATCH --output=" + slurm_name + "\n")
                    f.write("\n")
                    f.write("module purge\n")
                    f.write("\n")
                    f.write("# The first argument is the kind of augmentation.\n")
                    f.write("# The second argument is the name of the test unit.\n")
                    f.write("# The third argument is name of trial.\n")
                    f.write("# The fourth argument is the name of the prediction unit.\n")
                    f.write("python " + script_path_with_args)
