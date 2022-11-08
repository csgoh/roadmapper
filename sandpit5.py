from datetime import datetime

print(datetime.strftime(datetime.today(), "%Y-%m-%d"))
print(datetime.strptime(datetime.strftime(datetime.today(), "%Y-%m-%d"), "%Y-%m-%d"))
