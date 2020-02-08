##############################################
##############################################
##                                          ##
## This module is used for configuring the  ##
## logger that will be used to log the      ##
## entries throughout the execution of the  ##
## program.                                 ##
##                                          ##
##############################################
##############################################


import logging

def get_logger():
    
    ## Create logger with the module name
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    
    ## Create file handler which logs even debug messages
    fh = logging.FileHandler("/var/log/booking-airlifts.txt")
    fh.setLevel(logging.DEBUG)

    ## Create a console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    ## Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    ## Adding the handler to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger
