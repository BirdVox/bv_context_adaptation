import os
import sys

sys.path.append("../src")
import localmodule


# Define constants.
units = localmodule.get_units()
n_trials = 10
script_name = "022_train-skm.py"


# Create folder.
sbatch_dir = os.path.join(script_name[:-3], "sbatch")
os.makedirs(sbatch_dir, exist_ok=True)
slurm_dir = os.path.join(script_name[:-3], "slurm")
os.makedirs(slurm_dir, exist_ok=True)


# Loop over trials.
for trial_id in range(n_trials):


    # Define file path.
    file_path = os.path.join(
        sbatch_dir, script_name[:3] + "_trial-" + str(trial_id) + ".sh")


    # Open shell file.
    with open(file_path, "w") as f:
        # Print header.
        f.write(
            "# This shell script executes the Slurm jobs for training " +
            "Salamon's unsupervised learning pipeline (PCA-SKM).\n")
        f.write("\n")

        # Loop over recording units.
        for unit_str in units:
            # Define job name.
            job_name = "_".join(["021", unit_str, "trial-"+str(trial_id)])
            sbatch_str = "sbatch " + job_name + ".sbatch"

            # Write SBATCH command to shell file.
            f.write(sbatch_str + "\n")


    # Grant permission to execute the shell file.
    # https://stackoverflow.com/a/30463972
    mode = os.stat(file_path).st_mode
    mode |= (mode & 0o444) >> 2
    os.chmod(file_path, mode)
