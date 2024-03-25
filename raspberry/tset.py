import datetime
nowDate=datetime.datetime.now()

print(f"{str(nowDate.year)}-{str(nowDate.month)}-{str(nowDate.day)} {str(nowDate.hour)}:{str(nowDate.minute)}:{str(nowDate.second)}.{str(nowDate.microsecond)}")