# Project-specific libraries
import base_client as Client

instruments_json = Client.request("instruments", "get_instruments", { "is_active": True })

def get_id(symbol, dict = instruments_json):
  for key in dict:
    if dict[key]["symbol"] == symbol:
      return int(dict[key]["id"])
  raise Exception(f"Instrument '{symbol}' not found")

def get_settlement_days(symbol, dict = instruments_json):
  for key in dict:
    if dict[key]["symbol"] == symbol:
      if dict[key]["settlement_days"] is None:
        raise Exception(f"Instrument '{symbol}' lacks settlement_days")
      else:
        return int(dict[key]["settlement_days"])
  raise Exception(f"Instrument '{symbol}' not found")
