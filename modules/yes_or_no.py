##########################################
##########################################
##                                      ##
## This is just a module for taking a   ##
## yes or no input from the user.       ##
## No other function, just a yes or     ##
## no :P                                ##
##                                      ##
##########################################
##########################################

def yes_or_no(question): 
    reply = str(input(question + " y/n: ")).lower().strip()
    print("")
    while not(reply == "y" or reply == "yes" or reply == "n" or reply == "no"):
        print("Please input yes or no")
        reply = str(input(question + " y/n: ")).lower().strip()
        print("")
    if reply[0] == 'y': 
        return True
    else: 
        return False
