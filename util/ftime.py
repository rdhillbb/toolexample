from datetime import datetime

def distime():
    now = datetime.now()
    current_time_date = now.strftime("%Y-%m-%d %H:%M:%S")
    print("Current Date & Time:", current_time_date)
    print("---------\n")

