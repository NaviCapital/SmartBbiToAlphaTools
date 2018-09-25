# Project-specific libraries
import base_client as Client
import instruments as Instrument
import brokers as Broker
import market as Market

# External libraries
import os
import datetime
from datetime import timedelta
from bs4 import BeautifulSoup

def get_executions(kind = "bov"):
    today = datetime.date.today().strftime("%Y%m%d")
    path = os.getenv("ALPHA_XML_FOLDER") + f"negocios_{kind}_{today}.xml"
    xmldoc = open(path, "r")
    xmldoc = BeautifulSoup(xmldoc, "lxml")
    xml_negocios = xmldoc.findAll("negocio")
    executions = []
    for xml_negocio in xml_negocios:
        hash_negocio = fetch_negocio_from_xml(xml_negocio, kind)
        execution_date = datetime.date.today()
        settlement_days = Instrument.get_settlement_days(hash_negocio["instrument"])
        settlement_date = Market.add_business_days(execution_date, settlement_days)
        curr_negocio = {
            "broker_id": Broker.get_broker_id(hash_negocio["broker"]),
			"exec_ref_id": execution_date.strftime("%Y%m%d-") + hash_negocio["external_id"],
			"execution_date": execution_date.strftime("%Y-%m-%d"),
            "instrument_id": Instrument.get_id(hash_negocio["instrument"]),
			"quantity": int(hash_negocio["quantity"]),
			"settlement_date": settlement_date.strftime("%Y-%m-%d"),
            "side": 1 if hash_negocio["side"] == "C" else 2,
			"unit_value": float(hash_negocio["price"].replace(",", ".")),
		}
        executions.append(curr_negocio)
        #print("importando negocio", hash_negocio["external_id"], "de", len(xml_negocios))
    return executions

def fetch_negocio_from_xml(xml_negocio, kind = "bov"):
    hash_negocio = {}
    if kind == "bov":
        hash_negocio["instrument"] = xml_negocio.ativo.text
        hash_negocio["external_id"] = xml_negocio.id_operacao.text
        hash_negocio["quantity"] = xml_negocio.qtd.text
        hash_negocio["broker"] = int(xml_negocio.origem.text)
        hash_negocio["price"] = xml_negocio.preco.text
        hash_negocio["side"] = xml_negocio.tipo.text
    elif kind == "bmf":
        hash_negocio["instrument"] = xml_negocio.cd_negocio.text
        hash_negocio["external_id"] = xml_negocio.nr_seqcomi.text
        hash_negocio["quantity"] = xml_negocio.qt_negocio.text
        hash_negocio["broker"] = int(xml_negocio.cd_corret.text)
        hash_negocio["price"] = xml_negocio.pr_negocio.text
        hash_negocio["side"] = xml_negocio.cd_natope.text
    return hash_negocio
