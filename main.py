from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import config
import fdb
import time
import datetime

def block_function(origin_text):

    return [
            {
            	"type": "section",
            	"text": {
            		"type": "mrkdwn",
            		"text": f"{origin_text}"
            	}
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "Approve"
                        },
                        "style": "primary",
                        "value": "click_me_123"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "Deny"
                        },
                        "style": "danger",
                        "value": "click_me_123"
                    }
                ]
            }
        ]

def timestamp_to_datetime(timestamp):
    timestamp = float(timestamp)
    dt = datetime.datetime.fromtimestamp(timestamp)
    return dt.strftime('%Y-%m-%d %H:%M:%S')

# Инициализация WebClient с вашим Slack токеном
client = WebClient(token=config.TOKEN)

# ID канала, в котором находится сообщение
# channel_id = "C022PQ0N0UU"
channel_id = "C04TQPXT3UZ"


# Определяем timestamp последнего сообщения, чтобы не повторять обработку уже обработанных сообщений
result = client.conversations_history(channel=channel_id, limit = 1)
oldest_timestamp = result['messages'][0]['ts']


# Основной цикл программы
while True:
    try:
        # Получение списка сообщений в канале Slack
        print(f'oldest_timestamp: {oldest_timestamp}, {timestamp_to_datetime(oldest_timestamp)}')
        result = client.conversations_history(channel = channel_id, oldest = oldest_timestamp)
        messages = result["messages"]

        
        
        # Если есть новые сообщения, обработать их
        if len(messages) > 0:

            print(f'Кол-во сообщений: {len(messages)}')
            print(messages)
            i = 0
            for message in messages:
                # Получаем timestamp сообщения
                i += 1
                print(i)
                message_ts = message["ts"]
                text = message["text"]

                print(f'text: {text}')
                print(f'message_ts: {message_ts}')
                print(f'date time: {timestamp_to_datetime(float(message_ts))}')
                # Добавляем кнопки, если это новое сообщение
                if float(message_ts) > float(oldest_timestamp):
                    # Создаем блок с кнопками
                    blocks = block_function(text)
 
                    
                    # Обновляем сообщение, добавляя блок с кнопками
                    try:
                        response = client.chat_update(
                            channel=channel_id,
                            ts=message_ts,
                            blocks=blocks#,
                            # text = texts + ' ОБНОВИЛ'
                        )
                        print("Сообщение успешно обновлено!")
                        oldest_timestamp = message_ts
                    except SlackApiError as e:
                        print("Ошибка обновления сообщения: {}".format(e))
                
            
        # Ждем 1 секунду перед следующей проверкой сообщений
        time.sleep(1)
    
    except SlackApiError as e:
        print("Ошибка при получении списка сообщений: {}".format(e))
