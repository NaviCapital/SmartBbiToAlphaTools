import traceback
import datetime

def log_error():
    error = "################\n"
    now = datetime.date.today().strftime("%Y-%m-%d %H:%M")
    error += f"{now}\n" + traceback.format_exc() + "\n"
    file = open("logs.txt", "a")
    file.write(error)
    print(error)
