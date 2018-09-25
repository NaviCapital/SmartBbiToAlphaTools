import traceback
import datetime

def log_error(fullpath):
    error = "################\n"
    now = datetime.date.today().strftime("%Y-%m-%d %H:%M")
    error += f"{now}\n" + traceback.format_exc() + "\n"
    file = open(fullpath, "a")
    file.write(error)
    print(error)
