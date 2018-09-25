# Load environment vars
import dotenv, os, subprocess
path = dotenv.find_dotenv('.env')
dotenv.load_dotenv(dotenv_path=path)

# Settings
bbi_username = os.getenv("BBI_USERNAME")
bbi_password = os.getenv("BBI_PASSWORD")

# Download XML files from Smart BBI
executable_path = os.path.dirname(os.path.abspath(__file__)) + "\\" + os.path.join("smart_bbi", "TradeTracker.exe")
subprocess.call([executable_path, bbi_username, bbi_password])

# Import executions to AlphaTools
import executions as Execution
import base_client as Client
import traceback

try:
    Client.request("execution", "add_executions", { "executions": Execution.get_executions("bov") })
    print("Successfully imported BOV executions")
    Client.request("execution", "add_executions", { "executions": Execution.get_executions("bmf") })
    print("Successfully imported BMF executions")
except Exception as ex:
    print(traceback.format_exc())
