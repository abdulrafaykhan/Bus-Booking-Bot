# Bus-Booking-Bot
A bot programmed to automate the process of booking daily commute buses. 

<h2>Requirements </h2>
This bot has been coded using Python 3.7. If you need any help in setting up a Python 3.7 env, follow through with the following method to install Python 3.7 along with virtual environment package on Ubuntu (for other OSes, feel free to open an issue): 
<ol>
  <li>apt-get install python3.7 python3.7-dev python3-pip</li>
  <li>wget https://bootstrap.pypa.io/get-pip.py</li>
  <li>python3.7 get-pip.py</li>
  <li>python3.7 -m pip install virtualenv</li>
  <li>python3.7 -m virtualenv --python=/usr/bin/python3.7 venv</li>
Finally, to activate the virtual environment, use the following command:
  <li>. venv/bin/activate</li>
</ol>

<h2>Flow</h2>
Initially it takes all the login credentials. Please enter them correctly as currently no regexes are there to check for the for format of emails or stuff. So please give input accurately. 
Then, it asks for sending emails. After the whole execution of the script, it sends the execution logs to an email address of your choosing. However, for that you need an email address through which you can send the email address (For configuration of such an email, feel free to open an issue). Finally, it will send the execution logs to an email of your choosing and for that no seperate configuration is required. 

<h2>Issues & Feature Request</h2>
By no standards is this good quality code. I need all the help in making this better. Thus, if you have any suggestions, recommendations, any kind of criticism, any request, feel free to open an issue on GitHub!

Thank you!
