import datetime
from main import client

def timestamp_to_datetime(timestamp):
    dt = datetime.datetime.fromtimestamp(timestamp)
    return dt.strftime('%Y-%m-%d %H:%M:%S')

# message_ts = float('1685967260.402739')
oldest_timestamp = float('16859691228.043826') 

# print(timestamp_to_datetime(message_ts))
print(timestamp_to_datetime(oldest_timestamp))

channel_id = "C04TQPXT3UZ"
result = client.conversations_history(channel=channel_id, limit = 1)
messages = result["messages"]
print(result)