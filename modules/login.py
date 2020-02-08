##############################################
##############################################
##                                          ##
##  This module is used to get the authen-  ##
##  -cation token, in case the token is not ##
##  found in the temporary file. This just  ##
##  takes the logging credentials as params ##
##  and hits the login API to get the token.##
##                                          ##
##############################################
##############################################


import requests
import json
import sys
import os.path
from os import path
import modules.logstuff as ls

def login_func(main_logger, data):

    logger = main_logger


    # Populating the required variables
    try: 
        login_url = data["login_url"]
        login_data = {
                'platform':data["platform"],
                'email':data["email"],
                'password':data["password"],
                'deviceId':data["deviceId"],
                'isRooted':data["isRooted"],
                'fcm':data["fcm"]
        }
        # Specifying the headers
        ua_headers = {
                "User-Agent": data["user-agent"]
        }
    except KeyError as e: # In case the key does not exists in the JSON file
        logger.error("One of the credentials for login does not exists. Cannot login")
        logger.error(e)
        return None


    ## Populating the headers and params
    r = requests.post(url=login_url, headers=ua_headers, data=login_data)


    ## Reading the response from the server
    try: 
        response_dict = json.loads(r.text)
    except ValueError as e:
        logger.error("Server did not sent proper data")
        logger.error(e)
        return None
    # Checking the response code
    if response_dict["code"] != 200:
        ## If the response is not 200
        logger.error("Sorry, there was an issue processing the request. The server sent the response code: "+str(response_dict["code"]))
        return None
    else:
        ## Writing the authentication token to a temporary file
        auth_file = open("/tmp/auth_file.txt", "w")
        auth_file.write(response_dict["data"]["token"])
        auth_file.close()
        return response_dict["data"]["token"]
        logger.info("The authentication token has been successfully written to file")
# EOF
