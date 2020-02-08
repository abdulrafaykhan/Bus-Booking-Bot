##############################################
##############################################
##                                          ##
## This module is used to send the email    ##
## which will contain the logs of the exe-  ##
## -cution of the program. Plus, this is    ##
## also used to send the email in case the  ##
## remaining balance is less than a certain ##
## amount (specified in the check_balance   ##
## module)                                  ##
##                                          ##
##############################################
##############################################


import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_emails(logger, rem_bal_check, rem_balance, data):
    
    
    logger = logger


    # Configuring the credentials of the email to be sent
    try: 
        gmail_user = data["send_email_username"]
        gmail_password = data["send_email_password"]
        to = data["send_email_to"]
    except KeyError as e:  # In case the required key does not exist in the JSON file
        logger.error("One of the credentials for the email does not exist in the data file. Email cannot be sent. Exiting...")
        logger.error(e)
        sys.exit(1)


    # Configuring the required data for the email
    subject = "Logs for the booking script"
    if rem_bal_check == True: # Check whether its an email for low remaining credit
        body = "Uh oh! Its the low balance warning email again"
    else:
        body = "Attached is the log file for the execution of the script"
    sent_from = gmail_user


    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = gmail_user
    message["To"] = to
    if rem_bal_check == True: 
        message["Subject"] = "Low Remaining Balance Warning"
    else: 
        message["Subject"] = "Execution Logs for Booking Automation Program for Airlift" 


    # Adding body to email
    message.attach(MIMEText(body, "plain"))
    filename = "/var/log/booking-airlifts.txt"


    # Opening the file in binary mode
    with open(filename, "r") as attachment: 
        # Adding file as an octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())


    # Encoding the file in ASCII characters to send by email
    encoders.encode_base64(part)


    # Add header as key/value pair to attachment part
    part.add_header(
            "Content-Disposition", 
            f"attachment; filename= {filename}",
    )


## This block will be triggered in case the email is being sent
## to warn the user for low remaining credit

    # Checking whether this is an email for low balance warning
    if rem_bal_check == True: 
        html = """\
            <html>
                <body>
                    <h2>Hello, Earthling</h2>
                    <h3>Hope you are having a great day!!</h3>
                    <p>Your remaining balance is running low. Your current balance is """ + str(rem_balance) + """. Please re-charge at your earliest!
                    <br>Thanks!</br>
                    </p>
                    <p>Yours truly, </p>
                    <p>Airlift Booking Bot</p>
                </body>
            </html>
        """
        part1 = MIMEText(html, "html")
        message.attach(part1)
        text = message.as_string()

## End of Low 
## Balance Remaining Warning


    else:
        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()


## Email Sending Request Block
    try:
        server = smtplib.SMTP('smtp.gmail.com', port=587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, text)
        server.quit()
        logger.info("Email sent successfully!")
        # Send Emails...
    except smtplib.SMTPException as error:
        logger.error("Uh oh! Something went wrong while configuring the SMTP server")
        logger.error(str(error))
## End of Email Sending Request Block


    return None
