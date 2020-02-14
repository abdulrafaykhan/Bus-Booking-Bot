##############################################
##############################################
##                                          ##
## This is the main function. This is where ##
## all the fun happens. This is the module  ##
## which will initiate the execution of the ##
## of the program                           ##
##                                          ##
##############################################
##############################################


import json
import sys
import os.path
from os import path
import modules.logstuff as ls
import modules.send_email as se
import modules.login as ln
import modules.get_dates as gd
import modules.check_balance as cb
import modules.get_booking_status as gbs
import modules.confirm_book as cob
import modules.get_trip_info as gti
import modules.bring_trips as bt
import modules.populate_json_file as pjf

 
def main():


    ## Setting the logger parameters
    logger = ls.get_logger()


    # Checking for the existence of the JSON file
    status = path.exists("some.json")
    if status != True:
        # Incase the file with the credentials does not exists
        logger.error("File with the authentication credentials does not exists. Creating...")
        pjf.populate_json_file(logger)

    ## Reading the login credentials from the JSON file
    with open("some.json") as json_file:
        try: 
            data = json.load(json_file)
        except Exception as e: 
            logger.error("There was an issue parsing the JSON from the data file. Maybe there is an issue in the format of the JSON. Please check the file. Thanks!")
            logger.error(e)
            sys.exit(1)


    # Populating the authentication token
    auth_token = ""
    if not auth_token:
        status = path.exists("/tmp/auth_file.txt")
        if status != True:
            # Incase the file with the authentication token does not exists
            logger.info("File with the authentication token does not exists. Getting the token from POST request")
            auth_token = ln.login_func(logger, data)
        else:
            # File with the authentication does exists
            logger.info("File with the authentication token does exists. Getting the token from file")
            token_file = open("/tmp/auth_file.txt", "r")
            auth_token = token_file.read()
            token_file.close()


    # Getting and printing the dates for the bookings
    booking_dates = gd.get_dates(logger)
    logger.info("The following dates are on which the booking will be done")
    logger.info(booking_dates)
    # Checking the remaining balance
    rem_balance = cb.check_balance(logger, auth_token, data)

    if not data["send_email_username"] or not data["send_email_password"] or not data["send_email_to"]:
        logger.info("The email credentials were not provided. No email will be sent")
    else:
        try:
            if rem_balance <= 500:
                # If the balance is less than Rs. 500
                logger.error("Sorry, your remaining balance is insufficient for the booking")
                logger.error("Sending the low balance warning email...")
                se.send_emails(logger, True, rem_balance, data)
        except NameError as e:
            logger.error("There was some issue getting the remaining balance")
            return None
        try: 
            if rem_balance <= 200:
                # If the balance is less than Rs. 200
                logger.error("Sorry, your remaining balance is insufficient for the booking")
                logger.error("Sending the low balance warning email...")
                se.send_emails(logger, True, rem_balance, data)
        except NameError as e:
            logger.error("There was some issue getting the remaining balance")
            return None


    # Initiate the booking process
    logger.info("Starting the booking process...")
    for date in booking_dates:
        logger.info("Booking for the date: " + str(date))
        # For Morning Booking (True is for morning == True)
        bt.bring_nearby_trips(logger, auth_token, date, data, True)
        # For Evening Booking 
        bt.bring_nearby_trips(logger, auth_token, date, data, False)


    # Send the email to email the logs
    if not data["send_email_username"] or not data["send_email_password"] or not data["send_email_to"]: 
        logger.info("The email credentials were not provided. No email will be sent")
    else: 
        logger.info("Sending the final email...")
        se.send_emails(logger, False, rem_balance, data)


    # Close the JSON file handler
    json_file.close()


    return None

# Calling the main function
if __name__ == '__main__':

    main()
