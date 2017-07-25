import os
import sys
sys.path.append("../src")
import localmodule

# Define constants.
units = localmodule.get_units()
augmentations = localmodule.get_augmentations()
del augmentations["original"]
file_path = "002.sh"


# Open shell file.
with open(file_path, "w") as f:
    # Print header.
    f.write("# This shell script executes the Slurm jobs for data augmentation.\n")
    f.write("\n")

    # Loop over augmentations.
    for aug_str in augmentations:

        # Loop over instances.
        n_instances = augmentations[aug_str]
        for instance_id in range(n_instances):
            instance_str = str(instance_id)

            # Loop over recording units.
            for unit in units:
                unit_str = "unit" + str(unit).zfill(2)
                # Define job name.
                job_name = "_".join(["002", aug_str, instance_str, unit_str])
                sbatch_str = "sbatch " + job_name + ".sbatch"
                # Write SBATCH command to shell file.
                f.write(sbatch_str + "\n")
            f.write("\n")
        f.write("\n")


# Grant permission to execute the shell file.
# https://stackoverflow.com/a/30463972
mode = os.stat(file_path).st_mode
mode |= (mode & 0o444) >> 2
os.chmod(file_path, mode)
