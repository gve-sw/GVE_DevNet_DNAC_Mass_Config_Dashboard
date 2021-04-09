# GVE_DevNet_DNAC_Mass_Config_Dashboard
A prototype developed to leverage the Template and PnP REST API capabilities of Cisco DNA-Center, to assist customers in the mass provisioning of Network Hardware.

### ALSO INCLUDED
DNAC-TemplateProgrammer Repo

## Contacts
* Alexander Hoecht
* Igor Manassypov

## Solution Components
* DNA-Center
*  Python
*  Flask
*  Docker

## Installation/Configuration
Steps needed to install and configure the project's environment
```
# Create a Virtual Environment
python3 -m venv Virtual_Environment

# Activate Virtual Environment
source Virtual_Environment/bin/activate # (MacOS)
Virtual_Environment/Scripts/activate # (Windows)

# Install Dependencies
pip install -r requirements.txt
```


## Starting the Application
Once Dependencies are installed to Environment:
```
# Setup Flask application
export FLASK_APP=src # (MacOS)
set FLASK_APP=src # (Windows Command Prompt)
$env:FLASK_APP = "src" # (Windows PowerShell)

# Enable Development Features
export FLASK_ENV=development # (MacOS)
set FLASK_ENV=development # (Windows Command Prompt)
$env:FLASK_ENV = "development" # (Windows PowerShell)

# Create Application Database
flask init-db

# Start Application
flask run
```




# Screenshots

![/IMAGES/0image.png](/IMAGES/0image.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
