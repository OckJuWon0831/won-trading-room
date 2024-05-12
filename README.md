# WON! Trading Room

![architecture](https://github.com/OckJuWon0831/won-trading-room/assets/114837587/110f6692-c723-47ab-9bda-a9752d83a80b)

## Final Year Project

Comparison of the CNN-LSTM deep learning model(Combined model of CNN and LSTM) and ARIMA(Autoregressive Integrated Moving Average) prediction model on stock market data.

The data of FAANG(Facebook, Amazon, Apple, Netflix and Google) was crawled from Yahoo Finance API for approximately 15 years, and the models were trained and tested based on the obtained data.

🔗 http://18.139.100.114:8501/

🔎 [Wiki - Won Trading Room](https://github.com/OckJuWon0831/won-trading-room/wiki)

# How to set up
> ‼️ This application is developed in the Linux operating system.
> 
> ‼️ Using a Virtual Machine or AWS instance is recommended for Windows users

## If you are Windows user...
> ‼️ It is for the Windows 10 or 11 users
### Setting up the Linux subsystem on the Windows environment
1. Enter these commands on the Windows terminal
- `dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart`
- `dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart`
2. Install Ubuntu in the local environment
3. Reset your laptop and launch the Ubuntu application to finish the installation
4. Set your profiles and update & upgrade.
- `sudo apt-get update` & `sudo apt-get upgrade`


## Installing Docker
1. `sudo apt-get update`
2. `sudo apt-get install apt-transport-https ca-certificates curl software-properties-common`
3. `curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -`
4. `sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"`
5. `sudo apt update`
6. `sudo apt install docker-ce`
- If the Docker is successfully installed then the version will be appeared.
7. `docker --version`

## Installing Docker-compose
1. ``sudo curl -L https://github.com/docker/compose/releases/download/v2.1.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose``
2. `sudo chmod +x /usr/local/bin/docker-compose`
3. `sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose`
- If the Docker-compose is successfully installed then the version will be shown.
4. `docker-compose --version`

# How to run
1. `git clone https://github.com/OckJuWon0831/won-trading-room`
2. Make `.env` file for the MySQL DB connection in the directory
  - `MYSQL_ROOT_PASSWORD="YOUR_PASSWORD"`
  - `MYSQL_DATABASE="stock_db"`
3. `sh init.sh` to initiate the containers and load data
- `docker-compose up --build -d` will be executed
# Usage

Connect the application: `https://<domain-ip>:8501/`

- localhost: `https://localhost:8501/`

Stop the application: `docker-compose stop`
Execute the application: `docker-compose start`

Remove the application: `docker-compose down`

- if you want to remove the whole data and run from the basic: `docker-compose down -v`

## Version

### Version 1.0.0

### BSc (Hons) Computer Science with Artificial Intelligence

### Ock Ju Won
