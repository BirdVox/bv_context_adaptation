import os
import sys
sys.path.append("../src")
import localmodule

units = localmodule.get_units()
augmentations = localmodule.get_units()
file_path = "002.sh"

with open(file_path, "w") as f:
    for unit in units:
        unit_str = str(unit).zfill(2)
        for aug_str in augmentations:
            sbatch_str = "sbatch 002-" + unit_str + "-" + aug_str + ".sbatch"
            f.write(sbatch_str + "\n")

# Grant permission to execute the file
# https://stackoverflow.com/a/30463972
mode = os.stat(file_path).st_mode
mode |= (mode & 0o444) >> 2
os.chmod(file_path, mode)
