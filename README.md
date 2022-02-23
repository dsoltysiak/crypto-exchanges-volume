# Monitoring volume across cryptocurrency exchanges

The project consists of an ETL pipeline to pull the data about cryptocurrency exchanges using the [CoinCap API](https://docs.coincap.io/). The data is then loaded into the data warehouse and visualized on the dashboard created in Metabase. The goal was to show how the volume in the last 24 hours changes in time across the exchanges and see the top 10 ones. Everything is containerized using Docker and is working on the Amazon EC2 instance.

## Architecture
In this project, PostgreSQL serves as a Data Warehouse. In the ETL process, there is python used, and since there are not many scripts to be scheduled, I have decided to use cron instead of setting up a framework like an Airflow. The cron job is scheduled to run every hour.

![architecture](/images/architecture.png)

## Visualization

The results are presented based on the data pulled across the length of one day. The first thing that can be easily observed is a massive gap between the first exchange and the rest. 

![first_dashboard](/images/first_dashboard.png)

Because of the previously mentioned gap, additionally, I would like to present a dashboard without the leader (Binance) to make the interchangeability of positions in the ranking more visible.

![second_dashboard](/images/second_dashboard.png)

## Installation
### Requirements:
1. [Git](https://git-scm.com/)
2. [AWS account](https://aws.amazon.com/)
3. [AWS CLI installed](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) and [configured](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)
4. [EC2 instance](https://aws.amazon.com/ec2/)

The first part is about cloning the repo and running the script to send the code to the instance.
```bash
git clone https://github.com/dsoltysiak/crypto-exchanges-volume
cd cryptomonitor

chmod 755 ./deploy_helpers/send_code_to_prod.sh
chmod 400 pem-file-full-location
./deploy_helpers/send_code_to_prod.sh pem-file-full-location EC2-Public-DNS
```
The next step is to install the docker and docker-compose by using the provided script.

```bash
chmod 755 install_docker.sh
./install_docker.sh

unzip cryptomonitor.gzip && cd cryptomonitor
```

## Usage

To spin up the docker containers use the docker-compose.
```bash
docker-compose --env-file env up --build -d
```
Then, the following command is responsible for running the tests.
```bash
docker exec pipelinerunner pytest /code/test
```
The next step is to log into the remote Metabase instance by using 
http://public-ipv4-address:3000 and set up a connection to the Postgres warehouse.

If one wants to finish, the below command should be used to tear down the containers, and then the EC2 instance should have been stopped or terminated.
```bash
docker-compose down
```

## License
[MIT](https://choosealicense.com/licenses/mit/)