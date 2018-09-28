# Project-specific libraries
from . import base_client as Client

brokers_json = Client.request("execution", "get_brokers", None)

def get_broker_id(b3_id, hash = brokers_json):
  for key in hash:
    if hash[key]["tordist_code"] == b3_id:
      return int(hash[key]["id"])
