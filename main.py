from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import config
import fdb
import time

# Инициализация WebClient с вашим Slack токеном
client = WebClient(token=config.TOKEN)

# ID канала, в котором находится сообщение
# channel_id = "C022PQ0N0UU"
channel_id = "C04TQPXT3UZ"

# Определяем timestamp последнего сообщения, чтобы не повторять обработку уже обработанных сообщений
oldest_timestamp = str(time.time())

# Основной цикл программы
while True:
    try:
        # Получение списка сообщений в канале Slack
        print(f'oldest_timestamp: {oldest_timestamp}')
        result = client.conversations_history(channel=channel_id, oldest=oldest_timestamp)
        messages = result["messages"]
        
        
        # Если есть новые сообщения, обработать их
        if len(messages) > 0:
            print(messages)
            for message in messages:
                # Получаем timestamp сообщения
                message_ts = message["ts"]
                texts = message["text"]
                print(type(texts))
                print(f'text: {texts}')
                
                # Добавляем кнопки, если это новое сообщение
                if message_ts > oldest_timestamp:
                    # Создаем блок с кнопками
                    blocks = None


                    
                    # Обновляем сообщение, добавляя блок с кнопками
                    try:
                        response = client.chat_update(
                            channel=channel_id,
                            ts=message_ts,
                            blocks=blocks,
                            text = texts + ' ОБНОВИЛ'
                        )
                        print("Сообщение успешно обновлено!")
                    except SlackApiError as e:
                        print("Ошибка обновления сообщения: {}".format(e))
                
                # Обновляем timestamp последнего сообщения
                if message_ts > oldest_timestamp:
                    oldest_timestamp = message_ts
            
        # Ждем 1 секунду перед следующей проверкой сообщений
        time.sleep(1)
    
    except SlackApiError as e:
        print("Ошибка при получении списка сообщений: {}".format(e))
