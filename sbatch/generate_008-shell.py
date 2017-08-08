import numpy as np
import os
import sys

sys.path.append("../src")
import localmodule


# Define constants
units = localmodule.get_units()
odfs = ["thrush", "tseep"]
file_path = "008.sh"
n_thresholds = 100
threshold_hop = 5
threshold_range = np.arange(0, n_thresholds, threshold_hop)
n_threshold_groups = len(threshold_range)


# Open shell file
with open(file_path, "w") as f:
    # Print header
    f.write("# This shell script executes all Slurm jobs for thresholding " +
        "Old Bird onset detection functions: Thrush and Tseep.\n")
    f.write("\n")

    # Loop over recording units
    for unit_str in units:

        # Loop over onset detection function ("thrush" and "tseep")
        for odf_str in odfs:

            # Loop over groups of thresholds
            for threshold_group_id in range(n_threshold_groups):
                # Define group of thresholds.
                thr_start = threshold_range[threshold_group_id]
                thr_start_str = str(thr_start).zfill(2)
                thr_stop = thr_start + threshold_hop - 1
                thr_stop_str = str(thr_stop).zfill(2)
                group_range_str = "-".join(["th", thr_start_str, thr_stop_str])

                # Define job name.
                job_name = "_".join(["008", unit_str, odf_str, group_range_str])
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
