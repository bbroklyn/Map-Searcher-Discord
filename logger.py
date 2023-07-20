from datetime import datetime
import os

def write_log(message, author):
    current_date = datetime.now().strftime("%Y-%m-%d")
    folder = "logs"
    filename = os.path.join(folder, f"{current_date}.log")

    if not os.path.exists(folder):
        os.makedirs(folder)

    if os.path.isfile(filename):
        with open(filename, "a") as file:
            current_datetime = datetime.now().strftime("[%y.%m.%d %H:%M]")
            file.write(f"{current_datetime} {author} -> {message}\n")
    else:
        with open(filename, "w") as file:
            file.write("MAP SEARCHER BOT LOGS:\n")