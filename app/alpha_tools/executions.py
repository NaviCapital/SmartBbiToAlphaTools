# Project-specific libraries
from . import base_client as Client
from . import instruments as Instrument
from . import brokers as Broker
from . import market as Market

# External libraries
import os
import datetime
from datetime import timedelta
from bs4 import BeautifulSoup

def get_all_executions_from_xml():
    executions = []
    executions += get_executions_from_xml("bov")
    executions += get_executions_from_xml("bmf")
    return executions

def get_executions_from_xml(kind = "bov"):
    '''Read trades from xml file and format it to AlphaTools.'''
    today = datetime.date.today().strftime("%Y%m%d")
    path = os.getenv("ALPHA_XML_FOLDER") + f"negocios_{kind}_{today}.xml"
    xmldoc = open(path, "r")
    xmldoc = BeautifulSoup(xmldoc, "lxml")
    xml_negocios = xmldoc.findAll("negocio")
    executions = []
    count = len(xml_negocios)
    for xml_negocio in xml_negocios:
        if count % 100 == 0: print("reading negocios...", count)
        count -= 1
        hash_negocio = fetch_negocio_from_xml(xml_negocio, kind)
        if hash_negocio["instrument"] in os.getenv("BLACKLIST").split(","): continue
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
    return executions

def fetch_negocio_from_xml(xml_negocio, kind = "bov"):
    '''Parse trade info from XML file depending on its provenance.'''
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
        hash_negocio["broker"] = int(xml_negocio.cd_origem.text)
        hash_negocio["price"] = xml_negocio.pr_negocio.text
        hash_negocio["side"] = xml_negocio.cd_natope.text
    return hash_negocio

def add_executions(executions):
    '''Upload executions to Inoa Alpha Tools.'''
    execution_chunks = [executions[i:i + 200] for i in range(0, len(executions), 200)]
    count = len(execution_chunks)
    for chunk in execution_chunks:
        print("sending chunk", count); count -= 1
        Client.request("execution", "add_executions", { "executions": chunk })

def get_orders_based_on_xml_executions(executions):
    '''Returns a list of orders based on executions from XML.'''
    executions = merge_executions(executions)
    orders = []
    if len(executions) > 0:
        for execution_key in executions:
            ex = executions[execution_key]
            orders.append({
                "instrument_id": ex["instrument_id"],
                "side": ex["side"],
                "quantity": ex["quantity"],
                "date": ex["execution_date"],
                "base_price": 0,
                "notes": ""
            })
    return orders



def get_orders_based_on_created_executions(date=datetime.date.today().strftime("%Y-%m-%d")):
    '''Returns a list of orders based on executions created on AlphaTools.'''
    group_info = Client.request("execution", "get_execution_group_info", { "start_date": date, "end_date": date })
    orders = []
    if group_info["items"] and len(group_info["items"]) > 0:
        items = group_info["items"]
        for item in items:
            if item["quantity"] != 0:
                orders.append({
                    "instrument_id": item["instrument_id"],
                    "side": item["side"],
                    "quantity": item["quantity"],
                    "date": date,
                    "base_price": 0,
                    "notes": item["execution_group_id"]
                })
    return orders

def create_orders(executions):
    '''Create orders based on executions and make sure they are not duplicates.'''
    orders = get_orders_based_on_xml_executions(executions)
    for order in orders:
        matching_order = find_matching_order(instrument_id=order["instrument_id"], side=order["side"])
        if matching_order:
            if float(matching_order["quantity"]) != order["quantity"]:
                order["order_id"] = matching_order["order_id"]
                Client.request("execution", "add_orders", { "orders": [order], "user_id": 1 })
                print("updated order", order["order_id"])
        else:
            Client.request("execution", "add_orders", { "orders": [order], "user_id": 1 })
            print("created new order", order["quantity"])


def get_orders(date=datetime.date.today().strftime("%Y-%m-%d"), instrument_ids=None, side=None):
    '''Return all the orders from Inoa filtered by some specific parameters.'''
    orders = Client.request("execution", "get_order_info", {
        "start_date": date,
        "end_date": date,
        "instrument_ids": instrument_ids,
        "side": side })
    return orders

