import os
import sys
sys.path.append("../src")
import localmodule

# Define constants
units = localmodule.get_units()
file_path = "000.sh"


# Open shell file
with open(file_path, "w") as f:
    # Print header
    f.write("# This shell script executes all Slurm jobs for generating WAV files.\n")
    f.write("\n")

    # Loop over recording units
    for unit in units:
        # Define job name
        unit_str = "unit" + str(unit).zfill(2)
        job_name = "_".join(["000", unit_str])
        sbatch_str = "sbatch " + job_name + ".sbatch"
        # Write SBATCH command to shell file.
        f.write(sbatch_str + "\n")


# Grant permission to execute the shell file.
# https://stackoverflow.com/a/30463972
mode = os.stat(file_path).st_mode
mode |= (mode & 0o444) >> 2
os.chmod(file_path, mode)
