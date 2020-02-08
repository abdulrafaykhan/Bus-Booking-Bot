##############################################
##############################################
##                                          ##
## This module is used for checking the     ##
## remaining balance. It just takes the     ##
## authentication token and then hits       ##
## check_balance API for getting the        ##
## remaining credit in the account          ##
##                                          ##
##############################################
##############################################


import json
import requests

def check_balance(logger, auth_token, data):

    
    logger = logger


    # Populating the required headers and params
    try: 
        url = data["check_balance_url"]
        user_agent = data["user-agent"]
        params = {

            # I dont know what this parameter does
            # Or why it is required
            # I think though it has to do with the
            # version of the application 
            # TODO: Check requesting without this parameter
            "version": data["version"]
        }
    except KeyError as e: # In case the required key does not exist in the JSON file
        logger.error("One of the credentials for checking balance does not exists in the JSON file. Balance cannot be checked.")
        logger.error(e)
        return None
    auth_headers = {
            "User-Agent": user_agent,
            "auth": auth_token
    }


    # Sending the GET request
    r = requests.get(url=url, headers=auth_headers, params=params)


    # Getting the balance
    try: 
        response_dict = json.loads(r.text)
    except ValueError as e: # In case the server did not send the expected response
        logger.error("Server did not send proper response")
        logger.error(e)
        return None
    if response_dict["code"] != 200:
        logger.error("Sorry, there was an issue processing the request. The server sent the response code: "+str(response_dict["code"]))
        return None
    rem_balance = response_dict["data"]["credits"]
    

    # Printing the remaining balance
    logger.info("Your current balance is: "+str(rem_balance))


    return rem_balance