def find_matching_order(date=datetime.date.today().strftime("%Y-%m-%d"), instrument_id=None, side=None):
    '''Given a few parameters, return the id of the first matching order.'''
    orders = Client.request("execution", "get_order_info", {
        "start_date": date,
        "end_date": date,
        "instrument_ids": [instrument_id],
        "side": side})
    for order_id in orders:
        if orders[order_id]["user_id"] == 1:
            return orders[order_id]
    return None

def delete_today_orders(date=datetime.date.today().strftime("%Y-%m-%d")):
    '''Delete every order based on specific date.'''
    orders = Client.request("execution", "get_order_info", { "start_date": date, "end_date": date })
    Client.request("execution", "delete_orders", { "order_ids": [int(order_id) for order_id in orders]})

def delete_orders(order_ids):
    '''Delete orders by id.'''
    Client.request("execution", "delete_orders", { "order_ids": order_ids })

def delete_executions(executions):
    '''Delete specific executions.'''
    Client.request("execution", "delete_executions_by_exec_ref_id", {
                   "exec_ref_ids": [execution["exec_ref_id"] for execution in executions]})

def add_order(order):
    '''Create order.'''
    date = datetime.date.today().strftime("%Y-%m-%d")
    # todo: check if order comes with a date
    new_order = {
        "instrument_id": order["instrument_id"],
        "side": order["side"],
        "quantity": order["quantity"],
        "broker_id": order["broker_ids"][0],
        "date": date,
        "base_price": 0, "notes": "" }
    Client.request("execution", "add_orders", { "orders": [new_order], "user_id": 1})

def add_order_from_execution(execution):
    new_order = {
        "instrument_id": execution["instrument_id"],
        "side": execution["side"],
        "quantity": execution["quantity"],
        "broker_id": execution["broker_id"],
        "date": execution["execution_date"],
        "base_price": 0, "notes": "" }
    Client.request("execution", "add_orders", { "orders": [new_order], "user_id": 1 })

def merge_executions(executions):
    '''Group/merge executions by instrument, side, and broker.'''
    merged_executions = {}
    for execution in executions:
        merging_factors = [str(execution["instrument_id"]), str(
            execution["side"]), str(execution["broker_id"])]
        merging_id = "-".join(merging_factors)
        if merging_id in merged_executions:
            merged_executions[merging_id]["quantity"] += execution["quantity"]
        else:
            merged_executions[merging_id] = execution.copy()
    return merged_executions

def merge_orders(orders):
    '''Group/merge orders by instrument, side, and broker.'''
    merged_orders = {}
    for order in orders:
        order = orders[order]
        merging_factors = [str(order["instrument_id"]), str(order["side"]), str(order["broker_ids"][0])]
        merging_id = "-".join(merging_factors)
        if merging_id in merged_orders:
            merged_orders[merging_id]["quantity"] = float(merged_orders[merging_id]["quantity"]) + float(order["quantity"])
        else:
            merged_orders[merging_id] = order.copy()
    return merged_orders

def find_merged_matching_inoa_order(execution, merged_inoa_orders):
    '''Find merged_order with same broker, instrument_id, and side.'''
    for order in merged_inoa_orders:
        order = merged_inoa_orders[order]
        same_instrument = order["instrument_id"] == execution["instrument_id"]
        same_side = order["side"] == execution["side"]
        same_broker_id = order["broker_ids"][0] == execution["broker_id"]
        if same_instrument and same_side and same_broker_id:
            return order
    return None

def find_matching_order_from_api_user(execution, orders):
    '''Given a list of orders, find the first matching order from api user.'''
    for order in orders:
        order = orders[order]
        same_instrument = order["instrument_id"] == execution["instrument_id"]
        same_side = order["side"] == execution["side"]
        same_broker_id = order["broker_ids"][0] == execution["broker_id"]
        api_user = order["user_id"] == 1
        if same_instrument and same_side and same_broker_id and api_user:
            return order
    return None

def update_quantity(order, quantity):
    '''Update order quantity.'''
    new_order = {
        "instrument_id": order["instrument_id"],
        "side": order["side"],
        "quantity": str(quantity),
        "broker_id": order["broker_ids"][0],
        "date": order["date"],
        "order_id": order["order_id"],
        "base_price": 0, "notes": ""}
    Client.request("execution", "add_orders", { "orders": [new_order], "user_id": 1 })
