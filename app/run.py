# Load environment vars
import dotenv
import os
import subprocess
dotenv.load_dotenv(dotenv_path=dotenv.find_dotenv('dev.env'))

# Download XML files from Smart BBI
current_path = os.path.dirname(os.path.abspath(__file__)) + "\\"
executable_path = current_path + os.path.join("smart_bbi", "TradeTracker.exe")
subprocess.call([executable_path, os.getenv("BBI_USERNAME"), os.getenv("BBI_PASSWORD")])

# Import executions to AlphaTools
import traceback
from alpha_tools import executions as Execution
from alpha_tools import base_client as Client
from alpha_tools import helpers as Helper

try:
    executions = Execution.get_all_executions_from_xml()
    Execution.create_orders(executions)
    Execution.add_executions(executions)
    print("Successfully imported all executions")
    Helper.log(current_path + "logs.txt", "Successfully imported all executions")

except Exception as ex:
    Helper.log(current_path + "logs.txt", traceback.format_exc())
    Helper.send_email(str(ex), traceback.format_exc())
    print(traceback.format_exc())
