# SMS Sender API

## Overview

**SMS Sender API** is a web server built with Python that allows sending SMS messages. The server runs inside a Docker container based on `python:3.9.21-alpine3.21`.

## How It Works

- The script takes a string containing one or multiple phone numbers.  
- If multiple numbers are provided (separated by `;`), the script splits them into a list.  
- It then iterates through each number and sends an individual SMS request.

## Requirements

The application depends on the following Python packages:

- `requests`
- `flask==3.1.0`
- `gunicorn==23.0.0`

These dependencies are automatically installed when building the Docker image.

## Hardware Requirements

To send SMS messages, you need a **GSM dongle** with a **SIM card**.  

The tested and supported dongle is:  
- **Tenda 4G185**

## Docker Image Parameters

The Docker image requires the following environment variables:

- **`ENDPOINT`**: The URL of the GSM dongle (e.g., `http://192.168.0.1`).
- **`ADMINPASS`**: The API password for the GSM dongle.

Make sure to set these variables when running the container.

## Running the Container (basic way)

To use the Docker image, execute the following command:

```sh
docker run -d \
           -p 5000:5000 \
           --name sms-sender \
           -e ENDPOINT="http://192.168.0.1" \
           -e ADMINPASS="password" \
           tibhome/sms-sender-api:main
```
## Running the Container (external config file)
```sh
docker run -d \
           -p 5000:5000 \
           --name sms-sender \
           -v /my/path/config.conf:/config.conf \
           tibhome/sms-sender-api:main
```

## Testing the API

To test API, execute the following command:

```sh
curl --location 'http://127.0.0.1:5000/send' \
     --header 'Content-Type: application/x-www-form-urlencoded' \
     --data-urlencode 'recipient=0612345678' \
     --data-urlencode 'message=This is test'
```

Response success:
```
{"response":"success"}
```

Response failed:
```
{"response":"Error: #ERROR_MESSAGE#"}
```