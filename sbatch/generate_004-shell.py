import os
import sys

sys.path.append("../src")
import localmodule


# Define constants.
units = localmodule.get_units()
augmentations = localmodule.get_augmentations()
file_path = "004.sh"


# Open shell file.
with open(file_path, "w") as f:
    # Print header.
    f.write("# This shell script executes the Slurm jobs for storing waveforms into HDF5 containers.\n")
    f.write("\n")

    # Loop over augmentations.
    for aug_str in augmentations:

        # Loop over instances.
        n_instances = augmentations[aug_str]
        for instance_id in range(n_instances):
            instance_str = str(instance_id)

            if aug_str == "original":
                instanced_aug_str = aug_str
            else:
                instanced_aug_str = "_".join([aug_str, instance_str])

            # Loop over recording units.
            for unit_str in units:
                # Define job name.
                job_name = "_".join(["004", instanced_aug_str, unit_str])
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
