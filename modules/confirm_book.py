##############################################
##############################################
##                                          ##
## This module will send the request to     ##
## book the ride and then will call the     ##
## function to check the status of the      ##
## booked ride. Just the flow of the API    ##
##                                          ##
##############################################
##############################################

import requests
import json
import modules.logstuff as ls
import modules.get_booking_status as gbs

def confirm_book(logger, dropoffstop_id, pickupstop_id, customertrip_id, auth_token, data):


    logger = logger


    # Populating the variables from the provided params
    try: 
        url = data["confirm_book_url"]
        auth_headers = {
            "User-Agent": data["user-agent"],
            "auth": auth_token
        }
        server_data = {
            "platform": data["platform"], 
            "promo": "", 
            "dropOffStopId": dropoffstop_id, 
            "pickUpStopId": pickupstop_id, 
            "customerTripId": customertrip_id, 
            "newUI": data["newui"]
        }
    except KeyError as e:
        logger.error("One of the credentials for confirming the booking status does not exists. Booking cannot be confirmed")
        logger.error(e)
        return None
    

    # Sending the POST request
    r = requests.post(url=url, headers=auth_headers, data=server_data)

    
    try: 
        response_dict = json.loads(r.text)
    except ValueError as e: # In case the server did not send the expected data
        logger.error("Server did not responded with proper data")
        logger.error(e)


    try: 
        if response_dict["code"] != 201 or response_dict["success"] != True:
            logger.error("Sorry, there was an issue processing the request. The server sent the response code: "+str(response_dict["code"]))
        booking_id = response_dict["data"]["booking_request_id"]
    except KeyError as e: # In case the required key doesnt exists in the response
        logger.error("The required keys do not exist in the response from the server for confirming the booking status")
        logger.error(e)
        return None


    # Finally calling the function    
    # to check the status of the booking
    gbs.check_booking_status(logger, booking_id, auth_token, data)


    return None
# EOF

