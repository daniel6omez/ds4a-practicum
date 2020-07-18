from TwStreamListener import *
from datetime import datetime


print(datetime.now())
print("Start process:")
myStreamListener = TwStreamListener()
myStreamListener.connect()
myStreamListener.run()
print("Stop process")


