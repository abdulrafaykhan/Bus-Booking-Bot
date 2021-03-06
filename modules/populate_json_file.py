##########################################
##########################################
##                                      ##
## This file populates the some.json    ##
## files which contains the credentials ##
## such as username, password, the API  ##
## endpoints. This will half be auto-   ##
## -matic and half will require intera- ##
## -ction from the user                 ##
##                                      ##
##                                      ##
##########################################
##########################################

import json
import requests
import modules.yes_or_no as yon
import re # To check for valid format of email


def check_email(email):

    email_regex = "^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"

    if(re.search(email_regex, email)): 
        return True
    else:
        return False


def populate_json_file(logger):

    # Importing the logger
    logger = logger

    airlift_email = input("Please enter your Airlift email address: ")
    
    while check_email(airlift_email) != True:
        logger.error("Email format is invalid!")
        print("Please enter the email in the correct format\n\n")
        airlift_email = input("Please enter your Airlift email address: ")

    airlift_password = input("Please enter your Airlift password: ")
    email_reply = yon.yes_or_no("Do you want to enter email credentials? NOTE: THESE WILL BE USED TO EMAIL EXECUTION LOGS TO YOU")
    if email_reply == True: 
        email_username = input("Please enter email address from which to send the email address: ")
        while check_email(email_username) != True:
            print("Please enter the email in the correct format\n\n")
            email_username = input("Please enter email address from which to send the email address: ")

        email_password = input("Please enter email password: ")
        email_send_to = input("Please enter the email address which you want to send the email: ")
        while check_email(email_send_to) != True: 
            print("Please enter the email in the correct format\n\n")
            email_send_to = input("Please enter the email address which you want to send the email: ")

    r = requests.get("https://raw.githubusercontent.com/abdulrafaykhan/Bus-Booking-Bot/master/template.json")
    response = r.json()
    response["email"] = airlift_email
    response["password"] = airlift_password
    if email_reply == True:
        response["send_email_username"] = email_username
        response["send_email_password"] = email_password
        response["send_email_to"] = email_send_to
    f = open("some.json", "w")
    f.write(json.dumps(response))
    f.close()
    return None
