* If you don't have it already, download and install either the Anaconda or the Miniconda Python 3 distribution.

* Create a conda environment with Python 3.5
`conda create -n lostanlen_spl2017 python=3.5`

* Activate environment lostanlen_spl2017
`source activate lostanlen_spl2017`

* Install numpy 

* Install h5py (custom license)
`conda install h5py`

* Install pandas (BSD 3-Clause license)
`conda install pandas`

* Install librosa (Brian McFee, ISC license)
`conda install -c conda-forge librosa`

* Install pysoundfile
`conda install -c carlthome pysoundfile`

* Install keras (François Chollet, MIT license)
`conda install -c conda-forge keras`

* Install Vesper (Harold Mills, MIT license)
`conda install -c haroldmills vesper`

* Clone and install muda v0.2 (Brian McFee, ISC license)
git clone https://github.com/bmcfee/muda.git
pip install -e muda

* Install mir_eval