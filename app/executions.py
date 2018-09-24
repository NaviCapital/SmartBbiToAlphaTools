# Project-specific libraries
import base_client as Client
import instruments as Instrument
import brokers as Broker
import market as Market

# External libraries
import datetime
from datetime import timedelta
from pprint import pprint
from bs4 import BeautifulSoup

def get_executions():
    xmldoc = open("../files/negocios.sample.xml", "r")
    xmldoc = BeautifulSoup(xmldoc, "lxml")
    negocios = xmldoc.findAll("negocio")
    executions = []
    for negocio in negocios:
        instrument_id = Instrument.get_id(negocio.ativo.text)
        execution_date = datetime.date.today()
        settlement_days = Instrument.get_settlement_days(negocio.ativo.text)
        settlement_date = Market.add_business_days(execution_date, settlement_days)
        executions.append({
            "broker_id": Broker.get_broker_id(122),
			"exec_ref_id": execution_date.strftime("%Y%m%d-") + negocio.id_operacao.text,
			"execution_date": execution_date.strftime("%Y-%m-%d"),
            "instrument_id": instrument_id,
			"quantity": int(negocio.qtd.text),
			"settlement_date": settlement_date.strftime("%Y-%m-%d"),
            "side": 1 if negocio.tipo.text == "C" else 2,
			"unit_value": float(negocio.preco.text.replace(",", ".")),
		})
        print("importando negocio", negocio.id_operacao.text, "de", len(negocios))
    return executions

try:
    Client.request("execution", "add_executions", { "executions": get_executions() })
except Exception as ex:
    print(ex)
    input("<press enter to quit>")