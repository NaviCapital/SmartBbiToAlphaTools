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
    # pega orders da inoa e agrupa por broker-ativo-side-user
    inoa_orders = Execution.get_orders()    # return: order: { broker_id, side, instrument_id, qty, user_id }
    # dá merge nas orders com mesmo broker-ativo-side
    merged_inoa_orders = Execution.merge_orders(inoa_orders) # return: order: { broker_id, side, instrument_id, qty }

    # pega executions do xml
    executions_from_xml = Execution.get_all_executions_from_xml()

    # agrupa executions por broker-ativo-side
    merged_executions = Execution.merge_executions(executions_from_xml)

    # pra cada execution em executions: <=
    for execution in merged_executions:
        # busca uma order da inoa com a mesma chave <=
        execution = merged_executions[execution]
        merged_matching_order = Execution.find_merged_matching_inoa_order(execution, merged_inoa_orders)
        # se encontrar uma order com essa chave <=
        if merged_matching_order:
            # se a quantidade da order encontrada < qde da execution <=
            if float(merged_matching_order["quantity"]) < execution["quantity"]:
                # busca por uma order com user api e chave broker-ativo-side
                matching_order = Execution.find_matching_order_from_api_user(execution, inoa_orders)
                # se encontrar order do user api
                diff_qty = execution["quantity"] - float(merged_matching_order["quantity"])
                if matching_order:
                    # atualiza: qde += diferença
                    new_quantity = float(matching_order["quantity"]) + diff_qty
                    Execution.update_quantity(matching_order, new_quantity)
                # se nao encontrar order do user api
                else:
                    # cria uma nova order pro user api com a qde da diferenca
                    merged_matching_order["quantity"] = diff_qty
                    Execution.add_order(merged_matching_order)
        # se nao encontrar order com essa chave
        else:
            # cria order pro user api usando essa chave e qde total
            Execution.add_order_from_execution(execution)

    # Execution.create_orders(executions)
    Execution.add_executions(executions_from_xml)
    print("Successfully imported all executions")
    Helper.log(current_path + "logs.txt", "Successfully imported all executions")

except Exception as ex:
    Helper.log(current_path + "logs.txt", traceback.format_exc())
    Helper.send_email(str(ex), traceback.format_exc())
    print(traceback.format_exc())
