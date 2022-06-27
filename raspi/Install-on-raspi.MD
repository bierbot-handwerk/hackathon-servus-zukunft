# Installation on Raspberry Pie (Fresh Raspi 4)

```bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install -y git python3-venv python3-dev python3-w1thermsensor
git clone https://github.com/codepals-org/hackathon-servus-zukunft.git
python3 -m venv .venv
source .venv/bin/activate
```

# Credentials needed to run the Python script

Create a file .env and place your MongoDB credentials there...

    MONGODB_URI=mongodb+srv://<user>:<password>@<host>/?retryWrites=true&w=majority

Never put your credentials in a public repository, so keep this .env out of your repo.

# Install RPi.GPIO 

```bash
wget https://pypi.python.org/packages/source/R/RPi.GPIO/RPi.GPIO-0.5.11.tar.gz
tar -xvf RPi.GPIO-0.5.11.tar.gz
cd RPi.GPIO-0.5.11
sudo python setup.py install
```

# Install Adafruit (Temperature & Humidity)

In some other folder...
```bash
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT/

# still with venv activated
python setup.py install
```
then go back to your normal project folder


