##############################################
##############################################
##                                          ##
## This module is just used to generate the ##
## required dates, as well as checking for  ##
## any day (such as Saturday or Sunday) on  ##
## which the booking is not to be held.     ##
##                                          ##
##############################################
##############################################


import modules.logstuff as ls
import datetime

def get_dates(logger):


    logger = logger


    # Getting the date of booking
    today_date = datetime.date.today()
    tomm_date = today_date + datetime.timedelta(days=1)
    dat_date = today_date + datetime.timedelta(days=2)


    # Getting the corresponding days and adding them to a list
    days = {}
    days[today_date.strftime("%A")] = today_date.strftime('%Y-%m-%d')
    days[tomm_date.strftime("%A")] = tomm_date.strftime('%Y-%m-%d')
    days[dat_date.strftime("%A")] = dat_date.strftime('%Y-%m-%d')


    # Logging
    logger.info("These are the selected days for the booking...")
    logger.info(days)
    booking_dates = []


    # Populating the list
    # for the booking dates
    # Printing for logging purposes
    for day in days:
        if day == "Saturday" or day == "Sunday":
            logger.error("Uh oh! This day is an off day. No booking will be done")
            continue
        booking_dates.append(days[day])


    # Finally returning the calculated dates
    return booking_dates
# EOF
