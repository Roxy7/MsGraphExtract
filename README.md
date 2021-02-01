# Introduction 

This project have been created in the context that you can't create/register an app in your Azure Active Directory organisation so you are not able to create app keys to authenticate a script to the MS Graph API. Hopfully there is still a way to extract lots of interresting data. Thank's to the graph-explorer webpage you are able to get a token to authenticate yourself!

More information and context here: https://xp-it.com/python-january/

references: https://developer.microsoft.com/fr-fr/graph/graph-explorer

## what this code does ?

When calling the api endpoint, the script will loop over the MS Graph api to extract all data (including pagination) and store it in a dedicated "output" folder. You wont get any data back from the api. It "just" store all the differents files on a "datalake".

--> withe docker, output folder is used as a volume to get the data back

## Requirement

Work with Python 3.8

To get you token, you must go and connect to https://developer.microsoft.com/fr-fr/graph/graph-explorer and copy/past your token. --> The token is only valid for 1h !

# Installation

## Docker

The easiest way is to use the Dockerized version of the app.

### Creating Docker container

    docker build -t graph-extract:0.1 .
    docker run -p 80:80 -v "$(pwd)/output:/app/output" --name Graph graph-extract:0.1

### Docker compose usage

    docker-compose up

## Outside Docker

If you want to run the api outside the docker container:

First install the python dependencies
    
    pip install -r requirements.txt

then navigate to api folder and launch uvicorn

    cd api
    uvicorn main:app --port 80

# Usage

For the app to work, you need to call the api passing your graph token in the header of each call.

key:*token*     |   value:*yourtokenhere*

## Endpoints

Best way to get all the available endpoint si to reach the swagger page:

* http://{urloftheapi}:1077/docs

Actuall endpoints:

* http://{urloftheapi}:1077/users --> extract ALL users
* http://{urloftheapi}:1077/users/{usemail} --> extract the specific user
* http://{urloftheapi}:1077/start/{startingcharacters} --> extract ALL users where their displayName start with {startingcharacters}
* http://{urloftheapi}:1077/groups --> extract ALL groups
* http://{urloftheapi}:1077/groups/{groupid} --> extract the specific group

