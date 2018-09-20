# Getting started

## Install project dependencies

Open a terminal, go to the root folder of this project, and run: ´pip install -r requirements.txt´

## Setup environment variables

Create a .env file in the root of the project.

Add the following variables to the file:

´´´
ALPHA_BASE_URL="http://prod.your_company_name.alphatools.com.br"
ALPHA_USERNAME=your_company_name
ALPHA_PASSWORD=super_password
´´´

## Get today's file from your broker

Get a real XML file with executions from SmartBBI - they usually send it every 20 mninutes via email. Place the file inside the ´files´ folder. Rename it to ´negocios.xml´.

Open the file ´app/executions.py´ and redirect the ´xml_doc´ variable to the right filename: ´negocios.xml´


# Usage

Double-click the ´executions.py´ file to import all executions from ´negocios.xml´ into your AlphaTools system.

# Contributing

Feel free to submit a pull-request with any improvement you might find useful.