# This is needed to install the drivers below as well as print from the mongodb database
sudo apt-get install python-imaging python-serial python-setuptools # printer and python tools
sudo apt-get install build-essential python-dev # compilation tools for c++ and python
sudo python -m pip install pymongo # the ORM used to retrieve information and print it

# this is needed for the PyUSB driver
wget https://sourceforge.net/projects/pyusb/files/PyUSB%201.0/1.0.0/pyusb-1.0.0.zip #location of the driver
unzip pyusb*.zip #need to unzip the driver
cd pyusb* # change into driver directory
python setup.py build # build the driver
sudo python setup.py install # install the driver

# this is needed for barcode printing
git clone https://github.com/lincolnloop/python-qrcode # clone the barcode printer repo
cd python-qrcode # change into the python-qrcode directory
python setup.py build # build the driver
sudo python setup.py install # install the driver

# this is the final driver needed to print. This ties everything together 
git clone https://github.com/manpaz/python-escpos.git # clone the repo
cd python-escpos # change into the driver directory
python setup.py build # build the driver
sudo python setup.py install # install the driver
