* If you don't have it already, download and install either the Anaconda or the Miniconda Python 3 distribution.

* Create a conda environment with Python 3.5
`conda create -n lostanlen_spl2017 python=3.5`

* Activate environment lostanlen_spl2017
`source activate lostanlen_spl2017`

* Install Tensorflow (Apache License 2.0) for deep learning
`conda install tensorflow`

* Install Keras (François Chollet, MIT License) for deep learning
`conda install keras`

* Install pandas (BSD 3-Clause license) for parsing annotations
`conda install pandas`

* Install pysoundfile for audio I/O
`conda install -c carlthome pysoundfile`

* Clone and install muda v0.2 (Brian McFee, ISC license) for data augmentation
```
git clone https://github.com/bmcfee/muda.git
pip install -e muda
```

* Install Vesper (Harold Mills, MIT license) for Old Bird flight call detector
`conda install -c haroldmills vesper`
