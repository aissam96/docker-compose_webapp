# docker-compose_webapp

### Definition

This web app serves a simple hello world page protected with basic http authentification, and it saves the access logs to a mongoDB database everytime someone accesses the webpage. If a user has entered a wrong password for more than 10 times, an automated script sends an alert email showing his username and the number of the wrong attempts.

The app runs on 4 docker containers:
web_app: based on an nginx image and its purpose is to serve the web page
attempts_counter: runs a python script every 20 minutes. This script counts the failed logins and sends an email if a user has reached 10 times.
logs_to_mongoDB: runs a python script to store the access logs in a collection in mongodb.
mongo: runs the mongo daemon. 

### Configuration

The password is stored in htpasswd file. "the default username and password are admin:admin"
The sender & receiver email addresses are configured in attempts_counter > script.py

### Running

To run the app, open the folder in terminal, and run:
```sh
$ docker-compose build
```

```sh
$ docker-compose up
```