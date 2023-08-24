import datetime
import pytz

Tz = pytz.timezone("Asia/Calcutta")
x = datetime.datetime.now(Tz)
today = str(x).split(" ")[0]
tday = today.split("-")[2]
year = today.split("-")[0]
month = x.strftime("%B")
tdate = tday + " " + month + " " + year
day = x.strftime("%A")