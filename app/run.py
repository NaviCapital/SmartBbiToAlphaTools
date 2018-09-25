# Load environment vars
import dotenv, os, subprocess
dotenv.load_dotenv(dotenv_path=dotenv.find_dotenv('.env'))

# Download XML files from Smart BBI
current_path = os.path.dirname(os.path.abspath(__file__)) + "\\" 
executable_path = current_path + os.path.join("smart_bbi", "TradeTracker.exe")
subprocess.call([executable_path, os.getenv("BBI_USERNAME"), os.getenv("BBI_PASSWORD")])

# Import executions to AlphaTools
from alpha_tools import executions as Execution
from alpha_tools import base_client as Client
from alpha_tools import helpers as Helper

try:
    Client.request("execution", "add_executions", { "executions": Execution.get_executions("bov") })
    print("Successfully imported BOV executions")
    raise Exception("aiasij")
    Client.request("execution", "add_executions", { "executions": Execution.get_executions("bmf") })
    print("Successfully imported BMF executions")
except Exception as ex:
    Helper.log_error(current_path + "logs.txt")