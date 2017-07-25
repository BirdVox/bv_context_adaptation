import os
import sys
sys.path.append("../src")
import localmodule

units = localmodule.get_units()
augmentations = localmodule.get_augmentations()
augmentations.pop("original")
file_path = "002.sh"

with open(file_path, "w") as f:
    f.write("# This shell script executes the Slurm jobs for data augmentation.\n")
    f.write("\n")
    # Loop over recording units
    for unit in units:
        unit_str = str(unit).zfill(2)
        # Loop over augmentations
        for aug_str in augmentations:
            n_aug_instances = augmentations[aug_str]
            # Loop over instances
            for aug_instance_id in range(n_aug_instances):
                aug_instance_str = str(aug_instance_id)
                job_name = "-".join(["002", unit_str, aug_str, aug_instance_str])
                sbatch_str = "sbatch " + job_name + ".sbatch"
                f.write(sbatch_str + "\n")
            f.write("\n")
        f.write("\n")

# Grant permission to execute the file
# https://stackoverflow.com/a/30463972
mode = os.stat(file_path).st_mode
mode |= (mode & 0o444) >> 2
os.chmod(file_path, mode)
