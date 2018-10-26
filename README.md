# Getting started

## Install project dependencies

Open a terminal, go to the root folder of this project, and run: `pip install -r requirements.txt`

## Setup environment variables

Create a `dev.env` file in the root of the project with the following content:

```
ALPHA_BASE_URL="http://prod.your_company_name.alphatools.com.br"
ALPHA_USERNAME=your_company_name
ALPHA_PASSWORD=super_password
ALPHA_XML_FOLDER="C://tmp/"

BBI_USERNAME=your_bbi_username
BBI_PASSWORD=your_bbi_password

SMTP_TO="operations@your_company.com.br"
SMTP_FROM="your_email@gmail.com"
SMTP_SERVER="smtp.your_server.com"
SMTP_PASS="y0ur_p4ssw0rd"

BLACKLIST="LAME4"
```


# Usage

Inside file explorer, go to the `SmartBbiToAlphaTools\app` folder, and double-click the `run.py` file to import today's trades from SmartBBI into AlphaTools.


# Contributing

Feel free to submit a pull-request with any improvement you might find useful.