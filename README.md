# Simple SSL/TLS client certificate verification 


## Apt to install

You will need the following package:
    
    sudo apt install python3
    sudo apt install virtualenv
    sudo apt install python3-pip

## Python env preparation

Prepare your virtualenv:

    virtualenv -p python3 venv
    . venv/bin/activate

If you want to exit your virtualenv:

    deactivate

## Run app

Create server certificate:

    openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout server.key -out server.crt

Make sure to enter ‘example.com’ for the Common Name.

Then generate a client certificate:

    openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout client.key -out client.crt

Then run the server python script

    python tsl_server.py

And the client

    python tsl_client.py
