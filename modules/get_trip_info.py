##############################################
##############################################
##                                          ##
## This module is used to get trip info     ##
## for trip that is to be booked. This is   ##
## necessary for getting the booking price  ##
## of the trip, which will later be used    ##
## to be compared with the remaining balan- ##
## -ce.                                     ##
## We have already handled the low balance  ##
## remaining in the main function. Just     ## 
## this is for checking the balance again.  ##
##                                          ##
##############################################
##############################################


import modules.logstuff
import requests
import json


def bring_trip_info(logger, trip_id, pickupstop_id, dropoffstop_id, auth_token, data):


    logger = logger


    # Populating the required parameters
    try: 
        url = data["bring_trip_info_url"]
        auth_headers = {
            "User-Agent": data["user-agent"],
            "auth": auth_token
        }
        booking_trip_data = {
                "tripId": trip_id, 
                "pickUpStopId": pickupstop_id, 
                "dropOffStopId": dropoffstop_id, 
                # This variable
                # Dont know what it does
                # or why its required
                # Maybe it has to do something 
                # with the return booking
                "isDirection": data["isDirection"]
        }
    except KeyError as e: # In case the key does not exists in the JSON file
        logger.error("One of the credentials required for bringing the trip information does not exists. Exiting...")
        logger.error(e)
        return None


    # If all is well, send the GET request 
    r = requests.get(url=url, headers=auth_headers, params=booking_trip_data)


    # Parsing the response from the server
    try: 
        response_dict = json.loads(r.text)
    except ValueError as e:
        logger.error("Server did not sent a proper response")
        logger.error(e)
    if response_dict["code"] != 204 or response_dict["success"] != True:
        # In case something is wrong with sending the request
        logger.error("Sorry, there was an issue processing the request. The server sent the response code: "+str(response_dict["code"]))
        return None
    trip_id = response_dict["data"]["tripId"]
    booking_price = response_dict["data"]["bookingPrice"]


    return None
# EOF

