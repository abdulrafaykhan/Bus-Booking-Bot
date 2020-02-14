#!/bin/bash

# Starting block
echo "Starting installation for Python 3.7 along with PIP and virtualenv package" | tee -a installation.log 
echo "This script logs the execution in a local file named installation.log. Refer to it in case some problem arises" | tee -a installation.log


# Updating the packages
echo "Updating the repositories"
apt-get update | tee -a installation.log
# Error Handling
if [ $? -eq 0 ]; then
	echo "Repositories updated successfully" | tee -a installation.log
else
	echo "Failure to update repositories" | tee -a installation.log
	exit 1
fi


# Installing the python 3 packages
echo "Installing the Python packages" | tee -a installation.log
apt-get --yes install python3.7 python3.7-dev python3-pip | tee -a installation.log
# Error Handling
if [ $? -eq 0 ]; then
	echo "Python packages installed successfully" | tee -a installation.log
else
	echo "Failed to install python packages" | tee -a installation.log
	exit 1
fi


# Getting the pip installation file
echo "Fetching the pip install script" | tee -a installation.log
wget https://bootstrap.pypa.io/get-pip.py | tee -a installation.log
# Error Handling
if [ $? -eq 0 ]; then
	echo "Pip install script fetched successfully" | tee -a installation.log
else
	echo "Failed to fetch pip install script" | tee -a installation.log
	exit 1
fi


# Executing the get-pip.py
echo "Installing the Pip package" | tee -a installation.log
python3.7 get-pip.py | tee -a installation.log 
# Error Handling
if [ $? -eq 0 ]; then
	echo "PIP packages installed successfully" | tee -a installation.log
else
	echo "Failed to install PIP packages" | tee -a installation.log
	exit 1
fi


# Installing the virtualenv package
echo "Installing the virtualenv package" | tee -a installation.log
python3.7 -m pip install virtualenv | tee -a installation.log
# Error Handling
if [ $? -eq 0 ]; then
	echo "Virtualenv package was installed successfully" | tee -a installation.log
else
	echo "Failed to install virtualenv package" | tee -a installation.log
	exit 1
fi


# Creating the virtualenv
echo "Creating the virtual env"
python3.7 -m virtualenv --python=/usr/bin/python3.7 venv | tee -a installation.log
# Error Handling
if [ $? -eq 0 ]; then
	echo "Virtual Environment created successfully" | tee -a installation.log
else
	echo "Failed to create the virtual env" | tee -a installation.log 
	exit 1
fi


# Deleting the get-pip.py file
echo "Deleting the get-pip.py file" | tee -a installation.log
rm get-pip*
# Error Handling
if [ $? -eq 0 ]; then
	echo "get-pip.py file deleted successfully!" | tee -a installation.log
else
	echo "Failed to delete get-pip.py" | tee -a installation.log 
	exit 1
fi

# Installing the requirements
echo "Installing the requirements" | tee -a installation.log
pip install -r requirements.txt 
# Error Handling
if [ $? -eq 0 ]; then
	echo "Requirements Installed Successfully" | tee -a installation.log
else
	echo "Failed to install requirements successfully" | tee -a installation.log 
	exit 1
fi


# Ending block
echo "Installation completed successfully!" | tee -a installation.log
echo "You can activate the virtual env by running the command source venv/bin/activate" | tee -a installation.log
