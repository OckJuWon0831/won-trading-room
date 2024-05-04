# WON! Trading Room

## Final Year Project

BSc (Hons) Computer Science with Artificial Intelligence

Ock Ju Won

Address: http://18.139.100.114:8501/

# How to run

1. Make `.env` file for the MySQL DB connection
2. Docker-compose and Docker must be installed in the local environment
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
