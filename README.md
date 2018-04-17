* If you don't have it already, download and install either the Anaconda or the Miniconda Python 3 distribution.

* Create a conda environment with Python 3.5
`conda create -n lostanlen_icassp2018 python=3.5`

* Activate environment lostanlen_spl2017
`source activate lostanlen_icassp2018`

* Install Tensorflow (Apache License 2.0) for deep learning
`conda install tensorflow`

* Install Keras (François Chollet, MIT License) for deep learning
`conda install keras`

* Install pandas (BSD 3-Clause license) for parsing annotations
`conda install pandas`

* Install pysoundfile for audio I/O
`conda install -c carlthome pysoundfile`

* Install muda (Brian McFee, ISC license) for data augmentation
`pip install muda`

* Install Vesper (Harold Mills, MIT license) for Old Bird flight call detector
`conda install -c haroldmills vesper`

* Install mir_eval (Colin Raffel, MIT license) for evaluation
`conda install -c carlthome mir_eval`

* Install pescador (ISC License) for stochastic multi-stream sampling
`conda install -c conda-forge pescador`

* Install scikit-learn (BSD License) for support vector machines
`conda install -c anaconda scikit-learn`

* Install skm (Justin Salamon) for spherical k-means
`pip install git+git://github.com/justinsalamon/skm`

* Results of the ICASSP 2018 paper by Lostanlen et al. are reproducible by running Python scripts `001` to `025` in this order, from the `src` folder. Arguments to these scripts are provided in the command line. The folders `sbatch/ID/sbatch` contains files for scheduling jobs with a Slurm workload manager, like the one that is maintained in the high-performance computing facility at NYU. These scripts can be generated programmatically by running Python scripts `sbatch/generate_ID.py`. The log files produced by the job manager are written to `sbatch/slurm`. We make them available to the general public, as they contain information on running times and memory footprints for each stage of the benchmark.


