import os
import sys

sys.path.append("../src")
import localmodule


# Define constants.
script_name = "046_train-pcen-add-convnet.py"
script_path = os.path.join("..", "..", "..", "src", script_name)
units = localmodule.get_units()
n_trials = 10
aug_kinds = ["all", "all-but-noise", "none"]


# Create folders.
sbatch_dir = os.path.join(script_name[:-3], "sbatch")
os.makedirs(sbatch_dir, exist_ok=True)
slurm_dir = os.path.join(script_name[:-3], "slurm")
os.makedirs(slurm_dir, exist_ok=True)


# Loop over augmentations.
for aug_kind_str in aug_kinds:

    # Loop over recording units.
    for unit_str in units:

        # Loop over trials.
        for trial_id in range(n_trials):

            # Define file path.
            trial_str = "trial-" + str(trial_id)
            job_name = "_".join([
                script_name[:3], "aug-" + aug_kind_str, unit_str, trial_str])
            file_name = job_name + ".sbatch"
            file_path = os.path.join(sbatch_dir, file_name)

            # Define script.
            script_list = [script_path, aug_kind_str, unit_str, str(trial_id)]
            script_path_with_args = " ".join(script_list)

            # Open file.
            with open(file_path, "w") as f:
                f.write("#!/bin/bash\n")
                f.write("\n")
                f.write("#BATCH --job-name=" + job_name + "\n")
                f.write("#SBATCH --nodes=1\n")
                f.write("#SBATCH --tasks-per-node=1\n")
                f.write("#SBATCH --cpus-per-task=1\n")
                if aug_kind_str == "all":
                    f.write("#SBATCH --time=12:00:00\n")
                else:
                    f.write("#SBATCH --time=6:00:00\n")
                f.write("#SBATCH --mem=8GB\n")
                f.write("#SBATCH --output=../slurm/slurm_" + job_name + "_%j.out\n")
                f.write("\n")
                f.write("module purge\n")
                f.write("\n")
                f.write("# The first argument is the name of the recording unit.\n")
                f.write("# The second argument is the duration of background.\n")
                f.write("python " + script_path_with_args)
