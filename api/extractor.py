import requests
import json
import os
from datetime import datetime
from urllib.parse import urlparse
import logging
from fastapi import logger, HTTPException


formatter = logging.Formatter('[%(asctime)s] %(levelname)-8s %(message)s')


def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# first file logger
logtFolder = f'output/log'
# creating log folder if itdoesn't exit
if not os.path.exists(logtFolder):
    os.makedirs(logtFolder)
logger = setup_logger('first_logger', f'{logtFolder}/app.log')

def extract(token,object,entity="",filter=""):

    

    start=datetime.now()
    payload = {}
    headers = {'Authorization': f'Bearer {token}'}
    baseUrl = "https://graph.microsoft.com"
    apiVersion = "beta"
    objectRequested = object
    objectValue = entity


    
    if filter != "":
        #Fetching startWith entities
        logger.info(f'STARTING: Extract {object} that start with: "{filter}"')
        url = f'{baseUrl}/{apiVersion}/{objectRequested}?$filter=startswith(displayName,\'{filter}\')'
        filePrefix = f'_{filter}'

    if entity != "":
        #Fetching specific entity
        logger.info(f'STARTING: Extract {object} with id: "{entity}"')
        filePrefix = f'_{objectValue}'
        url = f'{baseUrl}/{apiVersion}/{objectRequested}/{objectValue}'
    else:
    #Fetching ALL entities
        logger.info(f'STARTING: Extract all {object}')
        filePrefix = ""
        url = f'{baseUrl}/{apiVersion}/{objectRequested}'

    # creating output folder if it doesn't exist
    outputFolder = f'output/raw/api={apiVersion}/object={objectRequested}/year={start.year}/month={start.month}/day={start.day}'
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)

    i=0
    while url:
        url = get_data(f'{url}', payload, headers,f'{outputFolder}/{start.strftime("%Y%m%d_%H%M%S")}_{i}{filePrefix}.json')
        i+=1
    logger.info(f'FOLDER: {outputFolder}\n'
                f'{35 * " "}PATTERN: {start.strftime("%Y%m%d_%H%M%S")}_xxxx{filePrefix}.json\n'
                f'{35 * " "}SUCESSFULL: after {i} iterations in {datetime.now()-start}H'
                )
    #logger.info(f'files written with pattern: {start.strftime("%Y%m%d_%H%M%S")}_xxxx{filePrefix}.json')  
    #logger.info(f'operation finished after {i} iterations in {datetime.now()-start}H')
    return True

def get_data(url, payload, headers,filename):
    response = requests.request("GET", url, headers=headers, data=payload )
    data = response.text.encode('utf8')
    obj = json.loads(data) 
    
   # error received from the MS graphAPI
    if 'error' in obj:
        logger.error(f"{obj['error']['code']} - {obj['error']['message']}")
        logger.error(f"last url called: {url}")
        return False
        #raise HTTPException(status_code=500, detail=f"{obj['error']['code']} - {obj['error']['message']}")
    
 
    with open(filename, 'w') as outfile:
        outfile.write(data.decode("utf-8"))
        logger.debug(f'file written in: {filename}')
       
    # there is a new page to fetch on the specific request, return the url of it   
    if '@odata.nextLink' in obj:     
        return obj['@odata.nextLink']
    
    return False

def get_file(url, payload, headers,filename):
    response = requests.request("GET", url, headers=headers )
    if response.status_code!=200:
        return False

    with open(filename, "wb") as f:
        f.write(response.content)
    
    return True


def extractUserPhoto(token,object,entity="",typeExtract=""):
    start=datetime.now()
    payload = {}
    headers = {'Authorization': f'Bearer {token}'}
    baseUrl = "https://graph.microsoft.com"
    apiVersion = "beta"
    objectRequested = object

    outputFolder = f'output/raw/api={apiVersion}/object={objectRequested}_photo/year={start.year}/month={start.month}/day={start.day}'
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)

    logger.info(f'STARTING: Extract photo')

    if typeExtract=="list":
        jsonEmailList = json.loads(entity)
        i=0
        for email in jsonEmailList:
            url = f'{baseUrl}/{apiVersion}/{objectRequested}/{email}/photo/$value'
            get_file(url, payload, headers,f'{outputFolder}/{email}.jpeg')
            i=i+1
    else:
        url = f'{baseUrl}/{apiVersion}/{objectRequested}/{entity}/photo/$value'
        get_file(url, payload, headers,f'{outputFolder}/{entity}.jpeg')
        i=1
    
    logger.info(f'FOLDER: {outputFolder}\n'
                f'{35 * " "}SUCESSFULL: after {i} iterations in {datetime.now()-start}H'
                )

    return True



def extractUserMember(token,object,entity="",typeExtract=""):
    start=datetime.now()
    payload = {}
    headers = {'Authorization': f'Bearer {token}'}
    baseUrl = "https://graph.microsoft.com"
    apiVersion = "beta"
    objectRequested = object

    outputFolder = f'output/raw/api={apiVersion}/object={objectRequested}_member/year={start.year}/month={start.month}/day={start.day}'
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)

    logger.info(f'STARTING: Extract user member')

    if typeExtract=="list":
        jsonEmailList = json.loads(entity)
        i=0
        for email in jsonEmailList:
            #/transitiveMemberOf/microsoft.graph.group?$count=true
            url = f'{baseUrl}/{apiVersion}/{objectRequested}/{email}/transitiveMemberOf/microsoft.graph.group?$count=true'
            j=0
            while url:
                url = get_data(f'{url}', payload, headers,f'{outputFolder}/{start.strftime("%Y%m%d_%H%M%S")}_{email}_{j}.json')
                j=j+1

            i=i+1
    else:
        url = f'{baseUrl}/{apiVersion}/{objectRequested}/{entity}/transitiveMemberOf/microsoft.graph.group?$count=true'
        j=0
        while url:
            url = get_data(f'{url}', payload, headers,f'{outputFolder}/{start.strftime("%Y%m%d_%H%M%S")}_{entity}_{j}.json')
            j=j+1
        i=1
    
    logger.info(f'FOLDER: {outputFolder}\n'
                f'{35 * " "}SUCESSFULL: after {i} iterations in {datetime.now()-start}H'
                )

    return True