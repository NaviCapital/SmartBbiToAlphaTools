# Project-specific libraries
import base_client as Client

instruments_json = Client.request("instruments", "get_instruments", { "is_active": True })

def get_id(symbol, dict = instruments_json):
  for key in dict:
    if dict[key]["symbol"] == symbol:
      return int(dict[key]["id"])

def get_settlement_days(symbol, dict = instruments_json):
  for key in dict:
    if dict[key]["symbol"] == symbol:
      return int(dict[key]["settlement_days"])