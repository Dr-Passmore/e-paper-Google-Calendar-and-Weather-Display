# e-paper-Google-Calendar-and-Weather-Display

## Hardware Requirements

* Raspberry Pi (I recommend a Pi Zero)
* E-Paper screen
* Picture frame suitable for the screen

## Dependencies

### Install the required python dependencies

Use the requirements.txt file to install the required python dependencies

### Install the rquired libraries

In the terminal run the following commands:

wget <http://www.airspayce.com/mikem/bcm2835/bcm2835-1.60.tar.gz>\
tar zxvf bcm2835-1.60.tar.gz\
cd bcm2835-1.60/\
sudo ./configure\
sudo make\
sudo make check\
sudo make install\
sudo apt-get install wiringpi\
wget <https://project-downloads.drogon.net/wiringpi-latest.deb>\
sudo dpkg -i wiringpi-latest.deb\
sudo apt-get update\
sudo pip install RPi.GPIO\
cd\
wget <https://github.com/waveshare/e-Paper/archive/refs/heads/master.tar.gz>\
tar zxvf master.tar.gz\
cd e-Paper-master/RaspberryPi_JetsonNano/python/examples

Run the example file that matches your e-ink screen
