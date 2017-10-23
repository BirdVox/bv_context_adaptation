import os
import sys

sys.path.append("../src")
import localmodule


# Define constants.
units = localmodule.get_units()
n_trials = 10
script_name = "023_train-svm.py"
script_path = os.path.join("..", "..", "..", "src", script_name)


# Create folders.
sbatch_dir = os.path.join(script_name[:-3], "sbatch")
os.makedirs(sbatch_dir, exist_ok=True)
slurm_dir = os.path.join(script_name[:-3], "slurm")
os.makedirs(slurm_dir, exist_ok=True)


# Loop over recording units.
for unit_str in units:

    # Loop over trials.
    for trial_id in range(n_trials):

        # Define trial string.
        trial_str = str(trial_id)

        # Define file path.
        job_name = "_".join(["023", unit_str, "trial-" + trial_str])
        file_name = job_name + ".sbatch"
        file_path = os.path.join(sbatch_dir, file_name)

        # Define script.
        script_list = [script_path, unit_str, str(trial_id).zfill(2)]
        script_path_with_args = " ".join(script_list)

        # Open file.
        with open(file_path, "w") as f:
            f.write("#!/bin/bash\n")
            f.write("\n")
            f.write("#BATCH --job-name=" + job_name + "\n")
            f.write("#SBATCH --nodes=1\n")
            f.write("#SBATCH --tasks-per-node=1\n")
            f.write("#SBATCH --cpus-per-task=1\n")
            f.write("#SBATCH --time=24:00:00\n")
            f.write("#SBATCH --mem=24GB\n")
            f.write("#SBATCH --output=../slurm/slurm_" + job_name + "_%j.out\n")
            f.write("\n")
            f.write("module purge\n")
            f.write("\n")
            f.write("# The first argument is the name of the recording unit.\n")
            f.write("# The second argument is the name of the trial.\n")
            f.write("python " + script_path_with_args)
