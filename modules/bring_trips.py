###############################################
###############################################
##                                           ## 
##  This module will fetch the nearby trips  ##
##  based on the longitude, latitude and the ##
##  time of the booking.                     ##
##  It will test the booking time against a  ##
##  regex for both the morning and evening   ##
##  times.                                   ##
##                                           ##
###############################################
###############################################

import modules.logstuff as ls
import requests
import re
import json
import modules.get_trip_info as gti
import modules.confirm_book as cb

def bring_nearby_trips(logger, auth_token, date, data, morning):


    logger = logger


    # Populating the required headers, params and data
    try: 
        url = data["bring_nearby_trips_url"]
        auth_headers = {
            "User-Agent": data["user-agent"], 
            "auth": auth_token
        }
        # Need to import all since
        # both are needed to check
        # against condition
        m_pickup = data["m_pickup"]
        m_dropoff = data["m_dropoff"]
        e_pickup = data["e_pickup"]
        e_dropoff = data["e_dropoff"]
        if morning == True: 
            pickup_lng = data["m_pickuplng"]
            dropoff_lng = data["m_dropofflng"]
            pickup_lat = data["m_pickuplat"]
            dropoff_lat = data["m_dropofflat"]
        else: 
            pickup_lng = data["e_pickuplng"]
            dropoff_lng = data["e_dropofflng"]
            pickup_lat = data["e_pickuplat"]
            dropoff_lat = data["e_dropofflat"]
    except KeyError as e:
        logger.error("Cannot bring the nearby trips")
        logger.error(e)
        return None
    trip_data = {
            "date": date, 
            "pickUpLng": pickup_lng, 
            "dropOffLng": dropoff_lng, 
            "pickUpLat": pickup_lat, 
            "dropOffLat": dropoff_lat
    }


    # Sending the post request
    r = requests.post(url=url, headers=auth_headers, data=trip_data)


    try: 
        response_dict = json.loads(r.text)
    except ValueError as e: # In case the data was not sent from the server
        logger.error("Server did not responded with data")
        logger.error(e)
        return None 
    if response_dict["code"] != 200:
        # In case something is wrong with sending the request
        logger.error("Sorry, there was an issue processing the request. The server sent the response code: "+str(response_dict["code"]))
        return None
    # If the response is 200 but no data is returned
    # Added this in case there is no booking for a specified date
    # As on 5th February (Kashmir Day)
    if response_dict["code"] == 200 and not response_dict["data"]: 
        logger.error("Sorry, there was no data received from the server")
        return None


    # Generating the regexes to be compared with the time
    logger.debug("Generating the regex for the booking time...")
    morn_regex = re.compile("08:0.*")
    even_regex = re.compile("18:3.*")
    logger.debug("Regex Generated Successfully!!")
    # Regex successfully generated 


    # Looping through the available trips
    for pickup_point in response_dict["data"]: 
        pickup = pickup_point["pickUp"]["stop_name"]
        dropoff = pickup_point["dropOff"]["stop_name"]
        timing = pickup_point["pickUp"]["time"]
        # Comparing the time with the regex
        if morning == True:
            status = morn_regex.fullmatch(timing)
        else: 
            status = even_regex.fullmatch(timing)



# This block will be triggered for
# Morning Shift
        if pickup == m_pickup and dropoff == m_dropoff and status:
            
            # Now check whether the bus has seats
            if pickup_point["customerTrip"]["bus"]["capacity"] >= int(1): 
                trip_id = pickup_point["customerTrip"]["id"]
                pickupstop_id = pickup_point["pickUp"]["stop_id"]
                dropoffstop_id = pickup_point["dropOff"]["stop_id"]

                # Printing these just as a way of debug logging
                logger.info("Printing the Morning Shift Parameters")
                logger.info("The trip ID for this trip is: "+str(trip_id))
                logger.info("The pickup stop ID for this trip is: "+str(pickupstop_id))
                logger.info("The drop off stop ID for this trip is: "+str(dropoffstop_id))
                logger.info("The pickup stop name for this trip is: "+str(pickup_point["pickUp"]["stop_name"]))
                logger.info("The pick up timing for this shift is: "+str(pickup_point["pickUp"]["time"]))
                # End of debug logging block
            else:
                # The bus does not has seats :((
                logger.error("Sorry, the bus capacity is full")
                break


# This block will be triggered for
# Evening Shift
        elif pickup == e_pickup and dropoff == e_dropoff and status:

            # check if the bus has seats lol
            if pickup_point["customerTrip"]["bus"]["capacity"] >= int(1): 
                trip_id = pickup_point["customerTrip"]["id"]
                pickupstop_id = pickup_point["pickUp"]["stop_id"]
                dropoffstop_id = pickup_point["dropOff"]["stop_id"]

                # Printing these just as a way of debug logging
                logger.info("Printing the Morning Shift Parameters")
                logger.info("The trip ID for this trip is: "+str(trip_id))
                logger.info("The pickup stop ID for this trip is: "+str(pickupstop_id))
                logger.info("The drop off stop ID for this trip is: "+str(dropoffstop_id))
                logger.info("The pickup stop name for this trip is: "+str(pickup_point["pickUp"]["stop_name"]))
                logger.info("The pick up timing for this shift is: "+str(pickup_point["pickUp"]["time"]))
                # End of debug logging block
            else:
                # The bus does not has seats :((
                logger.error("Sorry, the bus capacity is full")
                break
        else:
            continue


# Finally calling the bring_trip_info function
# for bringing the parameters of the selected trip
    try:
        gti.bring_trip_info(logger, trip_id, pickupstop_id, dropoffstop_id, auth_token, data)
        cb.confirm_book(logger, dropoffstop_id, pickupstop_id, trip_id, auth_token, data)
    except UnboundLocalError as e: 
        logger.error("One of the booking variables were not populated successfully. This could be due to no data being sent in the response from the server ")
        logger.error(str(e))
        logger.info("Moving on with the bookings...")


    return None
