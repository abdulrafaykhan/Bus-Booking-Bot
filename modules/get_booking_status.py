##################################################
##################################################
##                                              ##
## This module will be used to check the status ##
## of the most recent booking. The API flow is  ##
## such that it requires a seperate request for ##
## getting the status of the last booking. Thus ##
## this module will just send a request to API  ##
## and print the status of the booking in the   ##
## log.                                         ##
##                                              ##
##################################################
##################################################


import requests
import modules.logstuff as ls
import json


def check_booking_status(logger, booking_id, auth_token, data):


    logger = logger


    # Populating the required parameters and header
    try: 
        url = data["get_booking_status_url"] + str(booking_id)
        auth_headers = {
            "User-Agent": data["user-agent"],
            "auth": auth_token
        }
    except KeyError as e: # In case the required key is not found in the JSON file
        logger.error("The URL for the checking the bookign status does not exists")
        logger.error(e)
        return None

    
    # Otherwise, if all is well, send the request
    r = requests.get(url=url, headers=auth_headers)


    try: 
        response_dict = json.loads(r.text)
    except ValueError as e: # In case the server did not send the expected response
        logger.error("Server did not send a proper response")
        logger.error(e)

  
    if response_dict["code"] != 200:
    ## If the response is not 200
        logger.error("Sorry, there was an issue processing the request. The server sent the response code: "+str(response_dict["code"]))
        return None


    # Checking the response for the booking status
    booking_status = response_dict["data"]["status"]
    if booking_status == "REJECTED": 
        logger.error("Sorry, your booking cannot be done right now. The server rejected the booking")
    booking_message = response_dict["data"]["message"]
    logger.info("The booking process has completed")
    logger.info(str(booking_status))
    logger.info(str(booking_message))
    # End of printing booking status block


    return None
