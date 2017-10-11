import os
import sys

sys.path.append("../src")
import localmodule


# Define constants.
aug_kinds = ["all", "noise", "none", "pitch", "stretch"]
units = localmodule.get_units()
script_name = "018_evaluate-icassp-convnet-full-audio.py"
script_path = os.path.join("..", "src", script_name)
n_trials = 10


# Loop over kinds of data augmentation.
for aug_kind_str in aug_kinds:

    # Loop over test units.
    for test_unit_str in units:

        # Loop over trials.
        for trial_id in range(n_trials):
            job_name = "_".join([
                "018",
                "aug-" + aug_kind_str,
                "test-" + test_unit_str,
                "trial-" + str(trial_id)
            ])
            file_name = job_name + ".sbatch"
            script_list = [
                script_path, aug_kind_str, test_unit_str, str(trial_id)]
            script_path_with_args = " ".join(script_list)

            with open(file_name, "w") as f:
                f.write("#!/bin/bash\n")
                f.write("\n")
                f.write("#BATCH --job-name=" + job_name + "\n")
                f.write("#SBATCH --nodes=1\n")
                f.write("#SBATCH --tasks-per-node=1\n")
                f.write("#SBATCH --cpus-per-task=1\n")
                f.write("#SBATCH --time=0:10:00\n")
                f.write("#SBATCH --mem=1GB\n")
                f.write("#SBATCH --output=slurm_" + job_name + "_%j.out\n")
                f.write("\n")
                f.write("module purge\n")
                f.write("\n")
                f.write("# The argument is the kind of data augmentation.\n")
                f.write("python " + script_path_with_args)
