from typing import Optional
from fastapi import FastAPI, Header
from fastapi.logger import logger

import uvicorn
import logging

import extractor


gunicorn_logger = logging.getLogger('gunicorn.error')
logger.handlers = gunicorn_logger.handlers
#logging.basicConfig(level=logging.DEBUG)
if __name__ != "main":
    logger.setLevel(gunicorn_logger.level)
else:
    logger.setLevel(logging.DEBUG)

app = FastAPI()


# a simple page that says hello
@app.get('/')
def hello():
    return 'You reached the GraphExtraction API'

@app.post("/users")
def extractAllUsers(token: Optional[str] = Header(None)) :
    response =  extractor.extract(token,"users")
    return response

@app.post("/users/{usermail}")
def extractUser(usermail, token: Optional[str] = Header(None)):
    response =  extractor.extract(token,"users",usermail.lower())
    return response

@app.post("/users/photo/")
def extractListUserPhoto(listuser: Optional[str] = Header(None), token: Optional[str] = Header(None)):
    response =  extractor.extractUserPhoto(token,"users",listuser.lower(),"list")
    return response

@app.post("/users/photo/{usermail}")
def extractUserPhoto(usermail, token: Optional[str] = Header(None)):
    response =  extractor.extractUserPhoto(token,"users",usermail.lower())
    return response

@app.post("/users/start/{filter}")
def extractUserStartWith(filter, token: Optional[str] = Header(None)):
    response =  extractor.extract(token,"users",filter=filter)
    return response

@app.post("/users/member/")
def extractListUserMember(listuser: Optional[str] = Header(None), token: Optional[str] = Header(None)):
    response =  extractor.extractUserMember(token,"users",listuser.lower(),"list")
    return response

@app.post("/users/member/{usermail}")
def extractUserMember(usermail, token: Optional[str] = Header(None)):
    response =  extractor.extractUserMember(token,"users",usermail.lower())
    return response

@app.post("/groups")
def extractAllGroups(token: Optional[str] = Header(None)):
    response =  extractor.extract(token,"groups")
    return response

@app.post("/groups/{groupid}")
def extractGroup(groupid, token: Optional[str] = Header(None)):
    response = extractor.extract(token,"groups",groupid)
    return response



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)