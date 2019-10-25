#!/usr/bin/env bash
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
# pip install http://download.pytorch.org/whl/cu90/torch-0.4.1-cp27-cp27mu-linux_x86_64.whl 
pip install pytorch torchvision
pip install -U scikit-learn
mkdir libs
cd libs
git clone https://github.com/dlitz/pycrypto.git
cd pycrypto
python setup.py build
python setup.py install
cd ..
git clone git://github.com/signal11/hidapi.git
cd hidapi
./bootstrap
./configure
sudo make
sudo make install
cd ..
git clone https://gitlab.com/NF6X_Archive/pyhidapi.git
cd pyhidapi
./setup.py install
sudo ./setup.py sdist
cd ..
cd ..
deactivate
